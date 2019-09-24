import argparse
import json
import sys

import requests

from config_helper import ConfigHelper

DEFAULT_CONFIG_FILE = 'config.ini'


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_file', action='store',
                        dest='config_file', default=DEFAULT_CONFIG_FILE,
                        help=('the name of the config file to read from,'
                              ' ie `config.ini`'))

    filters = parser.add_argument_group('filters')
    filters.add_argument('--parking-zone', action='store',
                         help=('search for buildings in'
                               ' parking zone PARKING_ZONE'))
    filters.add_argument('--building-id', action='store',
                         help='find the building with ID BUILDING_ID')
    filters.add_argument('--campus', action='store',
                         help='search for buildings located in campus CAMPUS')
    filters.add_argument('--gi-restrooms', action='store_true',
                         help=('search for building with'
                               ' gender inclusive restrooms'))
    filters.add_argument('--query', action='store',
                         help='search for locations using query QUERY')

    args = parser.parse_args(sys.argv[1:])

    # map arguments to values in location resource
    # query_filters are passed to the API,
    # filters are applied to values returned from the API
    return {
        'config_file': args.config_file or DEFAULT_CONFIG_FILE,
        'query_filters': {
            'parkingZoneGroup': args.parking_zone,
            'giRestroom': args.gi_restrooms,
            'q': args.query,
            'campus': args.campus,
        },
        'filters': {
            'bldgID': args.building_id,
        }
    }


def parse_query_filters(filters):
    output_filters = {}
    for key, value in filters.items():
        if value is not None:
            output_filters[key] = value
    return output_filters


def post_filter_locations(locations, args):
    for filter_key in parse_query_filters(args['filters']):
        locations = [location for location in locations
                     if location['attributes'][filter_key] ==
                     args['filters'][filter_key]]
    if args['filters']['bldgID'] is not None and len(locations) > 0:
        return locations[0]
    return locations


def fetch_locations(host, auth_token, args):
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json'
    }

    params = {
        'page[size]': 10000
    }
    params.update(parse_query_filters(args['query_filters']))

    r = requests.get(f'{host}v1/locations',
                     params, headers=headers)
    r.raise_for_status()

    data = r.json()

    locations = data['data']

    return post_filter_locations(locations, args)


args = parse_arguments()

cred_helper = ConfigHelper(args['config_file'])

host = cred_helper.get_host_url()
auth_token = cred_helper.get_access_token()

locations = fetch_locations(host, auth_token, args)
print(json.dumps(locations))
