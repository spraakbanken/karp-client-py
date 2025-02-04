from karp_api_client.dsl import Equals, Or


def test_dsl(snapshot) -> None:  # noqa: ANN001
    q = Equals(field="baseform", value="agha") | Equals(field="baseform", value="agin")

    actual = str(q)

    assert actual == snapshot


def test_empty_or() -> None:
    q = Or()

    assert q.ors == []


def test_equals_combined(snapshot) -> None:  # noqa: ANN001
    q = Or()

    q |= Equals(field="baseform", value="agha")
    q |= Equals(field="baseform", value="agin")

    actual = str(q)

    assert actual == snapshot
