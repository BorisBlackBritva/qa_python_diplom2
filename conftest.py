import pytest
import requests
from helpers.helpers import GeneralHelpers
from helpers.constants import Constants


@pytest.fixture
def create_and_del_user():

    help_gen = GeneralHelpers()
    payload = help_gen.generate_random_user_credentials()

    response_1 = requests.post('https://stellarburgers.nomoreparties.site/api/auth/register', json=payload)

    artefact = {
        'payload': payload,
        'accessToken': response_1.json().get('accessToken')
    }

    yield artefact

    response_2 = requests.delete('https://stellarburgers.nomoreparties.site/api/auth/user',
                               headers={
                                   'authorization': response_1.json().get('accessToken')
                               }
                               )


@pytest.fixture
def create_order(create_and_del_user):

    const = Constants()

    response = requests.post('https://stellarburgers.nomoreparties.site/api/orders',
                             headers={
                                 'authorization': create_and_del_user['accessToken']
                             },
                             json=const.ORDERS['correct_order']['payload'])

