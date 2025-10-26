import pytest

# from utils import delete_user, get_users_length, get_all_users
from seed_db import seed_recipes

RECIPE_URL = "/api/recipes/"


@pytest.fixture(scope="function", autouse=True)
def seed_recipe_data(session):
    """Seeds the database with recipe data for recipe tests."""
    return seed_recipes(session)


class TestRecipeEndpoints:
    def test_read_all_recipes(self, client):
        res = client.get(RECIPE_URL)
        assert res.status_code == 200
        assert len(res.json()) == 3

    # def read_user_recipes(self, client, auth_headers):
    #     res = client.get(RECIPE_URL, headers=auth_headers)
    #     assert res.status_code == 200
    #     assert len(res.json()) == 3
    #     assert res.json() == {
    #         [
    #             {}
    #         ]
    #     }
