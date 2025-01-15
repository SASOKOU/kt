import requests
import matplotlib.pyplot as plt
import pandas as pd


headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie': '_pk_id.2.b001=76bc16c875955df4.1736323930.; _pk_ses.2.b001=1',
    'origin': 'https://www.e-stat.go.jp',
    'priority': 'u=1, i',
    'referer': 'https://www.e-stat.go.jp/dbview?sid=0003281493',
    'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
    'x-requested-with': 'XMLHttpRequest',
}

params = (
    ('sid', '0003281493'),
)

data = {
  'rows': 'H4sIAAAAAAAAA5XSu2rcUBSF4Xc5tYp9JO2LVIYY4mLczDTGmEHxqBBoLmRkCBi/VRo/kN/DZxIGnFV5qRKbs/7qe3hJ+2FZxl+3u9TXVVqGn/N4N+zH1KfVj+1mdV+vv9lWRLKIRZdTlXbT+bT59G59fdLUkduu2W5uVzfl3el4npbpeLh73qc+V2mezsv3YRlS//CSDv+2teR4f/tTXj8dd9eD/P3K7fkwLeVW/sbfp3k4DJfc5fBafS44FpwtGBaMLSgWlC20WGjZQoOFhi3UWKjZQsZCZguCBSEL0kFBOraAJoU1KWhSWJOCJoU1KWhSWJOCJoU1KWhSWJOCJoU1KWhSWJOCJq/fFwu56/43eTmwhcACZ7IMHAucyTIwLHAmy0CxwJksgxYLnMkyaLDAmSyDGgucyTLIWOBMloFggTUZaDJYk4EmgzUZaDJYk4EmgzUZaDJYk4EmgzUZaDJYk4EmgzUZaDJYk4EmgzXpaNJZk44mnTXpaNJZk44mnTXpaNJZk44mnTXpaNJZk44mnTXpaNJZk44mnTVpaNJYk4YmjTVpaNJYk4YmjTVpaNJYk4YmjTVpaNJYk4YmjTVpaNJYk4YmjTWpaFJZk4omlTWpaFJZk4omlTWpaFJZk4omlTWpaFJZk4omlTWpaFJZk4omlTXZosmWNdmiyfYrJh+rNMzzepzHp2XcpT6/Pn4AJ/xLm9cSAAA=',
  'cols': 'H4sIAAAAAAAAA4uuVspNLClJLfJMUbIytNBRKklMykn1S8xNVbJS8vWI9wg2CnYyizeAAUMlHaWUzOKCECRlcCXGRhaGJpbGQE1AVQX5xZklmfl5fqW5QJN1lHIyi0tcEksSlayiq5XyIDqfz9z1fMr8J7u3PZu6AaglOT8FJGpoYGgA5JXmZZYAeUBZICe1oiAnMS8RZCBQTKlWB6sZ8c/W7n6ya+GTXd3PprYiG2hGgoEvNi142rT9RUMrqqMMLZHN2LULrxlAd2AYYGROggFA+af9iw0NnuxoBzH3Tn7cOP9xUxc2c43NCJobq6OUmJMTnJqTmlySCoro2lgAoYtMxvkBAAA=',
  'tops': 'H4sIAAAAAAAAA4uOBQApu0wNAgAAAA==',
  'apiTops': 'H4sIAAAAAAAAA4uOBQApu0wNAgAAAA==',
  'annotationFlg': '1',
  'rowNoDataDispFlg': '0',
  'colNoDataDispFlg': '0',
  'commaType': '0',
  'replaceSpChars': '0',
  'graphAxis': 'horizontal',
  'graphBasis': 'head',
  'graphSort': 'asc',
  'graphTitle': '',
  'graphType': 'barChart',
  'inputNumberOfCols': '100',
  'inputNumberOfRows': '100',
  'movementId': '0',
  'leftMoveFlg': '0',
  'rightMoveFlg': '0',
  'underMoveFlg': '0',
  'upMoveFlg': '0',
  'currentCols': '',
  'currentRows': '',
  'mode': 'table',
  'layoutName': ''
}

response = requests.post('https://www.e-stat.go.jp/dbview/api_get_result', headers=headers, params=params, data=data)
jsondata = response.json()
table = jsondata['table']
df = pd.read_html(table)[0]
df.rename(columns={'Unnamed: 0':'年份'},inplace=True)
df.to_csv('data.csv',index=False,encoding='utf-8-sig')


file_path = 'data.csv'  
data = pd.read_csv(file_path)


data['年份'] = data['年份'].str.extract('(\d+)').astype(int)


plt.figure(figsize=(10, 6))
plt.plot(data['年份'], data['発生件数 【件】'], label='Total Accidents', marker='o')
plt.plot(data['年份'], data['発生件数_死亡事故 【件】'], label='Fatal Accidents', marker='o')
plt.plot(data['年份'], data['負傷者数 【人】'], label='Injuries', marker='o')
plt.plot(data['年份'], data['死者数 【人】'], label='Fatalities', marker='o')

plt.title('Traffic Accident Trends', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True)
plt.tight_layout()


plt.savefig('trend_chart_en.png')  
plt.show()
print('根据グラフの情報に基づく分析結果として、経済バブルの膨張期に日本の民間の自動車保有量が確かに増加し始めたが、この成長は適切な交通インフラや法律・規制のタイムリーな更新とサポートを受けられていなかった。この不均衡が交通事故の件数と死亡率の上昇を引き起こした。さらに、法規の変更と人々の新しい交通規則への適応にも時間が必要であり、このプロセスでの遅れが事故の重大さを悪化させる可能性がある')
