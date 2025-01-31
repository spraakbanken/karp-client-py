"""Query endpoint."""

from collections.abc import Sequence
from http import HTTPStatus
from typing import Any
from urllib import parse

import attrs
import httpx
from returns.result import Failure, Result, Success

from karp_api_client import AuthenticatedClient, Client, dsl, errors
from karp_api_client.models.http_validation_error import HttpValidationError
from karp_api_client.models.query_response import QueryResponse
from karp_api_client.shared import Response


@attrs.define
class QueryOptions:
    """Options for adapting a Query."""

    q: str | dsl.Query | None = attrs.field(default=None)
    from_: int | None = attrs.field(default=None)
    size: int | None = attrs.field(default=None)
    sort: list[str] | None = attrs.field(default=None)
    lexicon_stats: bool | None = attrs.field(default=None)
    path: str | None = attrs.field(default=None)
    highlight: bool | None = attrs.field(default=None)

    def to_query_string(self) -> str:
        """Format this object as a query string."""
        d: dict[str, int | str] = {}
        if self.q:
            d["q"] = str(self.q)
        if self.from_:
            d["from"] = self.from_
        if self.size:
            d["size"] = self.size
        if self.sort and len(self.sort) > 0:
            d["sort"] = ",".join(self.sort)
        if self.lexicon_stats is not None:
            d["lexicon_stats"] = "true" if self.lexicon_stats else "false"
        if self.path:
            d["path"] = self.path
        if self.highlight is not None:
            d["highlight"] = str(self.highlight)

        if d:
            return parse.urlencode(d, quote_via=parse.quote)
        return ""


def query_sync(
    resources: str | Sequence[str],
    *,
    client: Client | AuthenticatedClient,
    query_options: QueryOptions | None = None,
) -> Result[Response[QueryResponse], Response[HttpValidationError | None]]:
    """Query.

    Args:
        resources : sequence of resources as strings, or as a commas-separatade string.
        client : the client to use for this API call
        query_options : optional query options

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code
                                and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EntryAddResponse, HttpValidationError]]
    """
    kwargs = _get_query_kwargs(
        resources=resources,
        query_options=query_options,
    )
    response = client.get_sync_client().request(**kwargs)

    return _build_query_response(client=client, response=response)


async def query_async(
    resources: str | Sequence[str],
    *,
    client: Client | AuthenticatedClient,
    query_options: QueryOptions | None = None,
) -> Result[Response[QueryResponse], Response[HttpValidationError | None]]:
    """Query.

    Args:
        resources : sequence of resources as strings, or as a commas-separatade string.
        client : the client to use for this API call
        query_options : optional query options

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code
                                and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EntryAddResponse, HttpValidationError]]
    """
    kwargs = _get_query_kwargs(
        resources=resources,
        query_options=query_options,
    )
    response = await client.get_async_client().request(**kwargs)

    return _build_query_response(client=client, response=response)


def _get_query_kwargs(resources: Sequence[str] | str, *, query_options: QueryOptions | None) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    resources_ = resources if isinstance(resources, str) else ",".join(resources)

    qs = "" if query_options is None else query_options.to_query_string()
    url = f"/query/{resources_}{'?' if qs else ''}{qs}"

    kwargs: dict[str, Any] = {"method": "get", "url": url}
    headers["Accept"] = "application/json"
    kwargs["headers"] = headers
    return kwargs


def _build_query_response(
    *, client: Client | AuthenticatedClient, response: httpx.Response
) -> Result[Response[QueryResponse], Response[HttpValidationError | None]]:
    return (
        _parse_query_response(client=client, response=response)
        .map(
            lambda resp: Response(
                status_code=HTTPStatus(response.status_code),
                content=response.content,
                headers=response.headers,
                parsed=resp,
            )
        )
        .alt(
            lambda opt_resp: Response(
                status_code=HTTPStatus(response.status_code),
                content=response.content,
                headers=response.headers,
                parsed=opt_resp,
            )
        )
    )


def _parse_query_response(
    *, client: Client | AuthenticatedClient, response: httpx.Response
) -> Result[QueryResponse, HttpValidationError | None]:
    match response.status_code:
        case 200:
            response_200 = QueryResponse.from_dict(response.json())

            return Success(response_200)
        case 422:
            response_422 = HttpValidationError.from_dict(response.json())
            return Failure(response_422)
        case _:
            if client.raise_on_unexpected_status:
                raise errors.UnexpectedStatus(response.status_code, response.content)
            return Failure(None)
