import copy
from typing import Any, Callable, ClassVar, Self, Union


class Query:
    _param_defs: ClassVar[dict[str, dict[str, Union[str, bool]]]] = {}

    def __init__(self, **params: Any) -> None:
        self._params: dict[str, Any] = {}
        for pname, pvalue in params.items():
            self._params[pname] = pvalue

    # Add type annotations for methods not defined in every subclass
    __ror__: ClassVar[Callable[["Query", "Query"], "Query"]]

    def __or__(self, other: "Query") -> "Query":
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
        value = None
        try:
            value = self._params[name]
        except KeyError:
            if pinfo := self._param_defs.get(name):
                if pinfo.get("multi"):
                    value = self._params.setdefault(name, [])
        if value is None:
            raise AttributeError(
                f"{self.__class__.__name__!r} has no attribute {name!r}"
            )
        return value


class Equals(Query):
    _param_defs = {
        "field": {"type": "query", "multi": False},
        "value": {"type": "query", "multi": False},
    }

    def __init__(self, *, field: str, value: str) -> None:
        super().__init__(
            field=field,
            value=value,
        )

    def to_query_string(self) -> str:
        return f"equals|{self.field}|{self.value}"


class Or(Query):
    _param_defs = {"ors": {"type": "query", "multi": True}}

    def __init__(self, first: Query, second: Query) -> None:
        super().__init__(ors=[first, second])

    def __or__(self, other: "Query") -> "Query":
        q = self._clone()
        if isinstance(other, Or):
            q.ors.extend(other.ors)
        else:
            q.ors.append(other)
        return q

    def to_query_string(self) -> str:
        queries = "||".join((q.to_query_string() for q in self.ors))
        return f"or({queries})"
