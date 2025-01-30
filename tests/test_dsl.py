from karp_api_client.dsl import Equals


def test_dsl(snapshot) -> None:
    q = Equals(field="baseform", value="agha") | Equals(field="baseform", value="agin")

    actual = q.to_query_string()

    assert actual == snapshot
