"""EntryDto model."""

from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from karp_api_client.shared import UNSET, Unset

if TYPE_CHECKING:
    from karp_api_client.models.entry_dto_entry import EntryDtoEntry


T = TypeVar("T", bound="EntryDto")


@_attrs_define
class EntryDto:
    """EntryDto.

    Attributes:
    id (str):
    version (int):
    last_modified (float):
    last_modified_by (str):
    resource (str):
    entry (EntryDtoEntry):
    message (Union[None, Unset, str]):
    discarded (Union[Unset, bool]):  Default: False.
    """

    id: str
    version: int
    last_modified: float
    last_modified_by: str
    resource: str
    entry: "EntryDtoEntry"
    message: Union[Unset, str, None] = UNSET
    discarded: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize this object to dict."""
        id_ = self.id

        version = self.version

        last_modified = self.last_modified

        last_modified_by = self.last_modified_by

        resource = self.resource

        entry = self.entry.to_dict()

        message: Union[Unset, str, None]
        message = UNSET if isinstance(self.message, Unset) else self.message

        discarded = self.discarded

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id_,
                "version": version,
                "last_modified": last_modified,
                "last_modified_by": last_modified_by,
                "resource": resource,
                "entry": entry,
            }
        )
        if message is not UNSET:
            field_dict["message"] = message
        if discarded is not UNSET:
            field_dict["discarded"] = discarded

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        """Deserialize from dict."""
        from karp_api_client.models.entry_dto_entry import EntryDtoEntry  # noqa: PLC0415

        d = src_dict.copy()
        id_ = d.pop("id")

        version = d.pop("version")

        last_modified = d.pop("last_modified")

        last_modified_by = d.pop("last_modified_by")

        resource = d.pop("resource")

        entry = EntryDtoEntry.from_dict(d.pop("entry"))

        def _parse_message(data: object) -> Union[Unset, str, None]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[Unset, str, None], data)

        message = _parse_message(d.pop("message", UNSET))

        discarded = d.pop("discarded", UNSET)

        entry_dto = cls(
            id=id_,
            version=version,
            last_modified=last_modified,
            last_modified_by=last_modified_by,
            resource=resource,
            entry=entry,
            message=message,
            discarded=discarded,
        )

        entry_dto.additional_properties = d
        return entry_dto

    @property
    def additional_keys(self) -> list[str]:
        """Return any additional keys."""
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        """Get an additional property by key."""
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        """Set an additional property."""
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        """Delete an additional property."""
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        """Check if this object contains an additional propery 'key'."""
        return key in self.additional_properties
