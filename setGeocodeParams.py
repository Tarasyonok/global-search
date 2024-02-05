import requests


def search(geokode):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": geokode,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        # обработка ошибочной ситуации
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    toponym_lower = list(map(float, toponym["boundedBy"]["Envelope"]["lowerCorner"].split()))
    toponym_upper = list(map(float, toponym["boundedBy"]["Envelope"]["upperCorner"].split()))

    x_spn = abs(toponym_upper[0] - toponym_lower[0])
    y_spn = abs(toponym_upper[1] - toponym_lower[1])

    delta = str(max(x_spn, y_spn))

    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "l": "map",
        "pt": ",".join([toponym_longitude, toponym_lattitude]),
    }

    return map_params
