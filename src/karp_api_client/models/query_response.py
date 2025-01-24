from typing import TYPE_CHECKING, Any, TypeVar

import attrs

if TYPE_CHECKING:
    from karp_api_client.models.entry_dto import EntryDto

T = TypeVar("T", bound="QueryResponse")


@attrs.define
class QueryResponse:
    total: int
    hits: list["EntryDto"]
    distribution: dict[str, int] | None
    additional_properties: dict[str, Any] = attrs.field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        hits = [entry.to_dict() for entry in self.hits]

        field_dict: dict[str, Any] = {
            "total": self.total,
            "distibution": self.distribution,
        }
        field_dict.update(self.additional_properties)

        field_dict.update(
            {
                "hits": hits,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.entry_dto import EntryDto

        d = src_dict.copy()
        hits = [EntryDto.from_dict(entry) for entry in d.pop("hits")]
        total = d.pop("total")
        distribution = d.pop("distribution")

        query_response = cls(
            total=total,
            hits=hits,
            distribution=distribution,
        )

        query_response.additional_properties = d
        return query_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
