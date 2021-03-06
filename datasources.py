#!/usr/bin/env python

from request import Requests
from request import WriteRead
from request import list_convert
import json


class Datasource(object):

    def __init__(self, directory, host_request, proxy, org_api, org_name=None):
        self.host_request = host_request
        self.org_api = org_api
        self.proxy = proxy
        self.directory = directory
        self.org_name = org_name

    def get_datasource(self):
        datasources_get = Requests('{}/{}'.format(self.host_request, self.org_api), self.proxy).get_requests()
        for dsource in datasources_get:
            if 'testdata' not in dsource['type'].lower():
                WriteRead(self.directory, dsource['type'].lower(), dsource, self.org_name, 'datasources').write()

    # post
    def post_datasource(self):
        dir = '{}/{}/datasources'.format(self.directory, self.org_name)
        files = list_convert(dir)
        for file in files:
            data = WriteRead(dir, file).read()
            Requests('{}/{}'.format(self.host_request, self.org_api), self.proxy, data).post_requests()
