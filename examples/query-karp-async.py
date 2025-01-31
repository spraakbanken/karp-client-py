"""Example of using this library in async code."""

from typing import TypeVar

import anyio
from returns.interfaces.specific.ioresult import IOResultLike2

from karp_api_client import Client, dsl
from karp_api_client.api import querying
from karp_api_client.shared import Response

_IoKind = TypeVar("_IoKind", bound=IOResultLike2)


# @kinded
# def _query(
#     client_get: Callable[[str], Kind2[_IoKind, httpx.Response, Exception]],
#     url: str,
# ) -> Kind2[_IoKind, dict[str, Any], Exception]:
#     return client_get(url).map(lambda response: response.json())


# if __name__ == "__main__":
#     client = Client()
#     result_future = _query(
#         future_safe(client.get_async_client().get),
#         "https://spraakbanken4.it.gu.se/karp/v7/query/ao",
#     )
#     query_result = anyio.run(result_future.awaitable)
#     print(query_result)


async def main() -> None:  # noqa: D103
    client = Client()

    async with client as client:
        q = dsl.Equals(field="baseform", value="agha") | dsl.Equals(field="baseform", value="agin")
        response = await querying.query_async(
            "schlyter,soederwall,soederwall-supp",
            client=client,
            query_options=querying.QueryOptions(size=25, q=q),
        )
        response.map(_print_table).lash(lambda err: print(f"Error occurred!\n{err}"))


def _print_table(response: Response) -> None:
    if response.parsed is None:
        print("No response")  # noqa: T201
        return
    print(f"{'baseform':20s}{'resource':20s}entry")  # noqa: T201
    for entry in response.parsed.hits:
        print(f"{entry.entry['baseform']:20s}{entry.resource:20s}{entry.to_dict()}")  # noqa: T201

    print("---")  # noqa: T201
    print(f"showing {len(response.parsed.hits)} entries of {response.parsed.total} in total.")  # noqa: T201


if __name__ == "__main__":
    anyio.run(main)
