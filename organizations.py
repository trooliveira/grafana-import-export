#!/usr/bin/env python

from request import Requests
from request import WriteRead
from request import list_convert
import json


class Organization(object):

    def __init__(self, directory, host_request, proxy,
                 org_api=None, org_name=None, host_request_basic_auth=None, orgs_api=None):
        self.host_request = host_request
        self.org_api = org_api
        self.orgs_api = orgs_api
        self.proxy = proxy
        self.host_request_basic_auth = host_request_basic_auth
        self.directory = directory
        self.org_name = org_name

    def get_organization(self):

        org_list = list()
        if self.host_request_basic_auth is None:
            # organization
            # get current
            org = [ Requests('{}/{}'.format(self.host_request, self.org_api), self.proxy).get_requests() ]
        else:
            # organization
            # get all
            org = Requests('{}/{}'.format(self.host_request_basic_auth,
                                          self.orgs_api), self.proxy).get_requests()
        for x in list(range(len(org))):
            WriteRead(self.directory, org[x]['name'], org[x]).write()
            org_list.append(org[x]['name'])

        return org_list


    def post_organization(self):
        # post organization
        dir = '{}/{}'.format(self.directory, self.org_name)
        files = list_convert(dir)
        for file in files:
            data_raw = WriteRead(dir, file).read()
            data = {
                'name': data_raw['name']
            }
            Requests('{}/{}'.format(self.host_request_basic_auth,
                                    self.orgs_api), self.proxy, data).post_requests()
