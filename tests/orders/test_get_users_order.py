import allure
from helpers.helpers import Helpers, Checkers
from helpers.constants import Constants


class TestGetUsersOrder:

    help = Helpers()
    const = Constants()
    check = Checkers()

    accessToken = None

    @classmethod
    def setup_class(cls):

        cls.credentials = cls.help.generate_random_user_credentials()
        response = cls.help.create_user(cls.credentials)
        cls.accessToken = response.json().get('accessToken')
        cls.help.create_order(cls.accessToken, cls.const.ORDERS['correct_order']['payload'])

    @allure.title('Позитивная проверка получения заказа конкретного пользователя, с авторизацией')
    def test_get_users_order_with_auth_success(self):

        response = self.help.get_users_order(self.accessToken)

        assert self.check.get_users_order_answer_checker(response, self.const.ORDERS['correct_order']['burger_name'])

    @allure.title('Негативная проверка получения заказа конкретного пользователя, без авторизации')
    def test_get_users_order_without_auth_error(self):

        response = self.help.get_users_order()

        assert self.check.status_code_and_body_checker(response, 401, {'success': False, 'message': 'You should be authorised'})

    @classmethod
    def teardown_class(cls):

        cls.help.del_user(cls.accessToken).json()
