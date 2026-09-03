from pathlib import Path
import argparse
import requests

class CollectElectricLoad:

    def __init__(self, years):
        self.years = years
        self.api_url = 'https://dados.ons.org.br/api/3/action/package_show'
        self.dataset_id = 'curva-carga'
        self.output_dir = Path('data/raw')

    def get_resources(self):
        response = requests.get(self.api_url, params = {'id': self.dataset_id}, timeout = 30)
        print(f'Status da API: {response.status_code}')

        response.raise_for_status()
        return response.json()['result']['resources']

    def find_resouce(self, resources, year):
        resource_name = f'CurvaCarga-{year}'

        for resource in resources:
            correct_name = resource['name'] == resource_name
            parquet_file = resource.get('format', '').upper() == 'PARQUET'

            if correct_name and parquet_file:
                return resource

        return None

    def save_data(self, data, year):
        file_path = self.output_dir / f'curva_carga_{year}.parquet'

        with open(file_path, 'wb') as file:
            file.write(data)

        return file_path

    def process(self, resources, year):
        file_path = self.output_dir / f'curva_carga_{year}.parquet'

        if file_path.exists():
            print(f'{year}: arquivo já existente.')
            return

        resource = self.find_resouce(resources, year)

        if resource is None:
            print(f'{year}: arquivo não foi encontrado.')

        response = requests.get(resource['url'], timeout = 60)
        response.raise_for_status()

        file_path = self.save_data(response.content, year)

        print(f'{year}: arquivo salvo em {file_path}')

    def process_years(self):
        resources = self.get_resources()

        for year in self.years:
            print(f'Coletando dados do ano {year}')
            self.process(resources, year)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--start', type = int, default = 2000)
    parser.add_argument('--stop', type = int, default = 2025)    
    parser.add_argument('--years', '-y', nargs = '+', type = int)

    args = parser.parse_args()

    if args.years:
        years = args.years
    else:
        years = list(range(args.start, args.stop + 1))

    collector = CollectElectricLoad(years)
    collector.process_years() 