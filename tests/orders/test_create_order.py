import allure
from helpers.helpers import Helpers, Checkers
from helpers.constants import Constants


class TestCreateOrder:

    help = Helpers()
    const = Constants()
    check = Checkers()

    accessToken = None

    @classmethod
    def setup_class(cls):

        credentials = cls.help.generate_random_user_credentials()
        response = cls.help.create_user(credentials)
        cls.accessToken = response.json().get('accessToken')

    @allure.title('Позитивная проверка создания заказа, без авторизации')
    def test_create_order_without_auth_success(self):

        response = self.help.create_order(payload=self.const.ORDERS['correct_order']['payload'])

        assert self.check.success_create_order_answer_checker(response, self.const.ORDERS['correct_order']['burger_name'])

    @allure.title('Позитивная проверка создания заказа, с авторизацией')
    def test_create_order_with_auth_success(self):

        response = self.help.create_order(self.accessToken, self.const.ORDERS['correct_order']['payload'])

        assert self.check.success_create_order_answer_checker(response, self.const.ORDERS['correct_order']['burger_name'], True)

    @allure.title('Негативная проверка создания заказа, без ингредиентов')
    def test_create_order_without_ingredients_error(self):

        response = self.help.create_order(payload=self.const.ORDERS['without_ingredients']['payload'])

        assert self.check.status_code_and_body_checker(response, 400, {'success': False, 'message': 'Ingredient ids must be provided'})

    @allure.title('Негативная проверка создания заказа, с кривым хешем ингредиентов')
    def test_create_order_incorrect_ingredients_hash_error(self):

        response = self.help.create_order(payload=self.const.ORDERS['incorrect_ingredients_hash']['payload'])

        assert response.status_code == 500

    @classmethod
    def teardown_class(cls):

        cls.help.del_user(cls.accessToken).json()
