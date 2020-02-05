#!/usr/bin/env python

from request import Requests
from request import WriteRead
from request import list_convert
from folder import Folders
import json


class Dashboard(object):

    def __init__(self, directory,
                 host_request, proxy, dashboard_api,
                 dashboard_search_api,
                 folder_api, folder_search_api):
        self.host_request = host_request
        self.dashboard_api = dashboard_api
        self.dashboard_search_api = dashboard_search_api
        self.folder_search_api = folder_search_api
        self.folder_api = folder_api
        self.proxy = proxy
        self.directory = directory

    def get_dashboard(self):
        # dashboard
        # get all dashboards
        dashboards_raw = Requests('{}/{}'.format(self.host_request,
                                                 self.dashboard_search_api), self.proxy).get_requests()
        # get each dasboard and write them
        for dash in list(range(len(dashboards_raw))):
            dashboard_stage = Requests('{}/{}/{}'.format(self.host_request, self.dashboard_api,
                                                         dashboards_raw[dash]['uri'].replace('db/', '')),
                                       self.proxy).get_requests()
            tags = dashboard_stage
            for item in ['created', 'createdBy', 'updated', 'updatedBy', 'expires', 'version']:
                del tags['meta'][item]

            if 'overwrite' in list(tags['meta'].keys()):
                del tags['overwrite']
            elif 'dashboard' in list(tags['dashboard'].keys()):
                del tags['dashboard']['version']

            tags['dashboard']['id'] = 'null'
            tags['dashboard']['uid'] = 'null'
            # folder
            # get folder
            print(tags)
            Folders(self.directory, self.host_request, self.folder_api,
                    self.proxy, tags['meta']['folderId']).get_folder()
            WriteRead(self.directory, tags['meta']['slug'], tags).write()

    def post_dashboard(self):
        files = list_convert(self.directory)
        for file in files:
            data_raw = WriteRead(self.directory, file).read()
            data = {
                'folderId': Folders(self.directory, self.host_request, self.folder_api,
                                    self.proxy, None, self.folder_search_api).post_folder(),
                'overwrite': True,
                'dashboard': {
                    'tags': data_raw['dashboard']['tags'],
                    'title': data_raw['dashboard']['title'],
                    'version': data_raw['dashboard']['version'],
                    'timezone': data_raw['dashboard']['timezone'],
                    'schemaVersion': data_raw['dashboard']['schemaVersion'],
                    'templating': data_raw['dashboard']['templating'],
                    'id': '',
                    'uid': ''
                }
            }

            if 'rows' in list(data_raw['dashboard'].keys()):
                data['dashboard'].update({'rows': data_raw['dashboard']['rows']})
            else:
                data['dashboard'].update({'panels': data_raw['dashboard']['panels']})

            Requests('{}/{}'.format(self.host_request, self.dashboard_api),
                     self.proxy, data).post_requests()
