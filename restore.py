#!/usr/bin/env python

from backup import Backup
from requests import get, post
from json import loads
from glob import glob
from urllib import quote



class Restore(Backup, object):
    
    def __init__(self, FILE_DIR, head, proxies, API, dashboard, folder):
        super(Restore, self).__init__(FILE_DIR, head, proxies, API, dashboard, folder)

    def post_folders(self, folderTitle):
        
        directory = '{}/{}/folders'.format(self.FILE_DIR,
                                           self.get_organization())

        with open('{}/{}.json'.format(directory,
                    folderTitle.replace(' - ', ' ').replace(' ', '-').lower().encode('utf-8')),
                        'r') as f:
            raw = f.read()
            data_raw = loads(raw)
            data = {
                'title': data_raw['title']
            }
            
            try:
                request = post(self.folder, headers=self.head, json=data, proxies=self.proxies)
                post_response = request.json()
            except ValueError:
                folders = get('{}/search?query={}'.format(self.API, quote(data['title'].encode("utf-8"))),
                headers=self.head, proxies=self.proxies)

                post_response = folders.json()
            data = post_response[0]['id']

            return data

    def post_all_dashboards(self):

        directory = '{}/{}/dashboards'.format(self.FILE_DIR,
                                              self.get_organization())

        files = [f for f in glob("{}/*.json".format(directory))]

        for file in files:
            with open('{}'.format(file), 'r') as f:
                raw = f.read()
                data_raw = loads(raw)

                data = {
                    'folderId': self.post_folders(data_raw['meta']['folderTitle']) if data_raw['meta']['folderId'] != 0 else 0,
                    'overwrite':True,
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

                if 'rows' in data_raw['dashboard'].keys():
                    data['dashboard'].update({'rows': data_raw['dashboard']['rows']})
                else:
                    data['dashboard'].update({'panels': data_raw['dashboard']['panels']})
            
                post('{}/db'.format(self.dashboard), headers=self.head, json=data, proxies=self.proxies)

    def post_all_datasources(self):
        directory = '{}/{}/datasources'.format(self.FILE_DIR,
                                               self.get_organization())

        files = [f for f in glob("{}/*.json".format(directory))]

        for file in files:
            with open('{}'.format(file), 'r') as f:
                raw = f.read()
                data_raw = loads(raw)
                post('{}/datasources'.format(self.API),
                                                headers=self.head, json=data_raw, proxies=self.proxies)
