#!/usr/bin/env python

import argparse

glb = argparse.ArgumentParser(conflict_handler='resolve')
glb.add_argument('-H', '--host', dest='host', type=str,
                 help='URL Grafana', required=True)
glb.add_argument('-P', '--port', dest='port', type=str,
                 help='Port URL Grafana', required=True)
glb.add_argument('-d', '--dir', dest='directory', type=str,
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
glb.add_argument('--current', action='store_true')
glb.add_argument('-k', '--api-key', dest='api_key',
                         type=str, help='bearer token')
glb.add_argument('--all', action='store_false')
glb.add_argument('-u', '--user', dest='user', type=str,
                     help='user')
glb.add_argument('-p', '--password', dest='passd', type=str,
                     help='password')

print(glb.parse_args())
args = glb.parse_args()

if args.current is True and args.user is not None and args.passd is not None:
    raise ValueError
elif args.all is False and args.api_key is not None:
    raise ValueError
# args.func()
# args.foo_bar(args)
