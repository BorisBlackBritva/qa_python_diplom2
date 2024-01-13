import allure
import pytest
from helpers.helpers import GeneralHelpers, UserHelpers, OrderHelpers
from helpers.chekers import UserCheckers, GeneralCheckers, OrderCheckers
from helpers.constants import Constants


class TestCreateUser:

    help_gen = GeneralHelpers()
    help_user = UserHelpers()
    const = Constants()
    check_gen = GeneralCheckers()
    check_user = UserCheckers()

    accessToken = None

    @allure.title('Позитивная проверка создания пользователя')
    def test_create_user_success(self):
        payload = self.help_gen.generate_random_user_credentials()

        response = self.help_user.create_user(payload)
        self.__class__.accessToken = response.json().get('accessToken')

        assert self.check_user.success_auth_login_user_answer_checker(response, payload)

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

        response = self.help_user.create_user(payload)

        assert self.check_gen.status_code_and_body_checker(response, 403, expected_body)

    @classmethod
    def teardown_class(cls):

        cls.help_user.del_user(cls.accessToken).json()
