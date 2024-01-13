import allure
from helpers.helpers import GeneralHelpers, UserHelpers, OrderHelpers
from helpers.chekers import UserCheckers, GeneralCheckers, OrderCheckers
from helpers.constants import Constants


class TestGetUsersOrder:

    help_order = OrderHelpers()
    const = Constants()
    check_gen = GeneralCheckers()
    check_order = OrderCheckers()

    @allure.title('Позитивная проверка получения заказа конкретного пользователя, с авторизацией')
    def test_get_users_order_with_auth_success(self, create_and_del_user, create_order):

        response = self.help_order.get_users_order(create_and_del_user['accessToken'])

        assert self.check_order.get_users_order_answer_checker(response, self.const.ORDERS['correct_order']['burger_name'])

    @allure.title('Негативная проверка получения заказа конкретного пользователя, без авторизации')
    def test_get_users_order_without_auth_error(self):

        response = self.help_order.get_users_order()

        assert self.check_gen.status_code_and_body_checker(response, 401, {'success': False, 'message': 'You should be authorised'})
