import random
import allure


class GeneralCheckers:

    @allure.step('Проверяем статус код и тело ответа')
    def status_code_and_body_checker(self, response, expected_status_code, expected_body):

        if response.json() == expected_body and response.status_code == expected_status_code:

            return True

        elif response.json() != expected_body or response.status_code == expected_status_code:

            raise AssertionError(
                f'Actual status.code {response.status_code} != expected {expected_status_code} or\\and \n'
                f'Actual response.json {response.json()} != expected {expected_body}')


class UserCheckers:

    @allure.step('Проверяем код ответа и тело при логине или создании пользователя')
    def success_auth_login_user_answer_checker(self, response, credentials):
        try:
            status_code_bool = response.status_code == 200
            success_in_body_bool = response.json().get('success') == True
            user_in_body_bool = response.json().get('user') == {'email': credentials['email'],
                                                                'name': credentials['name']}
            accessToken_in_body_bool = (response.json().get('accessToken').startswith('Bearer') and
                                        len(response.json().get('accessToken')) == 178)
            refreshToken_in_body_bool = len(response.json().get('refreshToken')) == 80
        except [ValueError, AttributeError]:
            pass
        finally:
            if (status_code_bool and success_in_body_bool and user_in_body_bool and accessToken_in_body_bool
                    and refreshToken_in_body_bool):
                return True
            else:
                raise AssertionError(
                    f"Actual status_code {response.status_code} != expected 200 \n"
                    "or \n"
                    f"Actual body {response.json()} != expected body "
                    f"{{'success': True, 'user': {{'email': {credentials['email']}, 'name': {credentials['name']}}}, "
                    f"'accessToken': response.json()['accessToken'].startswith('Bearer') "
                    f"and len(response.json()['accessToken']) == 178, "
                    f"'refreshToken': len(response.json()['refreshToken']) == 80}}"
                )

    @allure.step('Проверяем код ответа и тело при апдейте пользователя')
    def update_user_answer_checker(self, response, credentials):
        try:
            status_code_bool = response.status_code == 200
            success_in_body_bool = response.json().get('success') == True
            user_in_body_bool = response.json().get('user') == {'email': credentials['email'],
                                                                'name': credentials['name']}
        except [ValueError, AttributeError]:
            pass
        finally:
            if (status_code_bool and success_in_body_bool and user_in_body_bool):
                return True
            else:
                raise AssertionError(
                    f"Actual status_code {response.status_code} != expected 200 \n"
                    "or \n"
                    f"Actual body {response.json()} != expected body "
                    f"{{'success': True, 'user': {{'email': {credentials['email']}, 'name': {credentials['name']}}}"
                )


