#!/usr/bin/env python

from request import Requests
from request import WriteRead
from request import list_convert
import json
try:
    from urllib.parse import quote
except Exception:
    from urllib import quote


class Folders(object):

    def __init__(self, directory, host_request, folder_api, proxy, folder_id, org_name, folder_search_api=None):
        self.host_request = host_request
        self.folder_api = folder_api
        self.proxy = proxy
        self.folder_id = folder_id
        self.directory = directory
        self.folder_search_api = folder_search_api
        self.org_name = org_name

    def get_folder(self):
        if self.folder_id != 0:
            folder = Requests('{}/{}/id/{}'.format(self.host_request, self.folder_api,
                                                   self.folder_id), self.proxy).get_requests()
            name = folder['title'].replace(' - ', ' ').replace(' ', '-').lower().encode('utf-8')
            WriteRead(self.directory, name, folder, self.org_name, 'folders').write()

    def post_folder(self):
        data = WriteRead(self.directory, file).read()
        try:
            folders = Requests('{}/{}'.format(self.host_request,
                                              self.folder_api), self.proxy, data).post_requests()
        except ValueError:
            folders = Requests('{}/{}={}'.format(self.host_request,
                                                 self.folder_search_api,
                                                 quote(data['title'].encode("utf-8"))),
                               self.proxy).get_requests()
        folder_id = folders[0]['id'].json()

        if folder_id != 0:
            id = folder_id
        else:
            id = 0

        return id
