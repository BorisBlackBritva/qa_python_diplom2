import allure
import pytest
from helpers.constants import Constants
from helpers.helpers import GeneralHelpers, UserHelpers, OrderHelpers
from helpers.chekers import UserCheckers, GeneralCheckers, OrderCheckers


class TestLoginUser:

    help_user = UserHelpers()
    check_gen = GeneralCheckers()
    check_user = UserCheckers()

    @allure.title('Позитивная проверка логина пользователя')
    def test_login_user_success(self, create_and_del_user):

        response = self.help_user.login_user(create_and_del_user['accessToken'], create_and_del_user['payload'])

        assert self.check_user.success_auth_login_user_answer_checker(response, create_and_del_user['payload'])

    @allure.title('Негативная проверка логина пользователя:'
                  '- Левое мыло'
                  '- Левый пароль')
    @pytest.mark.parametrize('credential, value', [
        ['email', 'incorrect_email@incorrect.com'],
        ['password', 'incorrect_password']
    ])
    def test_login_with_incorrect_credentials_error(self, credential, value, create_and_del_user):

        create_and_del_user['payload'][credential] = value
        response = self.help_user.login_user(create_and_del_user['accessToken'], create_and_del_user['payload'])

        expected_body = {'success': False, 'message': 'email or password are incorrect'}
        assert self.check_gen.status_code_and_body_checker(response, 401, expected_body)

    @allure.title('Негативная проверка логина пользователя:'
                  '- Без мыла'
                  '- Без пароля')
    @pytest.mark.parametrize('key', ['email', 'password'])
    def test_login_with_not_fully_credentials_error(self, key, create_and_del_user):

        del create_and_del_user['payload'][key]
        response = self.help_user.login_user(create_and_del_user['accessToken'], create_and_del_user['payload'])

        expected_body = {'success': False, 'message': 'email or password are incorrect'}
        assert self.check_gen.status_code_and_body_checker(response, 401, expected_body)
