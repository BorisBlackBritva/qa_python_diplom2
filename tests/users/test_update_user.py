import allure
from helpers.helpers import GeneralHelpers, UserHelpers, OrderHelpers
from helpers.chekers import UserCheckers, GeneralCheckers, OrderCheckers


class TestUpdateUser:

    help_gen = GeneralHelpers()
    help_user = UserHelpers()
    check_gen = GeneralCheckers()
    check_user = UserCheckers()

    @allure.title('Проверка обновления пользователя с авторизацией')
    def test_update_user_success(self, create_and_del_user):

        new_credentials = self.help_gen.generate_random_user_credentials()
        response = self.help_user.update_user(create_and_del_user['accessToken'], new_credentials)

        assert self.check_user.update_user_answer_checker(response, new_credentials)

    @allure.title('Проверка обновления пользователя без авторизации')
    def test_update_user_error(self):

        new_credentials = self.help_gen.generate_random_user_credentials()
        response = self.help_user.update_user('', new_credentials)

        assert self.check_gen.status_code_and_body_checker(response, 401, {'success': False, 'message': 'You should be authorised'})
