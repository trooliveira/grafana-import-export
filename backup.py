#!/usr/bin/env python
# encoding: utf-8

from requests import get
from json import dump
from os import mkdir, path


class Backup(object):

    def __init__(self, FILE_DIR, head, proxies, API, dashboard='', folder=''):
        self.FILE_DIR = FILE_DIR
        self.head = head
        self.proxies = proxies
        self.API = API
        self.dashboard = dashboard
        self.folder = folder

    def get_organization(self):

        orgs = get('{}/org'.format(self.API), headers=self.head, proxies=self.proxies)
        # print(orgs.status_code)
        org = orgs.json()
        name = org['name']  # .replace('.', '')
        directory = '{}/{}'.format(self.FILE_DIR, name)

        if not path.exists(directory):
            mkdir('{}'.format(directory))
            mkdir('{}/folders'.format(directory))
            mkdir('{}/dashboards'.format(directory))
            mkdir('{}/datasources'.format(directory))

        return name

    def get_folder(self, id_index):

        folders = get('{}/id/{}'.format(self.folder, id_index),
                      headers=self.head, proxies=self.proxies)
        # print(folders.status_code).directo.directoryry

        foldering = folders.json()
        name = foldering['title'].replace(' - ', ' ').replace(' ', '-')
        name = name.lower().encode('utf-8')
        file = '{}.json'.format(name)

        with open('{}/{}/folders/{}'.format(self.FILE_DIR,
                                            Backup.get_organization(self),
                                            file, indent=True), 'w') as f:
            dump(foldering, f)

    def get_all_dashboards(self):
        dashboards_raw = get('{}/search?type=dash-db&query=&'.format(self.API),
                             headers=self.head, proxies=self.proxies)
        # print(dashboards_raw.status_code)

        for dash in dashboards_raw.json():
            dashboard_stage = get('{}/{}'.format(self.dashboard, dash['uri']),
                                  headers=self.head, proxies=self.proxies)
            # print(dashboard_stage.status_code)
            tags = dashboard_stage.json()

            for item in ['created', 'createdBy', 'updated', 'updatedBy', 'expires', 'version']:
                del tags['meta'][item]

            if 'overwrite' in tags['meta'].keys():
                del tags['overwrite']
            elif 'dashboard' in tags['dashboard'].keys():
                del tags['dashboard']['version']

            tags['dashboard']['id'] = 'null'
            tags['dashboard']['uid'] = 'null'

            if tags['meta']['folderId'] != 0:
                self.get_folder(tags['meta']['folderId'])

            with open('{}/{}/dashboards/{}'.format(self.FILE_DIR,
                                                   Backup.get_organization(self),
                                                   '{}.json'.format(tags['meta']['slug'])), 'w') as f:
                dump(dashboard_stage.json(), f, indent=True)

    def get_all_datasources(self):
        datasources_raw = get('{}/datasources'.format(self.API),
                              headers=self.head, proxies=self.proxies)
        # print(datasources_raw.status_code)

        for data in datasources_raw.json():
            if 'testdata' not in data['type'].lower():
                name = data['name'].replace(' - ', ' ').replace(' ', '-')  # .replace('_','-')
                name = name.lower().encode('utf-8')
                file = '{}.json'.format(name)
                with open('{}/{}/datasources/{}'.format(self.FILE_DIR,
                                                        Backup.get_organization(self), file), 'w') as f:
                    dump(data, f, indent=True)
