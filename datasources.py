#!/usr/bin/env python

from request import Requests
from request import WriteRead
from request import list_convert
import json


class Datasource(object):

    def __init__(self, directory, host_request, proxy, org_api):
        self.host_request = host_request
        self.org_api = org_api
        self.proxy = proxy
        self.directory = directory

    def get_datasource(self):
        datasources_get = Requests('{}/{}'.format(self.host_request, self.org_api), self.proxy).get_requests()
        for dsource in datasources_get:
            if 'testdata' not in dsource['type'].lower():
                WriteRead(self.directory, dsource['type'].lower(), dsource).write()

    # post
    def post_datasource(self):
        files = list_convert(self.directory)
        for file in files:
            data = WriteRead(self.directory, file).read()
            Requests('{}/{}'.format(self.host_request, self.org_api), self.proxy, data).post_requests()
