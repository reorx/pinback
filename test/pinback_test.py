import os
import shutil
import tempfile
import pytest
import re
import json
import httpretty
from urllib.parse import urlparse
from pinback import API, save_to_file


class MockApp(object):
    def __init__(self, base_url):
        self.base_url = base_url
        httpretty.enable()
        httpretty.HTTPretty.allow_net_connect = False

    def route(self, method, uri):
        url = self.base_url + uri
        pattern = re.compile('{}$'.format(url))

        def deco(f):
            def request_handler(request, url, headers):
                o = urlparse(url)
                url_no_params = '{o.scheme}://{o.netloc}{o.path}'.format(o=o)
                print('got request', request, url, url_no_params, headers)
                matched = pattern.search(url_no_params).groups()
                return f(request, *matched)

            httpretty.register_uri(
                getattr(httpretty, method),
                pattern,
                body=request_handler,
                streaming=True,
            )
            return f
        return deco


@pytest.fixture
def mock_app():
    app = MockApp(API.base_url)
    tmpdir = tempfile.mkdtemp()
    os.chdir(tmpdir)
    yield app
    shutil.rmtree(tmpdir)


def test_save_to_file(mock_app):
    content = '<xml>pinboard</xml>'
    token = 'fake-token'

    @mock_app.route('GET', '/posts/all')
    def mock_posts_all(req):
        try:
            auth_token = req.querystring['auth_token'][0]
        except IndexError as e:
            return (400, {}, 'can not get auth_token from request: {}'.format(e))
        if auth_token != token:
            return (400, {}, 'auth_token != pre defined token: {}'.format(auth_token))
        return (200, {}, content)

    api = API(token)
    resp = api.posts.all(raw=True)
    assert resp.status_code == 200, 'status_code={} body={}'.format(resp.status_code, resp.content)

    filename = save_to_file(resp.content)
    with open(filename, 'r') as f:
        assert f.read().strip() == content
