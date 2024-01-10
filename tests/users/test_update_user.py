import allure
from helpers.helpers import Helpers, Checkers
from helpers.constants import Constants


class TestUpdateUser:

    help = Helpers()
    const = Constants()
    check = Checkers()

    credentials = None
    accessToken = None

    @classmethod
    def setup_class(cls):

        cls.credentials = cls.help.generate_random_user_credentials()
        response = cls.help.create_user(cls.credentials)
        cls.accessToken = response.json().get('accessToken')

    @allure.title('Проверка обновления пользователя с авторизацией')
    def test_update_user_success(self):

        new_credentials = self.help.generate_random_user_credentials()
        response = self.help.update_user(self.accessToken, new_credentials)

        assert self.check.update_user_answer_checker(response, new_credentials)

    @allure.title('Проверка обновления пользователя без авторизациии')
    def test_update_user_success(self):
        new_credentials = self.help.generate_random_user_credentials()
        response = self.help.update_user('', new_credentials)

        assert self.check.status_code_and_body_checker(response, 401, {'success': False, 'message': 'You should be authorised'})

    @classmethod
    def teardown_class(cls):

        cls.help.del_user(cls.accessToken).json()
