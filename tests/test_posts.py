import pytest

from app import schemas


def test_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    print(res.json())
    assert res.status_code == 200


def test_unauth_get_one_post(test_posts,client):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(test_posts, authorized_client):
    res = authorized_client.get("/posts/9000")
    assert res.status_code == 404


def test_get_one_post(test_posts, authorized_client):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200


@pytest.mark.parametrize("title, content, published", [
    ("Happy to be in Delhi", "Delhi is awesome !!!!", True),
    ("Love Uttarakhand !", "Uttarakhand is majestic and beautiful !!!!", False)
])
def test_create_post(test_user, authorized_client, title, content, published):
    res = authorized_client.post("/posts/create_post", json={"title": title, "content": content, "published":published})
    assert res.status_code == 201


def test_delete_one_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_non_exist(authorized_client):
    res = authorized_client.delete("/posts/90000")
    assert res.status_code == 404


def test_update_post(authorized_client, test_posts):
    data = {
        "title": "Welcome to Goa !",
        "content": "Goa is so pretty!! Specially in winters !",
        "user_id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 200


def test_update_non_exist(authorized_client, test_posts):
    data = {
        "title": "Welcome to Goa !",
        "content": "Goa is so pretty!! Specially in winters !",
        "user_id": test_posts[0].id
    }
    res = authorized_client.put("/posts/90000", json= data)
    assert res.status_code == 404
