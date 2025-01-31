"""Contains shared errors types that can be raised from API functions."""


class UnexpectedStatus(Exception):  # noqa: N818
    """Raised by api functions when the response status is an undocumented status.

    Only raised if Client.raise_on_unexpected_status is True.

    Args:
        status_code: the returned status code
        content: the content of the response
    """

    def __init__(self, status_code: int, content: bytes) -> None:
        self.status_code = status_code
        self.content = content

        super().__init__(
            f"Unexpected status code: {status_code}\n\nResponse content:\n{content.decode(errors='ignore')}"
        )


__all__ = ["UnexpectedStatus"]
