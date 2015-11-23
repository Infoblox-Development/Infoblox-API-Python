import responses
from requests.exceptions import HTTPError
from infoblox import infoblox
from . import testcasefixture


class TestGetIpByHost(testcasefixture.TestCaseWithFixture):
    fixture_name = 'host_getbyip'

    @classmethod
    def setUpClass(cls):
        super(TestGetIpByHost, cls).setUpClass()
        with responses.RequestsMock() as res:
            res.add(responses.GET,
                    'https://10.10.10.10/wapi/v1.6/record:host',
                    body=cls.body,
                    status=200)
            cls.ip = cls.iba_ipa.get_ip_by_host('192.168.40.10')


    def test_get_ip_by_host(self):
        response_test_list = ['192.168.40.10']
        self.assertListEqual(self.ip, response_test_list)

    @responses.activate
    def test_get_ip_by_hostnotfound(self):
        responses.add(responses.GET,
                      'https://10.10.10.10/wapi/v1.6/record:host',
                      body='[]',
                      status=200)
        with self.assertRaises(infoblox.InfobloxNotFoundException):
            self.iba_ipa.get_ip_by_host('127.0.0.1')

    @responses.activate
    def test_get_ip_by_host_serverfail(self):
        responses.add(responses.GET,
                      'https://10.10.10.10/wapi/v1.6/record:host',
                      body='[]',
                      status=500)
        with self.assertRaises(HTTPError):
            self.iba_ipa.get_ip_by_host('192.168.40.10')
