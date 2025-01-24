from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.entry_dto_entry import EntryDtoEntry


T = TypeVar("T", bound="EntryDto")


@_attrs_define
class EntryDto:
    """
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
    message: Union[None, Unset, str] = UNSET
    discarded: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        version = self.version

        last_modified = self.last_modified

        last_modified_by = self.last_modified_by

        resource = self.resource

        entry = self.entry.to_dict()

        message: Union[None, Unset, str]
        if isinstance(self.message, Unset):
            message = UNSET
        else:
            message = self.message

        discarded = self.discarded

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
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
        from ..models.entry_dto_entry import EntryDtoEntry

        d = src_dict.copy()
        id = d.pop("id")

        version = d.pop("version")

        last_modified = d.pop("last_modified")

        last_modified_by = d.pop("last_modified_by")

        resource = d.pop("resource")

        entry = EntryDtoEntry.from_dict(d.pop("entry"))

        def _parse_message(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        message = _parse_message(d.pop("message", UNSET))

        discarded = d.pop("discarded", UNSET)

        entry_dto = cls(
            id=id,
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
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
