import requests

API_URL = 'https://dados.ons.org.br/api/3/action/package_show'
DATASET_ID = 'curva-carga'

response = requests.get(API_URL, params = {'id': DATASET_ID}, timeout = 30)
print(f'Status da API: {response.status_code}')

response.raise_for_status()

dataset = response.json()['result']

print(f'Dataset: {dataset['title']}')
print(f'Quantidade de recursos: {len(dataset['resources'])}\n')

for resource in dataset['resources'][:10]:
    print(resource['name'], resource.get('format'), resource['url'])