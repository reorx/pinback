#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import datetime
import requests


class API(object):
    base_url = 'https://api.pinboard.in/v1'
    uris = {
        '/posts/all': {
            'method': 'GET'
        },
        '/posts/recent': {
            'method': 'GET'
        },
    }
    token = None

    def __init__(self, token):
        self.token = token

    def __getattr__(self, name):
        return ResourcePath(self, name)

    def get_url(self, uri):
        return self.base_url + uri + '?auth_token=%s' % self.token

    def make_req(self, uri):
        try:
            options = self.uris[uri]
        except KeyError:
            raise Exception('URI %s is not in uris' % uri)
        method = options['method'].lower()

        requester = getattr(requests, method)
        url = self.get_url(uri)
        print('[REQUEST] {} {}'.format(requester.__name__, uri))
        resp = requester(url)
        return resp


class ResourcePath(object):
    def __init__(self, api, name, parent=None):
        self._api = api
        self._name = name
        self._parent = parent

    def __getattr__(self, name):
        return ResourcePath(self._api, name, self)

    def __call__(self, *args, **kwargs):
        return self._api.make_req(self.get_path())

    def get_path(self):
        names = []

        rp = self
        while rp is not None:
            names.insert(0, rp._name)
            rp = rp._parent

        return '/' + '/'.join(names)

    def __str__(self):
        return '<ResourcePath %s>' % self.get_path()


def save_to_file(body, filename=None):
    if not filename:
        filename = 'pinboard-backup-%s.xml' %\
            datetime.datetime.now().strftime('%Y-%m-%d')

    print('Write {} bytes to file {}'.format(len(body), filename))
    with open(filename, 'wb') as f:
        f.write(body)
    return filename


def main():
    try:
        with open('.token', 'r') as f:
            token = f.read()
    except IOError:
        print('Error: please write your pinboard api token to'
               ' file ".token" in current directory')
        sys.exit(1)

    try:
        filename = sys.argv[1]
    except IndexError:
        filename = None

    api = API(token)
    resp = api.posts.all(raw=True)
    if resp.status_code != 200:
        raise ValueError('request failed, status_code={} body={}'.format(resp.status_code, resp.content))
    save_to_file(resp.content, filename)


if __name__ == '__main__':
    main()
