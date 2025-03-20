import json
from http import HTTPStatus

import pytest
from httpx import AsyncClient

from .answer_for_test import (
    good_response_create_tweet,
    good_response_image_load,
    good_response_result,
    response_get_tweets,
    response_user,
)


@pytest.mark.asyncio
async def test_get_api_users_me(ac: AsyncClient):
    """Тест эндпоинта get api/users/me"""
    response = await ac.get("/api/users/me", headers={"api-key": "test1"})
    users_data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert users_data == response_user


@pytest.mark.asyncio
async def test_get_api_users_id(ac: AsyncClient):
    """Тест эндпоинта get api/users/{id}"""
    response = await ac.get("/api/users/1", headers={"api-key": "test"})
    users_data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert users_data == response_user


@pytest.mark.asyncio
async def test_post_users_follow(ac: AsyncClient):
    """Тест эндпоинта post api/users/{id}/follow"""
    response = await ac.post(
        "/api/users/3/follow", headers={"api-key": "test1"}
    )
    assert response.status_code == HTTPStatus.OK
    response = response.json()
    assert response == good_response_result


@pytest.mark.asyncio
async def test_delete_users_follow(ac: AsyncClient):
    """Тест эндпоинта delete api/users/{id}/follow"""
    response = await ac.delete(
        "/api/users/3/follow", headers={"api-key": "test1"}
    )
    assert response.status_code == HTTPStatus.OK
    response = response.json()
    assert response == good_response_result


@pytest.mark.asyncio
async def test_get_tweet(ac: AsyncClient):
    """Тест для эндпоинта get api/tweets"""
    response = await ac.get("/api/tweets", headers={"api-key": "test"})
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert data == response_get_tweets


@pytest.mark.asyncio
async def test_post_tweet(ac: AsyncClient):
    """Тест для эндпоинта post api/tweets"""
    response = await ac.post(
        "/api/tweets",
        headers={"Content-Type": "application/json", "api-key": "test"},
        content=(
            json.dumps({"tweet_data": "test_data", "tweet_media_ids": [1]})
        ),
    )
    data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert data == good_response_create_tweet


@pytest.mark.asyncio
async def test_delete_tweet(ac: AsyncClient):
    """Тест для эндпоинта delete api/tweets"""
    response = await ac.delete("/api/tweets/3", headers={"api-key": "test"})
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data == good_response_result


@pytest.mark.asyncio
async def test_post_media(ac: AsyncClient):
    """Тест для эндпоинта post api/medias"""
    with open("tests/test_photo.jpg", "rb") as file:
        file_data = file.read()
    response = await ac.post(
        "/api/medias", headers={"api-key": "test"}, files={"file": file_data}
    )
    assert response.status_code == HTTPStatus.OK
    result = response.json()
    assert result == good_response_image_load


@pytest.mark.asyncio
async def test_get_medias(ac: AsyncClient):
    """Тест для эндпоинта get api/medias/{id}"""
    response = await ac.get("/api/medias/3", headers={"api-key": "test"})
    assert response.status_code == HTTPStatus.OK
    result = response.content
    with open("tests/test_photo.jpg", "rb") as file:
        file_data = file.read()
    assert result == file_data


@pytest.mark.asyncio
async def test_post_likes(ac: AsyncClient):
    """Тест для эндпоинта post api/tweets/{id}/likes"""
    response = await ac.post(
        "/api/tweets/2/likes", headers={"api-key": "test"}
    )
    assert response.status_code == HTTPStatus.OK
    response = response.json()
    assert response == good_response_result


@pytest.mark.asyncio
async def test_delete_likes(ac: AsyncClient):
    """Тест для эндпоинта delete api//tweets/{id}/likes"""
    response = await ac.delete(
        "/api/tweets/2/likes", headers={"api-key": "test"}
    )
    assert response.status_code == HTTPStatus.OK
    response = response.json()
    assert response == good_response_result
