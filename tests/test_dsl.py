from karp_api_client.dsl import Equals


def test_dsl(snapshot) -> None:  # noqa: ANN001
    q = Equals(field="baseform", value="agha") | Equals(field="baseform", value="agin")

    actual = str(q)

    assert actual == snapshot
