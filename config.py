#!/usr/bin/env python

from backup import Backup
from restore import Restore
import argparse


def main():

    argp = argparse.ArgumentParser(description=__doc__,)

    argp.add_argument('-k', '--key', dest='key', type=str,
                      help='bearer token', required=True)
    argp.add_argument('-H', '--host', dest='host', type=str,
                      help='URL Grafana', required=True)
    argp.add_argument('-d', '--dir', dest='directory', type=str,
                      help='Directory for backup or get restore', required=True)
    argp.add_argument('-p', '--proxy', dest='proxy', type=str,
                      help='Proxy for requests (host and port)', default=None, required=False)
    type_group = argp.add_mutually_exclusive_group(required=True)
    type_group.add_argument('-b', '--backup', action='store_true', dest='type',
                            help='Backup panels and configs')
    type_group.add_argument('-r', '--restore', action='store_false', dest='type',
                            help='Restore panels and configs')

    args = argp.parse_args()

    proxies = {
        "http": args.proxy,
        "https": args.proxy
    }

    head = {
        'Authorization': 'Bearer {}'.format(args.key),
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json',
        'Accept-Charset': 'utf-8'
    }

    API = '{}/api'.format(args.host)
    folder = '{}/folders'.format(API)
    dashboard = '{}/dashboards'.format(API)

    attr = [args.directory, head, proxies, API, dashboard, folder]

    if args.type:
        bkp = Backup(*attr)
        bkp.get_organization()
        bkp.get_all_dashboards()
        bkp.get_all_datasources()
    else:
        rst = Restore(*attr)
        rst.post_all_dashboards()
        rst.post_all_datasources()


if __name__ == "__main__":
    main()
