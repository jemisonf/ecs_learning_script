import configparser

import requests

HOST_DEFAULT = 'api.oregonstate.edu'


class ConfigHelper:
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_access_token(self):
        if 'credentials' not in self.config:
            raise 'config file does not include credentials'
        credentials = self.config['credentials']

        try:
            client_id = credentials['client_id']
            client_secret = credentials['client_secret']
        except KeyError:
            raise ('credentials section does not contain'
                   ' client_id or client_secret')

        params = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials',
        }
        res = requests.post(
            f'{self.get_host_url()}oauth2/token', params)
        res.raise_for_status()

        data = res.json()

        if 'access_token' in data:
            return data['access_token']
        else:
            raise 'returned JSON data does not include access_token value'

    def get_host_url(self):
        try:
            host = self.config['api']['host']
        except KeyError:
            host = HOST_DEFAULT
        return f'https://{host}/'


if __name__ == '__main__':
    config_helper = ConfigHelper('config.ini')
    print(config_helper.get_access_token(), end='')
