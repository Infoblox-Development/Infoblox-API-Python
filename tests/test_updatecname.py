import responses
from requests.exceptions import HTTPError
from infoblox import infoblox
from . import testcasefixture


class TestUpdateCname(testcasefixture.TestCaseWithFixture):
    fixture_name = 'cname_update'

    @classmethod
    def setUpClass(cls):
        super(TestUpdateCname, cls).setUpClass()
        with responses.RequestsMock() as res:
            res.add(responses.GET,
                    'https://10.10.10.10/wapi/v1.6/record:cname',
                    body=cls.body,
                    status=200)
            res.add(responses.PUT,
                    'https://10.10.10.10/wapi/v1.6/record:cname/ZG5zLmJpbmRfY25hbWUkLl9kZWZhdWx0LmNvbS5lcXVpZmF4LnVzLmxhYnMuY2lhLmFhYWNuYW1ldGVzdA:cname.domain.com/default',
                    body='',
                    status=200)
            cls.ip = cls.iba_ipa.update_cname_record('newtarget.domain.com',
                                                     'cname.domain.com')

    def test_cname_update(self):
        self.assertIsNone(self.ip)

    @responses.activate
    def test_cname_update_nocname(self):
        responses.add(responses.GET,
                      'https://10.10.10.10/wapi/v1.6/record:cname',
                      body='[]',
                      status=200)
        responses.add(responses.PUT,
                      'https://10.10.10.10/wapi/v1.6/record:cname/ZG5zLmJpbmRfY25hbWUkLl9kZWZhdWx0LmNvbS5lcXVpZmF4LnVzLmxhYnMuY2lhLmFhYWNuYW1ldGVzdA:cname.domain.com/default',
                      body='',
                      status=200)
        with self.assertRaises(infoblox.InfobloxNotFoundException):
            ip = self.iba_ipa.update_cname_record('newtarget.domain.com',
                                                  'nocname.domain.com')

    @responses.activate
    def test_cname_update_other(self):
        responses.add(responses.GET,
                      'https://10.10.10.10/wapi/v1.6/record:cname',
                      body='{"text": "don\'t ever trust the needle"}',
                      status=203)
        responses.add(responses.PUT,
                      'https://10.10.10.10/wapi/v1.6/record:cname/ZG5zLmJpbmRfY25hbWUkLl9kZWZhdWx0LmNvbS5lcXVpZmF4LnVzLmxhYnMuY2lhLmFhYWNuYW1ldGVzdA:cname.domain.com/default',
                      body='',
                      status=200)
        with self.assertRaises(infoblox.InfobloxGeneralException):
            self.iba_ipa.update_cname_record('badtarget.domain.com',
                                             'cname.domain.com')

    @responses.activate
    def test_cname_update_badupdate(self):
        responses.add(responses.GET,
                      'https://10.10.10.10/wapi/v1.6/record:cname',
                      body=self.body,
                      status=200)
        responses.add(responses.PUT,
                      'https://10.10.10.10/wapi/v1.6/record:cname/ZG5zLmJpbmRfY25hbWUkLl9kZWZhdWx0LmNvbS5lcXVpZmF4LnVzLmxhYnMuY2lhLmFhYWNuYW1ldGVzdA:cname.domain.com/default',
                      body='',
                      status=500)
        with self.assertRaises(HTTPError):
            self.iba_ipa.update_cname_record('newtarget.domain.com',
                                             'cname.domain.com')

    @responses.activate
    def test_cname_update_nocname(self):
        responses.add(responses.GET,
                      'https://10.10.10.10/wapi/v1.6/record:cname',
                      body='[]',
                      status=200)
        responses.add(responses.PUT,
                      'https://10.10.10.10/wapi/v1.6/record:cname/ZG5zLmJpbmRfY25hbWUkLl9kZWZhdWx0LmNvbS5lcXVpZmF4LnVzLmxhYnMuY2lhLmFhYWNuYW1ldGVzdA:cname.domain.com/default',
                      body='',
                      status=200)
        with self.assertRaises(infoblox.InfobloxNotFoundException):
            ip = self.iba_ipa.update_cname_record('newtarget.domain.com',
                                                  'nocname.domain.com')
