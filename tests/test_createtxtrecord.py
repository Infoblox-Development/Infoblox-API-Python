import responses
from requests.exceptions import HTTPError
from infoblox import infoblox
from . import testcasefixture


class TestCreateTxtRecord(testcasefixture.TestCaseWithFixture):
    fixture_name = 'txt_create'

    @classmethod
    def setUpClass(cls):
        super(TestCreateTxtRecord, cls).setUpClass()
        with responses.RequestsMock() as res:
            res.add(responses.POST,
                    'https://10.10.10.10/wapi/v1.6/record:txt',
                    body=cls.body,
                    status=200)
            cls.ip = cls.iba_ipa.create_txt_record('txtrecord.domain.com',
                                                   'target.domain.com')

    def test_txt_create(self):
        self.assertIsNone(self.ip)

    @responses.activate
    def test_txt_create_error(self):
        responses.add(responses.POST,
                      'https://10.10.10.10/wapi/v1.6/record:txt',
                      body=self.body,
                      status=500)
        with self.assertRaises(HTTPError):
            self.iba_ipa.create_txt_record('txtrecord.domain.com',
                                           'target.domain.com')
