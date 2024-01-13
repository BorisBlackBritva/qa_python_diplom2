

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

    MAIN_URL = 'https://stellarburgers.nomoreparties.site/api'

    URLS = {
        'user': {
            'create': f'{MAIN_URL}/auth/register',
            'change_del': f'{MAIN_URL}/auth/user',
            'login': f'{MAIN_URL}/auth/login'
        },
        'order': {
            'all': f'{MAIN_URL}/orders'
        }
    }
