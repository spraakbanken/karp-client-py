from http import HTTPStatus
from typing import Any, Optional, Sequence, Union
from urllib import parse

import attrs
import httpx
from returns.result import Failure, Result, Success

from karp_api_client import AuthenticatedClient, Client, dsl, errors
from karp_api_client.models.http_validation_error import HttpValidationError
from karp_api_client.models.query_response import QueryResponse
from karp_api_client.types import Response


@attrs.define
class QueryOptions:
    q: Optional[Union[str, dsl.Query]] = attrs.field(default=None)
    from_: Optional[int] = attrs.field(default=None)
    size: Optional[int] = attrs.field(default=None)
    sort: Optional[list[str]] = attrs.field(default=None)
    lexicon_stats: Optional[bool] = attrs.field(default=None)
    path: Optional[str] = attrs.field(default=None)
    highlight: Optional[bool] = attrs.field(default=None)

    def to_query_string(self) -> str:
        d: dict[str, Union[int, str]] = {}
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
    resources: Union[str, Sequence[str]],
    *,
    client: Union[Client, AuthenticatedClient],
    query_options: QueryOptions | None = None,
) -> Result[Response[QueryResponse], Response[HttpValidationError | None]]:
    """Query.


    Args:
        resources : sequence of resources as strings, or as a commas-separatade string.
        query_options : optional query options

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EntryAddResponse, HttpValidationError]]
    """
    kwargs = _get_query_kwargs(
        resources=resources,
        query_options=query_options,
    )
    print(f"{kwargs=}")
    response = client.get_sync_client().request(**kwargs)

    return _build_query_response(client=client, response=response)


async def query_async(
    resources: Union[str, Sequence[str]],
    *,
    client: Union[Client, AuthenticatedClient],
    query_options: QueryOptions | None = None,
) -> Result[Response[QueryResponse], Response[HttpValidationError | None]]:
    """Query.


    Args:
        resources : sequence of resources as strings, or as a commas-separatade string.
        query_options : optional query options

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EntryAddResponse, HttpValidationError]]
    """
    kwargs = _get_query_kwargs(
        resources=resources,
        query_options=query_options,
    )
    print(f"{kwargs=}")
    response = await client.get_async_client().request(**kwargs)

    return _build_query_response(client=client, response=response)


def _get_query_kwargs(
    resources: Union[Sequence[str], str], *, query_options: QueryOptions | None
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    if isinstance(resources, str):
        _resources = resources
    else:
        _resources = ",".join(resources)

    qs = "" if query_options is None else query_options.to_query_string()
    url = f"/query/{_resources}{'?' if qs else ''}{qs}"

    _kwargs: dict[str, Any] = {"method": "get", "url": url}
    headers["Accept"] = "application/json"
    _kwargs["headers"] = headers
    return _kwargs


def _build_query_response(
    *, client: Union[Client, AuthenticatedClient], response: httpx.Response
) -> Result[Response[QueryResponse], Response[Optional[HttpValidationError]]]:
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
    *, client: Union[Client, AuthenticatedClient], response: httpx.Response
) -> Result[QueryResponse, Optional[HttpValidationError]]:
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
            else:
                return Failure(None)
