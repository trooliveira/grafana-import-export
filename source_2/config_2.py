#!/usr/bin/env python

from organizations import Organization
from datasources import Datasource
from dashboard_folder import Dashboard
from pathvalidate.argparse import validate_filepath, ValidationError
import argparse
import sys


def main():

    argp = argparse.ArgumentParser(description='Grafana import/export configs')
    argp.add_argument('-H', '--host', dest='host', type=str,
                      help='URL Grafana', required=False)
    argp.add_argument('-P', '--port', dest='port', type=str,
                      help='Port URL Grafana', required=False)
    argp.add_argument('-d', '--dir', dest='directory', type=str,
                      help='Directory for backup or get restore', required=False)
    argp.add_argument('--proxy', dest='proxy', type=str,
                      help='Proxy for requests (host and port)', default=None, required=False)

    args = argp.parse_args()

    try:
        validate_filepath(args.directory)
    except ValidationError:
        raise ValidationError, ValueError


if __name__ == "__main__":
    main()


'''class Commands(object):

    def __init__(self):

        argp = argparse.ArgumentParser(description='Grafana import/export configs',
                                       usage='config <commands> [<args>]
                                       Commands:
                                                backup     Backup panels, organizations and datasources
                                                restore    Restore panels, organizations and datasources
                                        )
        argp.add_argument('command', help='Subcommand to run')

        args_raw = argp.parse_args(sys.argv[1:2])

        if not hasattr(self, args_raw.command):
            print('Unrecognized command')
            argp.print_help()
            exit(1)

        args = getattr(self, args_raw.command)()

        self.command = args_raw.command
        self.host_port_request = '{}:{}'.format(args.host, args.port)
        try:
            self.host_request = 'http://api_key:{}@{}'.format(
                args.api_key, self.host_port_request)
        except Exception:
            self.user_pass_request = '{}:{}'.format(args.user, args.passd)
            self.host_request_basic_auth = 'http://{}@{}'.format(self.user_pass_request,
                                                                 self.host_port_request)
        self.org_api = 'api/org'
        self.orgs_api = 'api/orgs'
        self.folder_api = 'api/folders'
        self.dashboard_api = 'api/dashboards/db'
        self.dashboard_search_api = 'api/search?type=dash-db&query=&'
        self.folder_search_api = 'api/search?query'
        self.datasource_api = 'api/datasources'
        self.directory = args.directory
        self.proxy = {
            "http": args.proxy,
            "https": args.proxy
        }
        self.tp = args.tp
        # version_api = ''
        # user_api = ''

    def call_command(self):

        if self.command == 'backup':
            if self.tp:
                Organization(self.directory, None, self.proxy, self.org_api,
                             self.host_request_basic_auth, self.orgs_api).get_organization()
            else:
                Organization(self.directory, self.host_request, self.proxy,
                             self.org_api).get_organization()
            Datasource(self.directory, self.host_request, self.proxy,
                       self.datasource_api).get_datasource()
            Dashboard(self.directory, self.host_request, self.proxy,
                      self.dashboard_api, self.dashboard_search_api,
                      self.folder_api, self.folder_search_api).get_dashboard()
        elif self.command == 'restore':
            if self.tp:
                Organization(self.directory, self.host_request, self.proxy,
                             self.org_api).post_organization()
            else:
                Organization(self.directory, None, self.proxy, self.org_api,
                             self.host_request_basic_auth, self.orgs_api).post_organization()
            Datasource(self.directory, self.host_request, self.proxy,
                       self.datasource_api).post_datasource()
            Dashboard(self.directory, self.host_request, self.proxy,
                      self.dashboard_api, self.dashboard_search_api,
                      self.folder_api, self.folder_search_api).post_dashboard()

    def backup(self):

        argp = argparse.ArgumentParser(
            description='Backup panels, folders, organizations, datasources')
        argp.add_argument('backup')
        argp.add_argument('all', action='store_true')
        argp.add_argument('current', action='store_false')
        argp.parse_args(sys.argv[2:3])

        if sys.argv[2] == 'all':
            result = self.all(sys.argv[1])
        elif sys.argv[2] == 'current':
            result = self.current(sys.argv[1])
        return result

    def restore(self):

        argp = argparse.ArgumentParser(
            description='Restore panels, folders, organizations, datasources')
        argp.add_argument('restore')
        argp.add_argument('all', action='store_true')
        argp.add_argument('current', action='store_false')
        argp.parse_args(sys.argv[2:3])

        if sys.argv[2] == 'all':
            result = self.all(sys.argv[1])
        elif sys.argv[2] == 'current':
            result = self.current(sys.argv[1])

        return result

    def global_commands(self, action):
        argp = argparse.ArgumentParser()
        argp.add_argument('-H', '--host', dest='host', type=str,
                          help='URL Grafana', required=False)
        argp.add_argument('-P', '--port', dest='port', type=str,
                          help='Port URL Grafana', required=False)
        argp.add_argument('-d', '--dir', dest='directory', type=validate_filepath_arg,
                          help='Directory for backup or get restore', required=False)
        argp.add_argument('--proxy', dest='proxy', type=str,
                          help='Proxy for requests (host and port)', default=None, required=False)
        if action == 'all':
            args = argp.parse_args(sys.argv[7:])

        elif action == 'current':
            args = argp.parse_args(sys.argv[5:])

        return argparse.Namespace(**vars(args))

    def all(self, action):

        argp = argparse.ArgumentParser()
        argp.add_argument('-u', '--user', dest='user', type=str,
                          help='user', required=False)
        argp.add_argument('-p', '--password', dest='passd', type=str,
                          help='password', required=False)
        args = argp.parse_args(sys.argv[3:7])
        glob = self.global_commands('all')

        di = dict()
        for x in [args, glob, argparse.Namespace(tp=True)]:
            di.update(**vars(x))

        return(argparse.Namespace(**di))

    def current(self, action):

        argp = argparse.ArgumentParser()
        argp.add_argument('-k', '--api-key', dest='api_key',
                          type=str, help='bearer token', required=False)
        args = argp.parse_args(sys.argv[3:5])

        glob = self.global_commands('current')

        di = dict()
        for x in [args, glob, argparse.Namespace(tp=False)]:
            di.update(**vars(x))

        return(argparse.Namespace(**di))


if __name__ == "__main__":
    Commands().call_command()'''
