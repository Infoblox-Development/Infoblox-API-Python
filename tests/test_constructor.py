from infoblox import infoblox
from . import testcasefixture


class TestConstructor(testcasefixture.TestCaseWithFixture):
    fixture_name = 'alias_add'

    @classmethod
    def setUpClass(cls):
        super(TestConstructor, cls).setUpClass()


    def test_iba_host_is_set_from_init(self):
        self.assertEqual(self.iba_ipa.iba_host, '10.10.10.10')

    def test_iba_user_set_from_init(self):
        self.assertEqual(self.iba_ipa.iba_user, 'foo')

    def test_iba_password_set_from_init(self):
        self.assertEqual(self.iba_ipa.iba_password, 'bar')

    def test_iba_wapi_version_set_from_init(self):
        self.assertEqual(self.iba_ipa.iba_wapi_version, '1.6')

    def test_iba_dns_view_set_from_init(self):
        self.assertEqual(self.iba_ipa.iba_dns_view, 'default')

    def test_iba_network_view_set_from_init(self):
        self.assertEqual(self.iba_ipa.iba_network_view, 'default')
