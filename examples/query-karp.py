"""Example using this library in sync code."""

from karp_api_client import Client, dsl
from karp_api_client.api import querying
from karp_api_client.shared import Response


def main() -> None:  # noqa: D103
    client = Client()

    with client as client:
        q = dsl.Equals(field="baseform", value="agha") | dsl.Equals(field="baseform", value="agin")
        response = querying.query_sync(
            "schlyter,soederwall,soederwall-supp",
            client=client,
            query_options=querying.QueryOptions(size=25, q=q),
        )
        response.map(_print_table).lash(lambda err: print(f"Error occurred!\n{err}"))
        # match response:
        #     case Success(resp):
        #         _print_table(resp.parsed)
        #     case Failure(err):
        #         print(f"Error occurred!\n{err}")


def _print_table(response: Response) -> None:
    print(f"{response=}")
    if response.parsed is None:
        print("No response")  # noqa: T201
        return
    print(f"{'baseform':20s}{'resource':20s}entry")  # noqa: T201
    for entry in response.parsed.hits:
        print(f"{entry.entry['baseform']:20s}{entry.resource:20s}{entry.to_dict()}")  # noqa: T201

    print("---")  # noqa: T201
    print(f"showing {len(response.parsed.hits)} entries of {response.parsed.total} in total.")  # noqa: T201


if __name__ == "__main__":
    main()
