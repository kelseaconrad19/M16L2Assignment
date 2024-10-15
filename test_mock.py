import json
import pytest
from new_app import new_app

@pytest.fixture
def client():
    new_app.config["TESTING"] = True
    with new_app.test_client() as client:
        yield client

def test_home(client, mocker):
    payload = {'num1': 2, 'num2': 3}
    mocker.patch.object(client, 'post', return_value=new_app.response_class(
        response=json.dumps({'result': 5}),
        status=200,
        mimetype='application/json'
    ))

    response = client.get('/sum', json=payload)
    data = response.get_json()
    assert data['result'] == 5

if __name__ == '__main__':
    pytest.main([__file__])