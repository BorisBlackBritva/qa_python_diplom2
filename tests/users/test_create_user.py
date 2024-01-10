import allure
import pytest
from helpers.helpers import Helpers, Checkers
from helpers.constants import Constants


class TestCreateUser:

    help = Helpers()
    const = Constants()
    check = Checkers()

    accessToken = None

    @allure.title('Позитивная проверка создания пользователя')
    def test_create_user_success(self):
        payload = self.help.generate_random_user_credentials()

        response = self.help.create_user(payload)
        self.__class__.accessToken = response.json().get('accessToken')

        assert self.check.success_auth_login_user_answer_checker(response, payload)

    allure.title('Негативная проверка создания пользователя:'
                 '- Уже сущ-ющий пользователь'
                 '- Без имейла'
                 '- Без пароля'
                 '- Без имени')
    @pytest.mark.parametrize('payload, expected_body', [
        [const.USERS['already_exist'], {'success': False, 'message': 'User already exists'}],
        [const.USERS['without_email'], {'success': False, 'message': 'Email, password and name are required fields'}],
        [const.USERS['without_pass'], {'success': False, 'message': 'Email, password and name are required fields'}],
        [const.USERS['without_name'], {'success': False, 'message': 'Email, password and name are required fields'}]
    ])
    def test_create_user_error(self, payload, expected_body):

        response = self.help.create_user(payload)

        assert self.check.status_code_and_body_checker(response, 403, expected_body)

    @classmethod
    def teardown_class(cls):

        cls.help.del_user(cls.accessToken).json()
