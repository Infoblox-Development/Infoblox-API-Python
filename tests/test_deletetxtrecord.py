import responses
from requests.exceptions import HTTPError
from infoblox import infoblox
from . import testcasefixture


class TestDeleteTxtRecord(testcasefixture.TestCaseWithFixture):
    fixture_name = 'txt_delete'

    @classmethod
    def setUpClass(cls):
        super(TestDeleteTxtRecord, cls).setUpClass()
        with responses.RequestsMock() as res:
            res.add(responses.GET,
                   'https://10.10.10.10/wapi/v1.6/record:txt',
                    body=cls.body,
                    status=200)
            res.add(responses.DELETE,
                    'https://10.10.10.10/wapi/v1.6/record:txt/ZG5zLmJpbmRfdHh0JC5fZGVmYXVsdC5jb20uZXF1aWZheC51cy5sYWJzLmNpYS5hYWFfbW91c3RhY2hlLiJoaXBzdGVydHh0LmNpYS5sYWJzLnVzLmVxdWlmYXguY29tIg:textrecord.domain.com/default',
                    status=200)
            cls.ip = cls.iba_ipa.delete_txt_record('textrecord.domain.com')

    def test_txt_delete(self):
        self.assertIsNone(self.ip)

    @responses.activate
    def test_txt_norecordfound(self):
        responses.add(responses.GET,
                     'https://10.10.10.10/wapi/v1.6/record:txt',
                      body='[]',
                      status=200)
        responses.add(responses.DELETE,
                     'https://10.10.10.10/wapi/v1.6/record:txt/ZG5zLmJpbmRfdHh0JC5fZGVmYXVsdC5jb20uZXF1aWZheC51cy5sYWJzLmNpYS5hYWFfbW91c3RhY2hlLiJoaXBzdGVydHh0LmNpYS5sYWJzLnVzLmVxdWlmYXguY29tIg:textrecord.domain.com/default',
                      status=200)
        with self.assertRaises(infoblox.InfobloxNotFoundException):
            self.iba_ipa.delete_txt_record('norecord.domain.com')

    @responses.activate
    def test_txt_delete_exception(self):
        responses.add(responses.GET,
                     'https://10.10.10.10/wapi/v1.6/record:txt',
                      body=self.body,
                      status=200)
        responses.add(responses.DELETE,
                     'https://10.10.10.10/wapi/v1.6/record:txt/ZG5zLmJpbmRfdHh0JC5fZGVmYXVsdC5jb20uZXF1aWZheC51cy5sYWJzLmNpYS5hYWFfbW91c3RhY2hlLiJoaXBzdGVydHh0LmNpYS5sYWJzLnVzLmVxdWlmYXguY29tIg:textrecord.domain.com/default',
                      status=200)
        with self.assertRaises(infoblox.InfobloxGeneralException):
            self.iba_ipa.delete_txt_record('badtextrecord.domain.com')

    @responses.activate
    def test_txt_delete_badresponse(self):
        responses.add(responses.GET,
                     'https://10.10.10.10/wapi/v1.6/record:txt',
                      body=self.body,
                      status=500)
        responses.add(responses.DELETE,
                     'https://10.10.10.10/wapi/v1.6/record:txt/ZG5zLmJpbmRfdHh0JC5fZGVmYXVsdC5jb20uZXF1aWZheC51cy5sYWJzLmNpYS5hYWFfbW91c3RhY2hlLiJoaXBzdGVydHh0LmNpYS5sYWJzLnVzLmVxdWlmYXguY29tIg:textrecord.domain.com/default',
                      status=200)
        with self.assertRaises(HTTPError):
            self.iba_ipa.delete_txt_record('textrecord.domain.com')
