#!/usr/bin/env python

import requests
from os import mkdir, path, listdir
import json


class Requests(object):

    def __init__(self, host, proxy, data=None):
        self.host = host
        self.header = {
                       'Content-Type': 'application/json; charset=utf-8',
                       'Accept': 'application/json',
                       'Accept-Charset': 'utf-8'
        }
        self.proxy = proxy
        self.data = data

    def get_requests(self):
        json_things = requests.get(self.host, headers=self.header, proxies=self.proxy)
        return json_things.json()

    def post_requests(self):
        requests.post(self.host, headers=self.header, proxies=self.proxy, json=self.data)


class WriteRead(object):

    def __init__(self, directory, name, data=None):
        self.directory = directory
        self.name = name
        self.data = data

    def write(self):
        dir = '{}/{}'.format(self.directory, self.name)
        if not path.exists(dir):
            mkdir('{}'.format(dir))
        with open('{}/{}'.format(dir, '{}.json'.format(self.name), indent=True), 'w') as f:
            json.dump(self.data, f)

    def read(self):
        with open('{}/{}'.format(self.directory, self.name), 'r') as f:
            raw = f.read()
            data = json.loads(raw)
        return data


def list_convert(self):
    files = [f for f in listdir("{}".format(self.directory))]
    return files
