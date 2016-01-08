import responses
from requests.exceptions import HTTPError
from infoblox import infoblox
from . import testcasefixture


class TestCreateHostRecord(testcasefixture.TestCaseWithFixture):
    fixture_name = 'host_create'

    @classmethod
    def setUpClass(cls):
        super(TestCreateHostRecord, cls).setUpClass()
        with responses.RequestsMock() as res:
            res.add(responses.POST,
                    'https://10.10.10.10/wapi/v1.6/record:host',
                    body=cls.body,
                    status=200)
            cls.ip = cls.iba_ipa.create_host_record('192.168.40.10',
                                                    'host.domain.com')

    def test_host_create(self):
        self.assertEqual(self.ip, '192.168.40.10')

    @responses.activate
    def test_host_create_badip(self):
        responses.add(responses.POST,
                      'https://10.10.10.10/wapi/v1.6/record:host',
                      body=self.body,
                      status=200)
        with self.assertRaises(infoblox.InfobloxBadInputParameter):
            self.iba_ipa.create_host_record('not.an.ip.com',
                                            'host.domain.com')

    @responses.activate
    def test_host_create_badresponse(self):
        responses.add(responses.POST,
                      'https://10.10.10.10/wapi/v1.6/record:host',
                      body='[]',
                      status=500)
        with self.assertRaises(HTTPError):
            self.iba_ipa.create_host_record('192.168.40.10',
                                            'host.domain.com')
