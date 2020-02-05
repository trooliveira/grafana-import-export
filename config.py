#!/usr/bin/env python

from organizations import Organization
from datasources import Datasource
from dashboard_folder import Dashboard
from pathvalidate.argparse import validate_filepath, ValidationError
import argparse
import sys


def main():

    glb = argparse.ArgumentParser(conflict_handler='resolve')
    glb.add_argument('-H', '--host', dest='host', type=str,
                    help='URL Grafana', required=True)
    glb.add_argument('-P', '--port', dest='port', type=str,
                    help='Port URL Grafana', required=True)
    glb.add_argument('-d', '--dir', dest='directory', type=validate_filepath,
                    help='Directory for backup or get restore',
                    required=True)
    glb.add_argument('--proxy', dest='proxy', type=str,
                    help='Proxy for requests (host and port)',
                    default=None, required=False)

    type_group = glb.add_mutually_exclusive_group(required=True)
    type_group.add_argument('--backup', action='store_true', dest='type',
                            help='Backup panels and configs')
    type_group.add_argument('--restore', action='store_false', dest='type',
                            help='Restore panels and configs')

    type_form = glb.add_mutually_exclusive_group(required=True)
    type_form.add_argument('--current', action='store_true', dest='form')
    type_form.add_argument('--all', action='store_false', dest='form')

    key_usr = glb.add_mutually_exclusive_group(required=True)
    key_usr.add_argument('-k', '--api-key', dest='api_key',
                     type=str, help='bearer token')
    key_usr.add_argument('-u', '--user', dest='user', type=str,
                     help='user')

    glb.add_argument('-p', '--password', dest='passd', type=str,
                     help='password')

    args = glb.parse_args()

    """ try:
        validate_filepath(args.directory)
    except ValidationError:
        raise ValidationError, ValueError """

    host_port_request = '{}:{}'.format(args.host, args.port)
    try:
        host_request = 'http://api_key:{}@{}'.format(args.api_key, host_port_request)
    except Exception:
        try:
            user_pass_request = '{}:{}'.format(args.user, args.passd)
            host_request_basic_auth = 'http://{}@{}'.format(user_pass_request, host_port_request)
        except ValueError as e:
            raise 'It needs password arg', e

    org_api = 'api/org'
    orgs_api = 'api/orgs'
    folder_api = 'api/folders'
    dashboard_api = 'api/dashboards/db'
    dashboard_search_api = 'api/search?type=dash-db&query=&'
    folder_search_api = 'api/search?query'
    datasource_api = 'api/datasources'
    directory = args.directory
    proxy = {
        "http": args.proxy,
        "https": args.proxy
    }

    if args.type is True:
        if args.form is True:
            Organization(directory, host_request, proxy, org_api).get_organization()
        elif args.form is False:
            Organization(directory, None, proxy, org_api,
                         host_request_basic_auth, orgs_api).get_organization()

        Datasource(directory, host_request, proxy,
                   datasource_api).get_datasource()
        Dashboard(directory, host_request, proxy,
                  dashboard_api, dashboard_search_api,
                  folder_api, folder_search_api).get_dashboard()
    elif args.type is False:
        if args.form is True:
            Organization(directory, host_request, proxy,
                         org_api).post_organization()
        elif args.form is False:
            Organization(directory, None, proxy, org_api,
                         host_request_basic_auth, orgs_api).post_organization()
        Datasource(directory, host_request, proxy,
                   datasource_api).post_datasource()
        Dashboard(directory, host_request, proxy,
                  dashboard_api, dashboard_search_api,
                  folder_api, folder_search_api).post_dashboard()


if __name__ == "__main__":
    main()
