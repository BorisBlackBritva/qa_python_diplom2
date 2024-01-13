import string
import random
import allure
import requests
from helpers.constants import Constants


class GeneralHelpers:

    @allure.step('Создаем рандомные креды для пользователя')
    def generate_random_user_credentials(self):
        def generate_random_string(length):
            letters = string.ascii_lowercase
            random_string = ''.join(random.choice(letters) for i in range(length))
            return random_string

        email = f'{generate_random_string(10)}@{generate_random_string(10)}.com'
        password = generate_random_string(10)
        name = generate_random_string(10)

        payload = {
            "email": email,
            "password": password,
            "name": name
        }

        return payload


class UserHelpers:

    const = Constants()

    @allure.step('Создаем пользователя')
    def create_user(self, payload):
        response = requests.post(self.const.URLS['user']['create'], json=payload)

        return response

    @allure.step('Удаляем пользователя')
    def del_user(self, accessToken):
        response = requests.delete(self.const.URLS['user']['change_del'],
                                   headers={
                                       'authorization': accessToken
                                   }
                                   )

        return response

    @allure.step('Логиним пользователя')
    def login_user(self, accessToken, payload):
        response = requests.post(self.const.URLS['user']['login'], json=payload,
                                 headers={
                                     'authorization': accessToken
                                 }
                                 )

        return response

    @allure.step('Обновляем пользователя')
    def update_user(self, accessToken, payload):
        response = requests.patch(self.const.URLS['user']['change_del'], json=payload,
                                  headers={
                                      'authorization': accessToken
                                  }
                                  )

        return response


class OrderHelpers:

    const = Constants()

    @allure.step('Создаем заказ')
    def create_order(self, accessToken=None, payload=None):

        if accessToken:

            response = requests.post(self.const.URLS['order']['all'],
                                     headers={
                                         'authorization': accessToken
                                     },
                                     json=payload)

        else:
            response = requests.post(self.const.URLS['order']['all'], json=payload)

        return response

    @allure.step('Получаем заказ конкретного пользователя')
    def get_users_order(self, accessToken=None):

        response = requests.get(self.const.URLS['order']['all'], headers={
            'authorization': accessToken
        })

        return response
