

class Constants:

    USERS = {
        "already_exist": {
            "email": "test-data@yandex.ru",
            "password": "password",
            "name": "Username"
        },
        "without_email": {
            "password": "password",
            "name": "Username"
        },
        "without_pass": {
            "email": "test-data@yandex.ru",
            "name": "Username"
        },
        "without_name": {
            "email": "test-data@yandex.ru",
            "password": "password"
        }
    }

    ORDERS = {
        'correct_order': {
            "burger_name": 'Альфа-сахаридный традиционный-галактический бургер',
            "payload": {
                "ingredients": ["61c0c5a71d1f82001bdaaa78", "61c0c5a71d1f82001bdaaa74"]
            }
        },
        'incorrect_ingredients_hash': {
            "payload": {
                "ingredients": ["61c0c5a71d1f82001bdaaa78123", "61c0c5a71d1f82001bdaaa74123"]
            }
        },
        'without_ingredients': {
            "payload": {
                "ingredients": []
            }
        }
    }
