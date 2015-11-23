import responses
from requests.exceptions import HTTPError
from infoblox import infoblox
from . import testcasefixture


class TestAddHostAlias(testcasefixture.TestCaseWithFixture):
    fixture_name = 'alias_add'

    @classmethod
    def setUpClass(cls):
        super(TestAddHostAlias, cls).setUpClass()
        with responses.RequestsMock() as res:
            res.add(responses.GET,
                    'https://10.10.10.10/wapi/v1.6/record:host',
                    body=cls.body,
                    status=200)
            res.add(responses.PUT,
                    'https://10.10.10.10/wapi/v1.6/record:host/ZG5zLmhvc3QkLl9kZWZhdWx0LmNvbS5lcXVpZmF4LnVzLmxhYnMuY2lhLmFhYS10ZXN0aG9zdA:host.domain.com/default',
                    status=200)
            cls.ip = cls.iba_ipa.add_host_alias('host.domain.com',
                                                'alias.domain.com')

    def test_add_host_alias(self):
        self.assertIsNone(self.ip)

    @responses.activate
    def test_add_host__alias_nohost(self):
        responses.add(responses.GET,
                      'https://10.10.10.10/wapi/v1.6/record:host',
                      body='[]',
                      status=200)
        responses.add(responses.PUT,
                      'https://10.10.10.10/wapi/v1.6/record:host/ZG5zLmhvc3QkLl9kZWZhdWx0LmNvbS5lcXVpZmF4LnVzLmxhYnMuY2lhLmFhYS10ZXN0aG9zdA:host.domain.com/default',
                      status=200)
        with self.assertRaises(infoblox.InfobloxNotFoundException):
            self.iba_ipa.add_host_alias('nohost.domain.com',
                                        'alias.domain.com')

    @responses.activate
    def test_add_host_alias_badresponse(self):
        responses.add(responses.GET,
                      'https://10.10.10.10/wapi/v1.6/record:host',
                      body='[]',
                      status=500)
        with self.assertRaises(HTTPError):
            self.iba_ipa.add_host_alias('nohost.domain.com',
                                        'alias.domain.com')
