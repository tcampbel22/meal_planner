import pytest
from seed_db import seed_recipes
from utils import get_all_recipes

RECIPE_URL = "/api/recipes/"


@pytest.fixture(scope="function", autouse=True)
def seed_recipe_data(session, create_one_user):
    return seed_recipes(session)


class TestReadRecipe:
    def test_read_all_recipes(self, client):
        res = client.get(RECIPE_URL)
        assert res.status_code == 200
        assert len(res.json()) == 3

    def test_read_user_recipes(self, client, auth_headers, create_one_user):
        res = client.get(RECIPE_URL, headers=auth_headers)
        assert res.status_code == 200
        assert len(res.json()) == 3
        recipes = res.json()
        bob_id = create_one_user.id
        for recipe in recipes:
            assert recipe["user_id"] == str(bob_id)

        pasta_recipe = next(
            (r for r in recipes if r["recipeName"] == "Pasta Carbonara"), None
        )

        assert pasta_recipe is not None
        assert pasta_recipe["url"] == "https://www.italy.com"
        assert pasta_recipe["cuisine"] == "Italian"
        assert pasta_recipe["user_id"] == str(bob_id)


class TestAddRecipes:
    def test_add_recipe_no_name(
        self, client, auth_headers, create_one_user, session
    ):
        assert len(get_all_recipes(session)) == 3

        res = client.post(
            RECIPE_URL,
            headers=auth_headers,
            json={
                "recipeName": "",
                "recipeUrl": "https://finland.fi/",
                "cuisine": "Finnish",
                "portionSize": 4,
            },
        )
        assert res.status_code == 422
        assert len(get_all_recipes(session)) == 3

    def test_add_recipe_no_url(
        self, client, auth_headers, create_one_user, session
    ):
        assert len(get_all_recipes(session)) == 3

        res = client.post(
            RECIPE_URL,
            headers=auth_headers,
            json={
                "recipeName": "Makaroni Laatikko",
                "recipeUrl": "",
                "cuisine": "Finnish",
                "portionSize": 4,
            },
        )
        assert res.status_code == 422
        assert len(get_all_recipes(session)) == 3

    def test_add_recipe_portions_is_str(
        self, client, auth_headers, create_one_user, session
    ):
        assert len(get_all_recipes(session)) == 3

        res = client.post(
            RECIPE_URL,
            headers=auth_headers,
            json={
                "recipeName": "Makaroni Laatikko",
                "recipeUrl": "https://finland.fi/",
                "cuisine": "Finnish",
                "portionSize": "hello",
            },
        )
        assert res.status_code == 422
        assert len(get_all_recipes(session)) == 3

    def test_add_one_recipe(
        self, client, auth_headers, create_one_user, session
    ):
        assert len(get_all_recipes(session)) == 3
        res = client.post(
            RECIPE_URL,
            headers=auth_headers,
            json={
                "recipeName": "Makaroni Laatikko",
                "recipeUrl": "https://finland.fi/",
                "cuisine": "Finnish",
                "portionSize": 4,
            },
        )
        assert res.status_code == 201
        assert len(get_all_recipes(session)) == 4

        new_recipe = res.json()
        bob_id = create_one_user.id

        assert new_recipe is not None
        assert new_recipe["user_id"] == str(bob_id)
        assert new_recipe["recipeName"] == "Makaroni Laatikko"
        assert new_recipe["url"] == "https://finland.fi/"
        assert new_recipe["cuisine"] == "Finnish"
        assert new_recipe["portionSize"] == 4
