# karp-client-py
Karp API Client

> [!NOTE]
> This project is under development

## Installation

To add this package to your project
```shell
uv add git+https://github.com/spraakbanken/karp-api-client-py
```

## Usage

Use this library in sync code:

```python
from returns.result import Failure, Success

from karp_api_client import Client, dsl
from karp_api_client.api import querying
from karp_api_client.models.query_response import QueryResponse


def main():
    client = Client()

    with client as client:
        q = dsl.Equals(field="baseform", value="agha") | dsl.Equals(
            field="baseform", value="agin"
        )
        response = querying.query_sync(
            "schlyter,soederwall,soederwall-supp",
            client=client,
            query_options=querying.QueryOptions(size=25, q=q),
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
```

Or use it in async code:
```python
import anyio
from returns.result import Failure, Success

from karp_api_client import Client, dsl
from karp_api_client.api import querying
from karp_api_client.models.query_response import QueryResponse


async def main():
    client = Client()

    async with client as client:
        q = dsl.Equals(field="baseform", value="agha") | dsl.Equals(
            field="baseform", value="agin"
        )
        response = await querying.query_async(
            "schlyter,soederwall,soederwall-supp",
            client=client,
            query_options=querying.QueryOptions(size=25, q=q),
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
    anyio.run(main)
```

## Roadmap

- [ ] Karp Query DSL
  - [ ] Query operators
    - [ ] `contains|<field>|<string>`
    - [ ] `endswith|<field>|<string>`
    - [x] `equals|<field>|<string>`
    - [ ] `exists|<field>`
    - [ ] `freetext|<string>` 
    - [ ] `gt|<field>|<value>` 
    - [ ] `gte|<field>|<value>`
    - [ ] `lt|<field>|<value>`
    - [ ] `lte|<field>|<value>`
    - [ ] `missing|<field>` 
    - [ ] `regexp|<field>|<regex.*>`
    - [ ] `startswith|<field>|<string>`
  - [ ] Logical operators
    - [ ] `not(<expr1>||<expr2>||...)`
    - [ ] `and(<expr1>||<expr2>||...)`
    - [x] `or(<expr1>||<expr2>||...)`
  - [ ] Subqueries
- [ ] API Calls
  - [ ] Querying
    - [x] `/query/{resources}`
    - [ ] `/query/stats/{resources}`
    - [ ] `/query/entries/{resource_id}/{entry_ids}`
  - [ ] Editing
  - [ ] Statistics
  - [ ] History
  - [ ] Resources
  - [ ] Default
