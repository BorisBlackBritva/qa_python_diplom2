import allure
import pytest
from helpers.helpers import Helpers, Checkers


class TestLoginUser:

    help = Helpers()
    check = Checkers()

    credentials = None
    accessToken = None

    @classmethod
    def setup_class(cls):

        cls.credentials = cls.help.generate_random_user_credentials()
        response = cls.help.create_user(cls.credentials)
        cls.accessToken = response.json().get('accessToken')

    @allure.title('Позитивная проверка логина пользователя')
    def test_login_user_success(self):

        response = self.help.login_user(self.accessToken, self.credentials)

        assert self.check.success_auth_login_user_answer_checker(response, self.credentials)

    @allure.title('Негативная проверка логина пользователя:'
                  '- Левое мыло'
                  '- Левый пароль')
    @pytest.mark.parametrize('credential, value', [
        ['email', 'incorrect_email@incorrect.com'],
        ['password', 'incorrect_password']
    ])
    def test_login_with_incorrect_credentials_error(self, credential, value):

        self.credentials[credential] = value
        response = self.help.login_user(self.accessToken, self.credentials)

        expected_body = {'success': False, 'message': 'email or password are incorrect'}
        assert self.check.status_code_and_body_checker(response, 401, expected_body)

    @allure.title('Негативная проверка логина пользователя:'
                  '- Без мыла'
                  '- Без пароля')
    @pytest.mark.parametrize('key', ['email', 'password'])
    def test_login_with_not_fully_credentials_error(self, key):

        del self.credentials[key]
        response = self.help.login_user(self.accessToken, self.credentials)

        expected_body = {'success': False, 'message': 'email or password are incorrect'}
        assert self.check.status_code_and_body_checker(response, 401, expected_body)

    @classmethod
    def teardown_class(cls):

        cls.help.del_user(cls.accessToken).json()
