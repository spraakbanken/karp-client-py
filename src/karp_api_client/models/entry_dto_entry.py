"""Model for the entry in EntryDto."""

from typing import Any, Optional, TypeVar

import attrs

T = TypeVar("T", bound="EntryDtoEntry")


@attrs.define
class EntryDtoEntry:
    """Entry for EntryDto.entry."""

    additional_properties: dict[str, Any] = attrs.field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize as dict."""
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        """Deserialize from dict."""
        d = src_dict.copy()
        entry_dto_entry = cls()

        entry_dto_entry.additional_properties = d
        return entry_dto_entry

    @property
    def additional_keys(self) -> list[str]:
        """Get keys of additional properties."""
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        """Get additional property by 'key'."""
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        """Set additional property by 'key'."""
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        """Delete additional property by 'key'."""
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        """Check if additional properties contains 'key'."""
        return key in self.additional_properties

    def get(self, key: str, default=None) -> Optional[Any]:  # noqa: ANN001
        """Look up additional property by 'key' and fall back to default if not present."""
        try:
            return self.additional_properties[key]
        except KeyError:
            return default
