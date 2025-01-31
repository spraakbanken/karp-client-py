"""Utility types."""

from collections.abc import MutableMapping
from http import HTTPStatus
from typing import Generic, Literal, Optional, TypeVar

import attrs


class Unset:
    def __bool__(self) -> Literal[False]:
        return False

    def __str__(self) -> str:
        return "UNSET"

    def __repr__(self) -> str:
        return "UNSET"


UNSET: Unset = Unset()
T = TypeVar("T")


@attrs.define
class Response(Generic[T]):
    """A response from an endpoint."""

    status_code: HTTPStatus
    content: bytes
    headers: MutableMapping[str, str]
    parsed: Optional[T]


__all__ = ["Response"]
