"""Karp Query DSL."""

import copy
from collections.abc import Callable
from typing import Any, ClassVar, Union

from karp_api_client.shared import UNSET, Unset

try:
    from typing import Self  # type: ignore [attr-defined]
except ImportError:
    from typing_extensions import Self


class Query:
    """Base class for all queries."""

    _param_defs: ClassVar[dict[str, dict[str, Union[str, bool]]]] = {}

    def __init__(self, **params: Any) -> None:
        """Construct a Query."""
        self._params: dict[str, Any] = {}
        for pname, pvalue in params.items():
            self._params[pname] = pvalue

    # Add type annotations for methods not defined in every subclass
    __ror__: ClassVar[Callable[["Query", "Query"], "Query"]]

    def __or__(self, other: "Query") -> "Query":
        """Combine queries with or."""
        # make sure we give queries that know how to combine themselves
        # preference
        if hasattr(other, "__ror__"):
            return other.__ror__(self)
        return Or(self, other)

    def _clone(self) -> Self:
        c = self.__class__()
        for attr in self._params:
            c._params[attr] = copy.copy(self._params[attr])
        return c

    def __getattr__(self, name: str) -> Any:
        """Read a value if it exists."""
        value = None
        try:
            value = self._params[name]
        except KeyError:
            if (pinfo := self._param_defs.get(name)) and pinfo.get("multi"):
                value = self._params.setdefault(name, [])
        if value is None:
            raise AttributeError(f"{self.__class__.__name__!r} has no attribute {name!r}")
        return value


class Equals(Query):
    """Find all entries where the `field` equals `value`.

    Stricter than `contains`.
    """

    _param_defs: ClassVar[dict[str, dict[str, Union[str, bool]]]] = {
        "field": {"type": "query", "multi": False},
        "value": {"type": "query", "multi": False},
    }

    def __init__(self, _field: Union[str, Unset] = UNSET, _value: Union[str, Unset] = UNSET, **kwargs: Any) -> None:
        """Constuct a Equals query."""
        if _field is not UNSET:
            kwargs[str(_field)] = _value
        super().__init__(**kwargs)

    def __str__(self) -> str:
        """Format this query as the Karp Api."""
        return f"equals|{self.field}|{self.value}"


class Or(Query):
    """Find all entries that matches any of the queries."""

    _param_defs: ClassVar[dict[str, dict[str, Union[str, bool]]]] = {"ors": {"type": "query", "multi": True}}

    def __init__(self, *queries: Query) -> None:
        """Construct an Or query by combining two queries."""
        super().__init__(ors=list(queries))

    def __or__(self, other: "Query") -> "Query":
        """Combine other query with or."""
        q = self._clone()
        if isinstance(other, Or):
            q.ors.extend(other.ors)
        else:
            q_other = other._clone()
            q.ors.append(q_other)
        return q

    def __str__(self) -> str:
        """Format for Karp API."""
        queries = "||".join(str(q) for q in self.ors)
        return f"or({queries})"
