import os
import ssl
import typing
from typing import Any, Optional, Self, TypeVar, Union

import attrs
import httpx


class ApiKeyAuth(httpx.Auth):
    def __init__(self, token: str) -> None:
        self.api_token = token

    def auth_flow(
        self, request: httpx.Request
    ) -> typing.Generator[httpx.Request, httpx.Response, None]:
        request.url = request.url.copy_with(api_key=self.api_token)
        yield request


T = TypeVar("T", bound="ClientBase")


@attrs.define(slots=False)
class ClientBase:
    raise_on_unexpected_status: bool = attrs.field(default=False, kw_only=True)
    _base_url: str = attrs.field(
        default="https://spraakbanken4.it.gu.se/karp/v7", alias="base_url"
    )
    _cookies: dict[str, str] = attrs.field(factory=dict, kw_only=True, alias="cookies")
    _headers: dict[str, str] = attrs.field(factory=dict, kw_only=True, alias="headers")
    _timeout: Optional[httpx.Timeout] = attrs.field(
        default=None, kw_only=True, alias="timeout"
    )
    _verify_ssl: Union[str, bool, ssl.SSLContext] = attrs.field(
        default=True, kw_only=True, alias="verify_ssl"
    )
    _follow_redirects: bool = attrs.field(
        default=False, kw_only=True, alias="follow_redirects"
    )
    _httpx_args: dict[str, Any] = attrs.field(
        factory=dict, kw_only=True, alias="httpx_args"
    )
    _client: Optional[httpx.Client] = attrs.field(default=None, init=False)
    _async_client: Optional[httpx.AsyncClient] = attrs.field(default=None, init=False)

    def set_base_url(self, base_url: str) -> Self:
        """Update the base_url for this Client."""
        self._base_url = base_url
        return self

    def with_headers(self, headers: dict[str, str]) -> Self:
        """Get a new client matching this one with additional headers"""
        if self._client is not None:
            self._client.headers.update(headers)
        if self._async_client is not None:
            self._async_client.headers.update(headers)
        return attrs.evolve(self, headers={**self._headers, **headers})

    def with_cookies(self, cookies: dict[str, str]) -> Self:
        """Get a new client matching this one with additional cookies"""
        if self._client is not None:
            self._client.cookies.update(cookies)
        if self._async_client is not None:
            self._async_client.cookies.update(cookies)
        return attrs.evolve(self, cookies={**self._cookies, **cookies})

    def with_timeout(self, timeout: httpx.Timeout) -> Self:
        """Get a new client matching this one with a new timeout (in seconds)"""
        if self._client is not None:
            self._client.timeout = timeout
        if self._async_client is not None:
            self._async_client.timeout = timeout
        return attrs.evolve(self, timeout=timeout)

    def set_sync_client(self, client: httpx.Client) -> Self:
        """Manually set the underlying httpx.Client

        **NOTE**: This will override any other settings on the client, including cookies, headers, and timeout.
        """
        self._client = client
        return self

    def get_sync_client(self) -> httpx.Client:
        """Get the underlying httpx.Client, constructing a new one if not previously set"""
        if self._client is None:
            self._client = self._create_sync_client()
        return self._client

    # @abc.abstractmethod
    def _create_sync_client(self) -> httpx.Client:
        return httpx.Client(
            base_url=self._base_url,
            cookies=self._cookies,
            headers=self._headers,
            timeout=self._timeout,
            verify=self._verify_ssl,
            follow_redirects=self._follow_redirects,
            **self._httpx_args,
        )

    def __enter__(self) -> Self:
        """Enter a context manager for self.client—you cannot enter twice (see httpx docs)"""
        self.get_sync_client().__enter__()
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        """Exit a context manager for internal httpx.Client (see httpx docs)"""
        self.get_sync_client().__exit__(*args, **kwargs)

    def set_async_client(self, async_client: httpx.AsyncClient) -> Self:
        """Manually the underlying httpx.AsyncClient

        **NOTE**: This will override any other settings on the client, including cookies, headers, and timeout.
        """
        self._async_client = async_client
        return self

    def get_async_client(self) -> httpx.AsyncClient:
        """Get the underlying httpx.AsyncClient, constructing a new one if not previously set"""
        if self._async_client is None:
            self._async_client = self._create_async_client()
        return self._async_client

    def _create_async_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            base_url=self._base_url,
            cookies=self._cookies,
            headers=self._headers,
            timeout=self._timeout,
            verify=self._verify_ssl,
            follow_redirects=self._follow_redirects,
            **self._httpx_args,
        )

    async def __aenter__(self) -> Self:
        """Enter a context manager for underlying httpx.AsyncClient—you cannot enter twice (see httpx docs)"""
        await self.get_async_client().__aenter__()
        return self

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:
        """Exit a context manager for underlying httpx.AsyncClient (see httpx docs)"""
        await self.get_async_client().__aexit__(*args, **kwargs)


@attrs.define(slots=False)
class Client(ClientBase):
    """Client to use for unauthenticated API calls."""


@attrs.define(slots=False)
class AuthenticatedClient(ClientBase):
    """Client to use for authenticated API calls."""

    _token: str = attrs.field(kw_only=True, alias="token")

    def _create_sync_client(self) -> httpx.Client:
        client = super()._create_sync_client()
        client.auth = ApiKeyAuth(self._token)
        return client

    def _create_async_client(self) -> httpx.AsyncClient:
        client = super()._create_async_client()
        client.auth = ApiKeyAuth(self._token)
        return client

    @classmethod
    def from_env(cls) -> "AuthenticatedClient":
        token = None
        if token_from_env := os.environ.get("KARP_API_CLIENT_API_TOKEN"):
            token = token_from_env
        elif token_from_env := os.environ.get("KARP_API_TOKEN"):
            token = token_from_env

        if token is None:
            raise RuntimeError("must set KARP_API_CLIENT_API_TOKEN or KARP_API_TOKEN")
        else:
            return cls(token=token)
