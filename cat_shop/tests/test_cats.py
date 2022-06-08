import pytest
from flask.testing import FlaskClient
from db.models import Kitty, Breed, db
import datetime


@pytest.mark.parametrize(
    "url, expected_code",
    [("/cats/", 200), ("cats/1", 200), ("/breed/", 200), ("/breed/1", 200)],
)
def test_get_cats(client: FlaskClient, url: str, expected_code: int) -> None:
    response = client.get(url)
    assert expected_code == response.status_code

def test_post_breed(client: FlaskClient, app) -> None:
    with app.app_context():
        kitty_count = db.session.query(Breed).count()
    response = client.post("/breed/", json={"name": "new_breed"})
    with app.app_context():
        count_after = db.session.query(Breed).count()
    assert kitty_count + 1 == count_after

def test_post_breed(client: FlaskClient, app) -> None:
    breed_name = "new_breed"
    with app.app_context():
        breed_count = db.session.query(Breed).count()
    client.post("/breed/", json={"name": breed_name})
    with app.app_context():
        count_after = db.session.query(Breed).count()
        new_breed = db.session.query(Breed).filter_by(name=breed_name).first()
    assert breed_count + 1 == count_after
    assert new_breed.name == breed_name


def test_post_cats(client: FlaskClient, app) -> None:
    cat = dict(
        name="new_cat",
        description="new_cat_description",
        breed_id=1,
        birthday="2022-05-05",
    )
    with app.app_context():
        kitty_count = db.session.query(Kitty).count()
    client.post("/cats/", json=cat)
    with app.app_context():
        count_after = db.session.query(Kitty).count()
        new_cat = db.session.query(Kitty).filter_by(**cat).first()
    assert kitty_count + 1 == count_after
    assert new_cat.name == cat.get("name")
    assert new_cat.description == cat.get("description")
    assert new_cat.breed_id == cat.get("breed_id")
    assert new_cat.birthday == datetime.datetime.strptime(cat.get("birthday"), "%Y-%m-%d").date()


def test_delete_cat(client: FlaskClient, app) -> None:
    with app.app_context():
        kitty_count = db.session.query(Kitty).count()
    client.delete("/cats/1")
    with app.app_context():
        kitty_after_response = db.session.query(Kitty).count()
    assert kitty_after_response == kitty_count - 1


def test_delete_breed(client: FlaskClient, app) -> None:
    with app.app_context():
        breed_count = db.session.query(Breed).count()
    client.delete("/breed/1")
    with app.app_context():
        breed_after_response = db.session.query(Breed).count()
    assert breed_after_response == breed_count - 1


def test_delete_cat(client: FlaskClient, app) -> None:
    with app.app_context():
        kitty_count = db.session.query(Kitty).count()
    client.delete("/cats/1")
    with app.app_context():
        kitty_after_response = db.session.query(Kitty).count()
    assert kitty_after_response == kitty_count - 1


def test_patch_breed(client: FlaskClient, app) -> None:
    breed_id = 2
    new_breed_name = "new_breed_name"
    with app.app_context():
        old_breed = db.session.query(Breed).filter_by(id=breed_id).first()
    new_breed_name = f"{old_breed.name}_update"
    client.patch(f"/breed/{breed_id}", json={"name": new_breed_name})
    with app.app_context():
        new_breed = db.session.query(Breed).filter_by(id=breed_id).first()
    assert old_breed.name != new_breed.name
    assert new_breed.name == new_breed_name


def test_patch_cat(client: FlaskClient, app) -> None:
    cat_id = 2
    with app.app_context():
        old_cat = db.session.query(Kitty).filter_by(id=cat_id).first()
    new_cat_name = f"{old_cat.name}_update"
    client.patch(f"/cats/{cat_id}", json={"name": new_cat_name})
    with app.app_context():
        new_cat = db.session.query(Kitty).filter_by(id=cat_id).first()
    assert old_cat.name != new_cat.name
    assert new_cat.name == new_cat_name