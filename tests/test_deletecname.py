import responses
from requests.exceptions import HTTPError
from infoblox import infoblox
from . import testcasefixture


class TestDeleteCname(testcasefixture.TestCaseWithFixture):
    fixture_name = 'cname_delete'

    @classmethod
    def setUpClass(cls):
        super(TestDeleteCname, cls).setUpClass()
        with responses.RequestsMock() as res:
            res.add(responses.GET,
                    'https://10.10.10.10/wapi/v1.6/record:cname',
                    body=cls.body,
                    status=200)
            res.add(responses.DELETE,
                    'https://10.10.10.10/wapi/v1.6/record:cname/ZG5zLmJpbmRfY25hbWUkLl9kZWZhdWx0LmNvbS5lcXVpZmF4LnVzLmxhYnMuY2lhLmFhYWNuYW1ldGVzdA:cname.domain.com/default',
                    status=200)
            cls.ip = cls.iba_ipa.delete_cname_record('cname.domain.com')

    def test_cname_delete(self):
        self.assertIsNone(self.ip)

    @responses.activate
    def test_cname_delete_badhostname(self):
        responses.add(responses.GET,
                      'https://10.10.10.10/wapi/v1.6/record:cname',
                      body='[]',
                      status=200)
        responses.add(responses.DELETE,
                      'https://10.10.10.10/wapi/v1.6/record:cname/ZG5zLmJpbmRfY25hbWUkLl9kZWZhdWx0LmNvbS5lcXVpZmF4LnVzLmxhYnMuY2lhLmFhYWNuYW1ldGVzdA:cname.domain.com/default',
                      status=200)
        with self.assertRaises(infoblox.InfobloxNotFoundException):
            self.iba_ipa.delete_cname_record('nocname.domain.com')

    @responses.activate
    def test_cname_delete_unexpected(self):
        responses.add(responses.GET,
                      'https://10.10.10.10/wapi/v1.6/record:cname',
                      body=self.body,
                      status=200)
        responses.add(responses.DELETE,
                      'https://10.10.10.10/wapi/v1.6/record:cname/ZG5zLmJpbmRfY25hbWUkLl9kZWZhdWx0LmNvbS5lcXVpZmF4LnVzLmxhYnMuY2lhLmFhYWNuYW1ldGVzdA:cname.domain.com/default',
                      status=200)
        with self.assertRaises(infoblox.InfobloxGeneralException):
            self.iba_ipa.delete_cname_record('genexp.domain.com')

    @responses.activate
    def test_cname_delete_bad_response(self):
        responses.add(responses.GET,
                      'https://10.10.10.10/wapi/v1.6/record:cname',
                      body=self.body,
                      status=500)
        responses.add(responses.DELETE,
                      'https://10.10.10.10/wapi/v1.6/record:cname/ZG5zLmJpbmRfY25hbWUkLl9kZWZhdWx0LmNvbS5lcXVpZmF4LnVzLmxhYnMuY2lhLmFhYWNuYW1ldGVzdA:cname.domain.com/default',
                      status=200)
        with self.assertRaises(HTTPError):
            self.iba_ipa.delete_cname_record('cname.domain.com')
