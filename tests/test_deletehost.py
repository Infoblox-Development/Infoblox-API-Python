import responses
from requests.exceptions import HTTPError
from infoblox import infoblox
from . import testcasefixture


class TestDeleteHost(testcasefixture.TestCaseWithFixture):
    fixture_name = 'host_delete'

    @classmethod
    def setUpClass(cls):
        super(TestDeleteHost, cls).setUpClass()
        with responses.RequestsMock() as res:
            res.add(responses.GET,
                    'https://10.10.10.10/wapi/v1.6/record:host',
                    body=cls.body,
                    status=200)
            res.add(responses.DELETE,
                    'https://10.10.10.10/wapi/v1.6/record:host/ZG5zLmhvc3QkLl9kZWZhdWx0LmNvbS5lcXVpZmF4LnVzLmxhYnMuY2lhLmFhYS10ZXN0aG9zdA:host.domain.com/default',
                    status=200)
            cls.ip = cls.iba_ipa.delete_host_record('host.domain.com')

    def test_host_delete(self):
        self.assertIsNone(self.ip)

    @responses.activate
    def test_host_delete_hostnotfound(self):
        responses.add(responses.GET,
                      'https://10.10.10.10/wapi/v1.6/record:host',
                      body='[]',
                      status=200)
        responses.add(responses.DELETE,
                      'https://10.10.10.10/wapi/v1.6/record:host/ZG5zLmhvc3QkLl9kZWZhdWx0LmNvbS5lcXVpZmF4LnVzLmxhYnMuY2lhLmFhYS10ZXN0aG9zdA:host.domain.com/default',
                      status=200)
        with self.assertRaises(infoblox.InfobloxNotFoundException):
            ip = self.iba_ipa.delete_host_record('hostnotfound.domain.com')

    @responses.activate
    def test_host_delete_servererror(self):
        responses.add(responses.GET,
                      'https://10.10.10.10/wapi/v1.6/record:host',
                      body=self.body,
                      status=500)
        responses.add(responses.DELETE,
                      'https://10.10.10.10/wapi/v1.6/record:host/ZG5zLmhvc3QkLl9kZWZhdWx0LmNvbS5lcXVpZmF4LnVzLmxhYnMuY2lhLmFhYS10ZXN0aG9zdA:host.domain.com/default',
                      status=200)
        with self.assertRaises(HTTPError):
            ip = self.iba_ipa.delete_host_record('host.domain.com')

