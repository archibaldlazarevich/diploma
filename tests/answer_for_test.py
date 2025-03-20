users: list[dict] = [
    {"name": "Nik", "api_key": "test1"},
    {"name": "Alex", "api_key": "test2"},
    {"name": "Kol", "api_key": "test3"},
    {"name": "test", "api_key": "test"},
]

media: list[dict] = [
    {"path": "/app/src/images/photo.jpg"},
    {"path": "/app/src/images/photo.jpg"},
    {"path": "/app/src/images/test_photo.jpg"},
]

tweets: list[dict] = [
    {
        "user_id": 1,
        "tweets_likes": 1,
        "tweets_data": "tweet_test_1",
        "tweet_media_ids": 1,
    },
    {
        "user_id": 1,
        "tweets_likes": 2,
        "tweets_data": "tweet_test_1",
        "tweet_media_ids": 2,
    },
    {
        "user_id": 4,
        "tweets_likes": 0,
        "tweets_data": "tweet_test_1",
        "tweet_media_ids": 2,
    },
]

likes: list[dict] = [
    {"user_id": 1, "tweets_id": 1},
    {"user_id": 1, "tweets_id": 2},
    {"user_id": 4, "tweets_id": 2},
]

followed_data: list[dict] = [
    {"follower_id": 1, "followed_id": 2},
    {"follower_id": 3, "followed_id": 4},
]

response_user: dict = {
    "result": True,
    "user": {
        "id": 1,
        "name": "Nik",
        "followers": [],
        "following": [{"id": 2, "name": "Alex"}],
    },
}


response_get_tweets: dict = {
    "result": True,
    "tweets": [
        {
            "id": 2,
            "content": "tweet_test_1",
            "attachments": ["/api/medias/2"],
            "author": {"id": 1, "name": "Nik"},
            "likes": [
                {"user_id": 1, "name": "Nik"},
                {"user_id": 4, "name": "test"},
            ],
        },
        {
            "id": 1,
            "content": "tweet_test_1",
            "attachments": ["/api/medias/1"],
            "author": {"id": 1, "name": "Nik"},
            "likes": [{"user_id": 1, "name": "Nik"}],
        },
        {
            "id": 3,
            "content": "tweet_test_1",
            "attachments": ["/api/medias/2"],
            "author": {"id": 4, "name": "test"},
            "likes": [],
        },
    ],
}

good_response_result: dict = {"result": True}

good_response_create_tweet: dict = {"result": True, "tweets_id": 4}

good_response_image_load: dict = {"result": True, "media_id": 4}
