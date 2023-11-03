import requests
import pandas as pd


def get_point_wb():
    """Получение координат и id точек выдачи"""

    headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0",
               'content-type': "application/json",
               'x-requested-with': 'XMLHttpRequest'}

    pickup_resp = requests.get(url='https://static-basket-01.wb.ru/vol0/data/all-poo-fr-v8.json',
                               headers=headers)

    payload = f"{[pickup.get('id') for pickup in pickup_resp.json()[0].get('items')]}"

    response = requests.post(url="https://www.wildberries.ru/webapi/poo/byids",
                             data=payload, headers=headers)
    data = response.json()

    list_points = []
    for pickup in pickup_resp.json()[0].get('items'):
        point = {
            'lat': pickup.get('coordinates')[0],
            'lon': pickup.get('coordinates')[1],
            'adress': pickup.get('address'),
            'type': data.get('value').get(str(pickup.get('id'))).get('wayInfo')
        }
        list_points.append(point)

    df = pd.DataFrame(list_points)
    df.to_excel('test_result.xlsx')



def main():
    get_point_wb()



if __name__ == '__main__':
    main()
