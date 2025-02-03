"""Query Response."""

from typing import TYPE_CHECKING, Any, Optional, TypeVar

import attrs

if TYPE_CHECKING:
    from karp_api_client.models.entry_dto import EntryDto

T = TypeVar("T", bound="QueryResponse")


@attrs.define
class QueryResponse:
    """Response returned from query."""

    total: int
    hits: list["EntryDto"]
    distribution: Optional[dict[str, int]]
    additional_properties: dict[str, Any] = attrs.field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict."""
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
        """Deserialize from dict."""
        from karp_api_client.models.entry_dto import EntryDto  # noqa: PLC0415

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
        """Get additional property keys."""
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        """Get an additional property by 'key'."""
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        """Set an additional property by 'key'."""
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        """Delete an additional property by 'key'."""
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        """Check if additional properties contains 'key'."""
        return key in self.additional_properties