class OrderCheckers:

    @allure.step('Проверяем статус код и тело ответа при создании заказа с авторизацией или без')
    def success_create_order_answer_checker(self, response=None, burger_name=None, auth=False):

        exceptions = []

        try:
            status_code_bool = response.status_code == 200
            success_bool = response.json().get('success')
            name_bool = response.json().get('name') == burger_name
            order_number_bool = type(response.json().get('order').get('number')) == int

        except AssertionError:
            pass

        try:
            if status_code_bool and success_bool and name_bool and order_number_bool:
                pass

            else:
                raise AssertionError(
                    f"Actual status_code {response.status_code} != expected 200 \n"
                    f"or \n "
                    f"Actual success field {response.json().get('success')} != True \n"
                    f"or \n "
                    f"Actual burger_name field {response.json().get('name')} != {burger_name} \n"
                    f"or \n "
                    f"Actual number field type {type(response.json().get('order').get('number'))} != int \n"
                )

        except AssertionError as error:
            exceptions.append(error)

        if auth:
            expected_body_fields_types = {
                "first_lvl_fields": {
                    "success": bool,
                    "order": dict
                },
                "order_fields": {
                    "ingredients": list,
                    "_id": str,
                    "owner": dict,
                    "status": str,
                    "name": str,
                    "createdAt": str,
                    "updatedAt": str,
                    "number": int,
                    "price": int
                },
                "ingredients_fields": {
                    "_id": str,
                    "name": str,
                    "type": str,
                    "proteins": int,
                    "fat": int,
                    "carbohydrates": int,
                    "calories": int,
                    "price": int,
                    "image": str,
                    "image_mobile": str,
                    "image_large": str,
                    "__v": int
                },
                "owner_fields": {
                    "name": str,
                    "email": str,
                    "createdAt": str,
                    "updatedAt": str
                }
            }

            for first_lvl_field in expected_body_fields_types:

                if first_lvl_field == 'first_lvl_fields':

                    for field in expected_body_fields_types['first_lvl_fields']:

                        try:
                            if (type(response.json().get(field))
                                    == expected_body_fields_types.get('first_lvl_fields').get(field)
                                    and (response.json().get(field)
                                         or response.json().get(field) == 0)):

                                continue

                            else:

                                raise AssertionError(
                                    f"Actual field \"{field}\" type {type(response.json().get(field))} != "
                                    f"expected field \"{field}\" type {expected_body_fields_types.get('first_lvl_fields').get(field)} "
                                    f"or "
                                    f"Field is empty")

                        except AssertionError as error:
                            exceptions.append(error)
                            continue

                elif first_lvl_field == 'order_fields':

                    for field in expected_body_fields_types['order_fields']:

                        try:

                            if (type(response.json().get('order').get(field))
                                    == expected_body_fields_types.get('order_fields').get(field)
                                    and (response.json().get('order').get(field)
                                         or response.json().get('order').get(field) == 0)):

                                continue

                            else:

                                raise AssertionError(
                                    f"Actual field \"{field}\" type {type(response.json().get('order').get(field))} != "
                                    f"expected field \"{field}\" type {expected_body_fields_types.get('order_fields').get(field)} "
                                    f"or "
                                    f"Field is empty")

                        except AssertionError as error:
                            exceptions.append(error)
                            continue

                elif first_lvl_field == 'ingredients_fields':

                    for field in expected_body_fields_types['ingredients_fields']:

                        try:

                            n = random.randint(0, len(response.json().get('order').get('ingredients')) - 1)

                            if (type(response.json().get('order').get('ingredients')[n].get(field))
                                    == expected_body_fields_types.get('ingredients_fields').get(field)
                                    and (response.json().get('order').get('ingredients')[n].get(field)
                                         or response.json().get('order').get('ingredients')[n].get(field) == 0)):

                                continue

                            else:

                                raise AssertionError(
                                    f"Actual field \"{field}\" type {type(response.json().get('order').get('ingredients')[n].get(field))} != "
                                    f"expected field \"{field}\" type {expected_body_fields_types.get('ingredients_fields').get(field)} "
                                    f"or "
                                    f"Field is empty")

                        except AssertionError as error:

                            exceptions.append(error)
                            continue

                elif first_lvl_field == 'owner_fields':

                    try:

                        for field in expected_body_fields_types['owner_fields']:

                            if (type(response.json().get('order').get('owner').get(field))
                                    == expected_body_fields_types.get('owner_fields').get(field)
                                    and (response.json().get('order').get('owner').get(field)
                                         or response.json().get('order').get('owner').get(field) == 0)):

                                continue

                            else:

                                raise AssertionError(
                                    f"Actual field \"{field}\" type {type(response.json().get('order').get('owner').get(field))} != "
                                    f"expected field \"{field}\" type {expected_body_fields_types.get('owner_fields').get(field)} "
                                    f"or "
                                    f"Field is empty")

                    except AssertionError as error:
                        exceptions.append(error)
                        continue

        if exceptions:

            for exception in exceptions:
                print(exception)

        else:
            return True

    @allure.step('Проверяем статус код и тело ответа при получении заказа конкретного пользователя')
    def get_users_order_answer_checker(self, response, burger_name):

        exceptions = []
        n = random.randint(0, len(response.json().get('orders')) - 1)

        try:
            status_code_bool = response.status_code == 200
            success_bool = response.json().get('success')
            name_bool = response.json().get('orders')[n].get('name') == burger_name

        except AssertionError:
            pass

        try:
            if status_code_bool and success_bool and name_bool:
                pass

            else:
                raise AssertionError(
                    f"Actual status_code {response.status_code} != expected 200 \n"
                    f"or \n "
                    f"Actual success field {response.json().get('success')} != True \n"
                    f"or \n "
                    f"Actual burger_name field {response.json().get('name')} != {burger_name} \n"
                )

        except AssertionError as error:
            exceptions.append(error)

        expected_body_fields_types = {
            "first_lvl_fields": {
                "success": bool,
                "orders": list,
                "total": int,
                "totalToday": int
            },
            "order_fields": {
                "_id": str,
                "ingredients": list,
                "status": str,
                "name": str,
                "createdAt": str,
                "updatedAt": str,
                "number": int
            }
        }

        for first_lvl_field in expected_body_fields_types:

            if first_lvl_field == 'first_lvl_fields':

                for field in expected_body_fields_types['first_lvl_fields']:

                    try:
                        if (type(response.json().get(field))
                                == expected_body_fields_types.get('first_lvl_fields').get(field)
                                and (response.json().get(field)
                                     or response.json().get(field) == 0)):

                            continue

                        else:

                            raise AssertionError(
                                f"Actual field \"{field}\" type {type(response.json().get(field))} != "
                                f"expected field \"{field}\" type {expected_body_fields_types.get('first_lvl_fields').get(field)} "
                                f"or "
                                f"Field is empty")

                    except AssertionError as error:
                        exceptions.append(error)
                        continue

            elif first_lvl_field == 'order_fields':

                for field in expected_body_fields_types['order_fields']:

                    try:

                        if (type(response.json().get('orders')[n].get(field))
                                == expected_body_fields_types.get('order_fields').get(field)
                                and (response.json().get('orders')[n].get(field)
                                     or response.json().get('orders')[n].get(field) == 0)):

                            continue

                        else:

                            raise AssertionError(
                                f"Actual field \"{field}\" type {type(response.json().get('orders')[n].get(field))} != "
                                f"expected field \"{field}\" type {expected_body_fields_types.get('order_fields').get(field)} "
                                f"or "
                                f"Field is empty")

                    except AssertionError as error:

                        exceptions.append(error)
                        continue

        if exceptions:

            for exception in exceptions:
                print(exception)

        else:
            return True