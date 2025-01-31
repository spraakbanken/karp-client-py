"""Validation error."""

from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ValidationError")


@_attrs_define
class ValidationError:
    """Validation error.

    Attributes:
    loc (list[Union[int, str]]):
    msg (str):
    type_ (str):
    """

    loc: list[int | str]
    msg: str
    type_: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict."""
        loc = []
        for loc_item_data in self.loc:
            loc_item: int | str
            loc_item = loc_item_data
            loc.append(loc_item)

        msg = self.msg

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "loc": loc,
                "msg": msg,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        """Deserialize from dict."""
        d = src_dict.copy()
        loc = []
        loc_ = d.pop("loc")
        for loc_item_data in loc_:

            def _parse_loc_item(data: object) -> int | str:
                return cast(int | str, data)

            loc_item = _parse_loc_item(loc_item_data)

            loc.append(loc_item)

        msg = d.pop("msg")

        type_ = d.pop("type")

        validation_error = cls(
            loc=loc,
            msg=msg,
            type_=type_,
        )

        validation_error.additional_properties = d
        return validation_error

    @property
    def additional_keys(self) -> list[str]:
        """Additonal keys."""
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
        """Check if this the additional properties contains 'key'."""
        return key in self.additional_properties
