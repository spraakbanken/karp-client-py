from karp_api_client.dsl.query import Equals
from returns.result import Failure, Success

from karp_api_client import Client, dsl
from karp_api_client.api.querying import query
from karp_api_client.models.query_response import QueryResponse


def main():
    client = Client()

    with client as client:
        q = dsl.Equals(field="baseform", needle="agha") || dsl.Equals(field="baseform",needle="agin")
        response = query.sync(
            client,
            "schlyter,soederwall,soederwall-supp",
            query_options=query.QueryOptions(
                size=25, q="or(equals|baseform|agha||equals|baseform|agin)"
            ),
        )
        match response:
            case Success(resp):
                _print_table(resp.parsed)
            case Failure(err):
                print(f"Error occurred!\n{err}")


def _print_table(response: QueryResponse | None) -> None:
    if response is None:
        print("No response")
        return
    print(f"{'baseform':20s}{'resource':20s}entry")
    for entry in response.hits:
        print(f"{entry.entry['baseform']:20s}{entry.resource:20s}{entry.to_dict()}")

    print("---")
    print(f"showing {len(response.hits)} entries of {response.total} in total.")


if __name__ == "__main__":
    main()
