from io import BytesIO
import requests
from PIL import Image
import sys


def map_scale(top):
    low = list(map(float, top['boundedBy']['Envelope']['lowerCorner'].split()))
    up = list(map(float, top['boundedBy']['Envelope']['upperCorner'].split()))
    return str(max(abs(low[0] - up[0]) * 1.5, abs(low[1] - up[1]) * 1.5))


api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
search_api_server = "https://search-maps.yandex.ru/v1/"

map_api_server = "http://static-maps.yandex.ru/1.x/"
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
toponym_to_find = " ".join(sys.argv[1:])
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}
response = requests.get(geocoder_api_server, params=geocoder_params)
if not response:
    pass
json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
address_ll = ','.join(toponym_coodrinates.split())
search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
if not response:
    pass

json_response = response.json()

# Получаем первую найденную организацию.
organization = json_response["features"]
if len(organization) > 10:
    organization = organization[:10]

result = [f'{address_ll},ya_ru']

for o in organization:
    if 'Hours' in o["properties"]['CompanyMetaData'].keys():
        if 'круглосуточно' in o["properties"]['CompanyMetaData']['Hours']['text']:
            result.append(f"{','.join(list(map(str, o['geometry']['coordinates'])))},pm2gnm")
        else:
            result.append(f"{','.join(list(map(str, o['geometry']['coordinates'])))},pm2blm")
    else:
        result.append(f"{','.join(list(map(str, o['geometry']['coordinates'])))},pmgns")

delta = map_scale(toponym)



map_params = {
    "ll": address_ll,
    "spn": ",".join([delta, delta]),
    "l": "map",
    "pt": '~'.join(result)
}
response = requests.get(map_api_server, params=map_params)
Image.open(BytesIO(
    response.content)).show()
