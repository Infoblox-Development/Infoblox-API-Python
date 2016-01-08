import responses
from requests.exceptions import HTTPError
from infoblox import infoblox
from . import testcasefixture


class TestDeleteHostAlias(testcasefixture.TestCaseWithFixture):
    fixture_name = 'alias_delete'

    @classmethod
    def setUpClass(cls):
        super(TestDeleteHostAlias, cls).setUpClass()
        with responses.RequestsMock() as res:
            res.add(responses.GET,
                    'https://10.10.10.10/wapi/v1.6/record:host',
                    body=cls.body,
                    status=200)
            res.add(responses.PUT,
                    'https://10.10.10.10/wapi/v1.6/record:host/ZG5zLmhvc3QkLl9kZWZhdWx0LmNvbS5lcXVpZmF4LnVzLmxhYnMuY2lhLmFhYS10ZXN0aG9zdA:host.domain.com/default',
                    status=200)
            cls.ip = cls.iba_ipa.delete_host_alias('host.domain.com',
                                                'alias.domain.com')

    def test_delete_host_alias(self):
        self.assertIsNone(self.ip)


    @responses.activate
    def test_delete_host_alias_unexpectedhost(self):
        responses.add(responses.GET,
                      'https://10.10.10.10/wapi/v1.6/record:host',
                      body=self.body,
                      status=200)
        responses.add(responses.PUT,
                      'https://10.10.10.10/wapi/v1.6/record:host/ZG5zLmhvc3QkLl9kZWZhdWx0LmNvbS5lcXVpZmF4LnVzLmxhYnMuY2lhLmFhYS10ZXN0aG9zdA:host.domain.com/default',
                      status=200)
        with self.assertRaises(infoblox.InfobloxGeneralException):
            self.iba_ipa.delete_host_alias('badhost.domain.com',
                                           'alias.domain.com')

    @responses.activate
    def test_delete_host_alias_hostnotfound(self):
        responses.add(responses.GET,
                      'https://10.10.10.10/wapi/v1.6/record:host',
                      body='[]',
                      status=200)
        responses.add(responses.PUT,
                      'https://10.10.10.10/wapi/v1.6/record:host/ZG5zLmhvc3QkLl9kZWZhdWx0LmNvbS5lcXVpZmF4LnVzLmxhYnMuY2lhLmFhYS10ZXN0aG9zdA:host.domain.com/default',
                      status=200)
        with self.assertRaises(infoblox.InfobloxNotFoundException):
            self.iba_ipa.delete_host_alias('nohost.domain.com',
                                           'alias.domain.com')

    @responses.activate
    def test_delete_host_alias_servererroronget(self):
        responses.add(responses.GET,
                      'https://10.10.10.10/wapi/v1.6/record:host',
                      body='[]',
                      status=500)
        responses.add(responses.PUT,
                      'https://10.10.10.10/wapi/v1.6/record:host/ZG5zLmhvc3QkLl9kZWZhdWx0LmNvbS5lcXVpZmF4LnVzLmxhYnMuY2lhLmFhYS10ZXN0aG9zdA:host.domain.com/default',
                      status=200)
        with self.assertRaises(HTTPError):
            self.iba_ipa.delete_host_alias('host.domain.com',
                                           'alias.domain.com')

    @responses.activate
    def test_delete_host_alias_servererroronpost(self):
        responses.add(responses.GET,
                      'https://10.10.10.10/wapi/v1.6/record:host',
                      body=self.body,
                      status=200)
        responses.add(responses.PUT,
                      'https://10.10.10.10/wapi/v1.6/record:host/ZG5zLmhvc3QkLl9kZWZhdWx0LmNvbS5lcXVpZmF4LnVzLmxhYnMuY2lhLmFhYS10ZXN0aG9zdA:host.domain.com/default',
                      status=500)
        with self.assertRaises(HTTPError):
            self.iba_ipa.delete_host_alias('host.domain.com',
                                           'alias.domain.com')
