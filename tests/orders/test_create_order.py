import allure
from helpers.helpers import GeneralHelpers, UserHelpers, OrderHelpers
from helpers.chekers import UserCheckers, GeneralCheckers, OrderCheckers
from helpers.constants import Constants


class TestCreateOrder:

    help_order = OrderHelpers()
    const = Constants()
    check_gen = GeneralCheckers()
    check_order = OrderCheckers()

    @allure.title('Позитивная проверка создания заказа, без авторизации')
    def test_create_order_without_auth_success(self):

        response = self.help_order.create_order(payload=self.const.ORDERS['correct_order']['payload'])

        assert self.check_order.success_create_order_answer_checker(response, self.const.ORDERS['correct_order']['burger_name'])

    @allure.title('Позитивная проверка создания заказа, с авторизацией')
    def test_create_order_with_auth_success(self, create_and_del_user):

        response = self.help_order.create_order(create_and_del_user['accessToken'], self.const.ORDERS['correct_order']['payload'])

        assert self.check_order.success_create_order_answer_checker(response, self.const.ORDERS['correct_order']['burger_name'], True)

    @allure.title('Негативная проверка создания заказа, без ингредиентов')
    def test_create_order_without_ingredients_error(self):

        response = self.help_order.create_order(payload=self.const.ORDERS['without_ingredients']['payload'])

        assert self.check_gen.status_code_and_body_checker(response, 400, {'success': False, 'message': 'Ingredient ids must be provided'})

    @allure.title('Негативная проверка создания заказа, с кривым хешем ингредиентов')
    def test_create_order_incorrect_ingredients_hash_error(self):

        response = self.help_order.create_order(payload=self.const.ORDERS['incorrect_ingredients_hash']['payload'])

        assert response.status_code == 500
