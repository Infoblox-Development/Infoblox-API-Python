import responses
from requests.exceptions import HTTPError
from infoblox import infoblox
from . import testcasefixture


class TestGetHost(testcasefixture.TestCaseWithFixture):
    fixture_name = 'host_get'

    @classmethod
    def setUpClass(cls):
        super(TestGetHost, cls).setUpClass()
        with responses.RequestsMock() as res:
            res.add(responses.GET,
                    'https://10.10.10.10/wapi/v1.6/record:host',
                    body=cls.body,
                    status=200)
            cls.ip = cls.iba_ipa.get_host('host.domain.com')

    def test_get_host(self):
        response_test_dict = {'view': 'default',
                              'name': 'host.domain.com',
                              'ipv4addrs': [{'host':
                                             'host.domain.com',
                                             'ipv4addr': '192.168.40.10',
                                             '_ref': 'record:host_ipv4addr/ZG5zLmhvc3RfYWRkcmVzcyQuX2RlZmF1bHQuY29tLmVxdWlmYXgudXMubGFicy5jaWEuYWFhLXRlc3Rob3N0LjEyLjYuNC4yLg:192.168.40.10/host.domain.com/default',
                                             'configure_for_dhcp': False}],
                              '_ref': 'record:host/ZG5zLmhvc3QkLl9kZWZhdWx0LmNvbS5lcXVpZmF4LnVzLmxhYnMuY2lhLmFhYS10ZXN0aG9zdA:host.domain.com/default'}
        self.assertDictEqual(self.ip, response_test_dict)

    @responses.activate
    def test_get_host_nohostfound(self):
        responses.add(responses.GET,
                      'https://10.10.10.10/wapi/v1.6/record:host',
                      body='[]',
                      status=200)
        with self.assertRaises(infoblox.InfobloxNotFoundException):
            ip = self.iba_ipa.get_host('host.domain.com')

    @responses.activate
    def test_get_host_servererror(self):
        responses.add(responses.GET,
                      'https://10.10.10.10/wapi/v1.6/record:host',
                      body='[]',
                      status=500)
        with self.assertRaises(HTTPError):
            ip = self.iba_ipa.get_host('host.domain.com')
