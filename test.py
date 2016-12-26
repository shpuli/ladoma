import requests
import pytest
from jsonschema import validate

url = "http://apigw.lamoda.ru/json/get_product_product_recommendations"

schema = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["product"],
        "properties": {
            "product": {
                "type": "object",
                "required": ["sku"],
                "properties": {
                    "sku": { "type": "string" },
                }
            }
        }
    }
}

positive_data = [
    ('{"sku": "LO019EMJGZ27", "limit": 3}', 3, 'correct sku, limit = 3'),
    ('{"sku": "LO019EMJGZ27"}', 12, 'correct sku, default limit = 12'),
    ('{"sku": "LO019EMJGZ27", "limit": 100}', 100, 'correct sku, limit far more than we have')
]

@pytest.mark.parametrize("query,limit,conditions", positive_data)
def test_get_recomendations(query,limit,conditions):
    r = requests.post(url, query)
    assert r.status_code == 200, 'Wrong code ' + r.status_code + ' on ' + conditions
    assert validate(r.json(), schema) == None, 'Failed schema on ' + conditions
    assert validate(r.json(), {"maxItems": limit}) == None, 'Wrong limit on ' + conditions

def test_empty_sku():
    wrong_data = '{"sku": "", "limit": 3}'
    r = requests.post(url, wrong_data)
    assert r.status_code == 400, r.text
    assert r.json()["faultcode"] == "Client.ValidationError", 'Wrong err type'
    assert r.json()["faultstring"], 'No error message'