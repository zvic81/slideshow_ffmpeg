# for test put in console pytest -s -v -m app
# need installed pytest to venv!!!

import pytest
import sys
import os.path
from apiflask import APIFlask
app_dir = (os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..')) + '/srs/')
sys.path.append(app_dir)
from routes import configure_routes
import schemas


@pytest.fixture
def config_apllication():
    app = APIFlask(__name__)
    configure_routes(app)
    app.url_map.strict_slashes = False  # open /goods/ as /goods
    app.config['DESCRIPTION'] = 'RestAPI server with Apiflask and postgresql'
    app.config['BASE_RESPONSE_SCHEMA'] = schemas.BaseResponse
    app.config['BASE_RESPONSE_DATA_KEY '] = 'data'
    client = app.test_client()
    return client


@pytest.mark.app
def test_base_route(config_apllication):
    url = '/'
    response = config_apllication.get(url)
    assert response.status_code == 302  # test redirect to localhost:5000/docs"
    url = '/docs'
    response = config_apllication.get(url)
    assert response.status_code == 200  # test request swagger interface


@pytest.mark.app
def test_get_route(config_apllication):
    url = '/goods'
    response = config_apllication.get(url)
    assert response.status_code == 200


@pytest.mark.app
def test_post_delete_route_success(config_apllication):
    url = '/goods'
    mock_request_data = {'name': 'funtass', 'manufacture_date': '2019-02-05',
                         'price': 21, 'picture_url': 'pic.com/mypic.jpg', }
    response = config_apllication.post(url, json=mock_request_data)
    assert response.status_code == 201, pprint(response.get_data())
    assert isinstance(response.get_json(), dict)
    id = response.get_json()['data']['id']
    url = '/goods/' + str(id)
    response = config_apllication.delete(url)
    assert response.status_code == 204


# test if server get failure for not correct json
@pytest.mark.app
def test_post_route_failure(config_apllication):
    url = '/goods'
    mock_request_data = {'names': 'funta', 'manufacture_date': '2019-02-05',
                         'price': 21, 'picture_url': 'pic.com/mypic.jpg', }
    response = config_apllication.post(url, json=mock_request_data)
    assert response.status_code == 400, pprint(response.get_data())


@pytest.mark.app
def test_get_orders_route(config_apllication):
    url = '/orders'
    response = config_apllication.get(url)
    assert response.status_code == 200
