import pytest
from flask.testing import FlaskClient


@pytest.mark.parametrize(
    "url, expected_code",
    [("/cats/", 200), ("cats/1", 200), ("/breed/", 200), ("/breed/1", 200)],
)
def test_get_cats(client: FlaskClient, url: str, expected_code: int) -> None:
    response = client.get(url)
    assert expected_code == response.status_code


# @pytest.mark.parametrize(
#     "url, expected_code",
#     [("/cats/", 201), ("/breed/", 201)],
# )
# def test_post_cats(client: FlaskClient, url: str, expected_code: int) -> None:
#     response = client.get(url)
#     assert expected_code == response.status_code