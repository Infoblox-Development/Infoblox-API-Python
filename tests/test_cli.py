from click.testing import CliRunner
from infoblox import cli
import responses
try:
    import unittest2 as unittest
except ImportError:
    import unittest
from unittest.mock import patch

def invoke(*args):
    runner = CliRunner()
    basics = ['--ipaddr=1.2.3.4', '--user=user1', '--password=pass1']
    return runner.invoke(cli.cli, basics + list(args))

class CreateCnameTests(unittest.TestCase):

    @patch('infoblox.infoblox.Infoblox.create_cname_record')
    @patch('infoblox.infoblox.Infoblox.__init__', return_value=None)
    def setUp(self, init_mock, create_cname_mock):
        self.init_mock = init_mock
        self.create_cname_mock = create_cname_mock
        self.result = invoke('cname', 'create', 'a', 'b')

    def test_create_cname_called_with_correct_fqdn(self):
        args, __ = self.create_cname_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_create_cname_called_with_correct_name(self):
        args, __ = self.create_cname_mock.call_args
        self.assertEqual(args[1], 'b')

    def test_create_cname_called_exactly_once(self):
        self.assertEqual(self.create_cname_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

    # The following tests actually test just the click group "cli" but due to
    # the nature of click require a full invocation of the command line
    # (otherwise the cli exits with a non-zero exit code and prints the help
    # text). They *could* be included on all test cases, but including them
    # once in this test case is entirely sufficient.
    def test_init_called_with_correct_ipaddr(self):
        args, __ = self.init_mock.call_args
        self.assertEqual(args[0], '1.2.3.4')

    def test_init_called_with_correct_user(self):
        args, __ = self.init_mock.call_args
        self.assertEqual(args[1], 'user1')

    def test_nit_called_with_correct_password(self):
        args, __ = self.init_mock.call_args
        self.assertEqual(args[2], 'pass1')

    def test_init_called_with_default_wapi_version(self):
        args, __ = self.init_mock.call_args
        self.assertEqual(args[3], '1.6')

    def test_init_called_with_default_dns_view(self):
        args, __ = self.init_mock.call_args
        self.assertEqual(args[4], 'default')

    def test_init_called_with_default_network_view(self):
        args, __ = self.init_mock.call_args
        self.assertEqual(args[5], 'default')

    def test_init_called_with_default_verify_ssl(self):
        args, __ = self.init_mock.call_args
        self.assertEqual(args[6], False)

    def test_init_called_exactly_once(self):
        self.assertEqual(self.init_mock.call_count, 1)

class DeleteCnameTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.delete_cname_record')
    def setUp(self, delete_cname_mock):
        self.delete_cname_mock = delete_cname_mock
        self.result = invoke('cname', 'delete', 'a')

    def test_delete_cname_called_with_correct_fqdn(self):
        args, __ = self.delete_cname_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_delete_cname_called_exactly_once(self):
        self.assertEqual(self.delete_cname_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class UpdateCnameTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.update_cname_record')
    def setUp(self, update_cname_mock):
        self.update_cname_mock = update_cname_mock
        self.result = invoke('cname', 'update', 'a', 'b')

    def test_update_cname_called_with_correct_old_fqdn(self):
        args, __ = self.update_cname_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_update_cname_called_with_correct_new_fqdn(self):
        args, __ = self.update_cname_mock.call_args
        self.assertEqual(args[1], 'b')

    def test_update_cname_called_exactly_once(self):
        self.assertEqual(self.update_cname_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class CreateHostrecordTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.create_host_record')
    def setUp(self, create_host_record_mock):
        self.create_host_record_mock = create_host_record_mock
        self.result = invoke('hostrecord', 'create', 'a', 'b')

    def test_create_host_record_called_with_correct_address(self):
        args, __ = self.create_host_record_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_create_host_record_called_with_correct_fqdn(self):
        args, __ = self.create_host_record_mock.call_args
        self.assertEqual(args[1], 'b')

    def test_create_host_record_called_exactly_once(self):
        self.assertEqual(self.create_host_record_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class DeleteHostrecordTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.delete_host_record')
    def setUp(self, delete_host_record_mock):
        self.delete_host_record_mock = delete_host_record_mock
        self.result = invoke('hostrecord', 'delete', 'a')

    def test_delete_host_record_called_with_correct_fqdn(self):
        args, __ = self.delete_host_record_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_delete_host_record_called_exactly_once(self):
        self.assertEqual(self.delete_host_record_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class AddHostaliasTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.add_host_alias')
    def setUp(self, add_host_alias_mock):
        self.add_host_alias_mock = add_host_alias_mock
        self.result = invoke('hostrecord', 'add_alias', 'a', 'b')

    def test_add_host_alias_called_with_correct_host_fqdn(self):
        args, __ = self.add_host_alias_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_add_host_alias_called_with_correct_alias_fqdn(self):
        args, __ = self.add_host_alias_mock.call_args
        self.assertEqual(args[1], 'b')

    def test_add_host_alias_called_exactly_once(self):
        self.assertEqual(self.add_host_alias_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class DeleteHostaliasTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.delete_host_alias')
    def setUp(self, delete_host_alias_mock):
        self.delete_host_alias_mock = delete_host_alias_mock
        self.result = invoke('hostrecord', 'delete_alias', 'a', 'b')

    def test_delete_host_alias_called_with_correct_host_fqdn(self):
        args, __ = self.delete_host_alias_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_delete_host_alias_called_with_correct_host_alias(self):
        args, __ = self.delete_host_alias_mock.call_args
        self.assertEqual(args[1], 'b')

    def test_delete_host_alias_called_exactly_once(self):
        self.assertEqual(self.delete_host_alias_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class GetHostByExtattrsTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.get_host_by_extattrs')
    def setUp(self, get_host_by_extattrs_mock):
        self.get_host_by_extattrs_mock = get_host_by_extattrs_mock
        self.result = invoke('hostrecord', 'by_extattrs', 'a')

    def test_get_host_by_extattrs_called_with_correct_extattrs(self):
        args, __ = self.get_host_by_extattrs_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_get_host_by_extattrs_called_exactly_once(self):
        self.assertEqual(self.get_host_by_extattrs_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class GetHostByRegexpTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.get_host_by_regexp')
    def setUp(self, get_host_by_regexp_mock):
        self.get_host_by_regexp_mock = get_host_by_regexp_mock
        self.result = invoke('hostrecord', 'by_regexp', 'a')

    def test_get_host_by_regexp_called_with_correct_extattrs(self):
        args, __ = self.get_host_by_regexp_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_get_host_by_regexp_called_exactly_once(self):
        self.assertEqual(self.get_host_by_regexp_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class GetHostTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.get_host')
    def setUp(self, get_host_mock):
        self.get_host_mock = get_host_mock
        self.result = invoke('hostrecord', 'get', 'a')

    def test_get_host_called_with_correct_fqdn(self):
        args, __ = self.get_host_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_get_host_called_exactly_once(self):
        self.assertEqual(self.get_host_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class GetHostByIPTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.get_host_by_ip')
    def setUp(self, get_host_by_ip_mock):
        self.get_host_by_ip_mock = get_host_by_ip_mock
        self.result = invoke('hostrecord', 'by_ip', 'a')

    def test_get_host_by_ip_called_with_correct_ip(self):
        args, __ = self.get_host_by_ip_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_get_host_by_ip_called_exactly_once(self):
        self.assertEqual(self.get_host_by_ip_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class GetHostExtattrsTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.get_host_extattrs')
    def setUp(self, get_host_extattrs_mock):
        self.get_host_extattrs_mock = get_host_extattrs_mock
        self.result = invoke('hostrecord', 'extattrs', 'a')

    def test_get_host_extattrs_called_with_correct_fqdn(self):
        args, __ = self.get_host_extattrs_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_get_host_extattrs_called_exactly_once(self):
        self.assertEqual(self.get_host_extattrs_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class CreateNetworkTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.create_network')
    def setUp(self, create_network_mock):
        self.create_network_mock = create_network_mock
        self.result = invoke('network', 'create', 'a')

    def test_create_network_called_with_correct_network(self):
        args, __ = self.create_network_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_create_network_called_exactly_once(self):
        self.assertEqual(self.create_network_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class DeleteNetworkTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.delete_network')
    def setUp(self, delete_network_mock):
        self.delete_network_mock = delete_network_mock
        self.result = invoke('network', 'delete', 'a')

    def test_delete_network_called_with_correct_network(self):
        args, __ = self.delete_network_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_delete_network_called_exactly_once(self):
        self.assertEqual(self.delete_network_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class NextNetworkTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.get_next_available_network')
    def setUp(self, next_network_mock):
        self.next_network_mock = next_network_mock
        self.result = invoke('network', 'next_network', 'a', 'b')

    def test_next_network_called_with_correct_networkcontainer(self):
        args, __ = self.next_network_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_next_network_called_with_correct_cidr(self):
        args, __ = self.next_network_mock.call_args
        self.assertEqual(args[1], 'b')

    def test_next_network_called_exactly_once(self):
        self.assertEqual(self.next_network_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class GetNetworkTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.get_network')
    def setUp(self, get_network_mock):
        self.get_network_mock = get_network_mock
        self.result = invoke('network', 'get', 'a')

    def test_get_network_called_with_correct_network(self):
        args, __ = self.get_network_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_get_network_called_exactly_once(self):
        self.assertEqual(self.get_network_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class GetNetworkByIpTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.get_network_by_ip')
    def setUp(self, get_network_by_ip_mock):
        self.get_network_by_ip_mock = get_network_by_ip_mock
        self.result = invoke('network', 'by_ip', 'a')

    def test_get_network_by_ip_called_with_correct_ip(self):
        args, __ = self.get_network_by_ip_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_get_network_by_ip_called_exactly_once(self):
        self.assertEqual(self.get_network_by_ip_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class GetNetworkByExtattrsTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.get_network_by_extattrs')
    def setUp(self, get_network_by_extattrs_mock):
        self.get_network_by_extattrs_mock = get_network_by_extattrs_mock
        self.result = invoke('network', 'by_extattrs', 'a')

    # def test_get_network_by_extattrs_called_with_correct_extattrs(self):
    #     args, __ = self.get_network_by_extattrs_mock.call_args
    #     self.assertEqual(args[0], 'a')

    def test_get_network_by_extattrs_called_exactly_once(self):
        self.assertEqual(self.get_network_by_extattrs_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class GetNetworkExtattrsTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.get_network_extattrs')
    def setUp(self, get_network_extattrs_mock):
        self.get_network_extattrs_mock = get_network_extattrs_mock
        self.result = invoke('network', 'extattrs', 'a')

    def test_get_network_extattrs_called_with_correct_network(self):
        args, __ = self.get_network_extattrs_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_get_network_extattrs_called_exactly_once(self):
        self.assertEqual(self.get_network_extattrs_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class UpdateNetworkExtattrsTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.update_network_extattrs')
    def setUp(self, update_network_extattrs_mock):
        self.update_network_extattrs_mock = update_network_extattrs_mock
        self.result = invoke('network', 'update_extattrs', 'a', 'b')

    def test_update_network_extattrs_called_with_correct_network(self):
        args, __ = self.update_network_extattrs_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_update_network_extattrs_called_with_correct_extattrs(self):
        args, __ = self.update_network_extattrs_mock.call_args
        self.assertEqual(args[1], 'b')

    def test_update_network_extattrs_called_exactly_once(self):
        self.assertEqual(self.update_network_extattrs_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class DeleteNetworkExtattrsTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.delete_network_extattrs')
    def setUp(self, delete_network_extattrs_mock):
        self.delete_network_extattrs_mock = delete_network_extattrs_mock
        self.result = invoke('network', 'delete_extattrs', 'a', 'b')

    def test_delete_network_extattrs_called_with_correct_network(self):
        args, __ = self.delete_network_extattrs_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_delete_network_extattrs_called_with_correct_extattrs(self):
        args, __ = self.delete_network_extattrs_mock.call_args
        self.assertEqual(args[1], 'b')

    def test_delete_network_extattrs_called_exactly_once(self):
        self.assertEqual(self.delete_network_extattrs_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class CreateNetworkContainerTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.create_networkcontainer')
    def setUp(self, create_network_container_mock):
        self.create_network_container_mock = create_network_container_mock
        self.result = invoke('networkcontainer', 'create', 'a')

    def test_create_network_container_called_with_correct_networkcontainer(self):
        args, __ = self.create_network_container_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_create_network_container_called_exactly_once(self):
        self.assertEqual(self.create_network_container_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class DeleteNetworkContainerTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.delete_networkcontainer')
    def setUp(self, delete_network_container_mock):
        self.delete_network_container_mock = delete_network_container_mock
        self.result = invoke('networkcontainer', 'delete', 'a')

    def test_delete_network_container_called_with_correct_networkcontainer(self):
        args, __ = self.delete_network_container_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_delete_network_container_called_exactly_once(self):
        self.assertEqual(self.delete_network_container_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class CreateTxtRecordTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.create_txt_record')
    def setUp(self, create_txt_record_mock):
        self.create_txt_record_mock = create_txt_record_mock
        self.result = invoke('txtrecord', 'create', 'a', 'b')

    def test_create_txt_record_called_with_correct_text(self):
        args, __ = self.create_txt_record_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_create_txt_record_called_with_correct_fqdn(self):
        args, __ = self.create_txt_record_mock.call_args
        self.assertEqual(args[1], 'b')

    def test_create_txt_record_called_exactly_once(self):
        self.assertEqual(self.create_txt_record_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class DeleteTxtRecordTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.delete_txt_record')
    def setUp(self, delete_txt_record_mock):
        self.delete_txt_record_mock = delete_txt_record_mock
        self.result = invoke('txtrecord', 'delete', 'a')

    def test_delete_txt_record_called_with_correct_fqdn(self):
        args, __ = self.delete_txt_record_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_delete_txt_record_called_exactly_once(self):
        self.assertEqual(self.delete_txt_record_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class GetTxtRecordByRegexpTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.get_txt_by_regexp')
    def setUp(self, get_txt_by_regexp_mock):
        self.get_txt_by_regexp_mock = get_txt_by_regexp_mock
        self.result = invoke('txtrecord', 'by_regexp', 'a')

    def test_get_txt_by_regexp_called_with_correct_regexp(self):
        args, __ = self.get_txt_by_regexp_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_get_txt_by_regexp_called_exactly_once(self):
        self.assertEqual(self.get_txt_by_regexp_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class CreateDhcpRangeTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.create_dhcp_range')
    def setUp(self, create_dhcp_range_mock):
        self.create_dhcp_range_mock = create_dhcp_range_mock
        self.result = invoke('dhcp', 'create', 'a', 'b')

    def test_create_dhcp_range_called_with_correct_start_ip_v4(self):
        args, __ = self.create_dhcp_range_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_create_dhcp_range_called_with_correct_end_ip_v4(self):
        args, __ = self.create_dhcp_range_mock.call_args
        self.assertEqual(args[1], 'b')

    def test_create_dhcp_range_called_exactly_once(self):
        self.assertEqual(self.create_dhcp_range_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class DeleteDhcpRangeTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.delete_dhcp_range')
    def setUp(self, delete_dhcp_range_mock):
        self.delete_dhcp_range_mock = delete_dhcp_range_mock
        self.result = invoke('dhcp', 'delete', 'a', 'b')

    def test_delete_dhcp_range_called_with_correct_start_ip_v4(self):
        args, __ = self.delete_dhcp_range_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_delete_dhcp_range_called_with_correct_end_ip_v4(self):
        args, __ = self.delete_dhcp_range_mock.call_args
        self.assertEqual(args[1], 'b')

    def test_delete_dhcp_range_called_exactly_once(self):
        self.assertEqual(self.delete_dhcp_range_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class GetNextIPTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.get_next_available_ip')
    def setUp(self, get_next_available_ip_mock):
        self.get_next_available_ip_mock = get_next_available_ip_mock
        self.result = invoke('ip', 'next_ip', 'a')

    def test_get_next_available_ip_called_with_correct_network(self):
        args, __ = self.get_next_available_ip_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_get_next_available_ip_called_exactly_once(self):
        self.assertEqual(self.get_next_available_ip_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)

class GetIpByHostTests(unittest.TestCase):
    @patch('infoblox.infoblox.Infoblox.get_ip_by_host')
    def setUp(self, get_ip_by_host_mock):
        self.get_ip_by_host_mock = get_ip_by_host_mock
        self.result = invoke('ip', 'by_host', 'a')

    def test_get_ip_by_host_called_with_correct_fqdn(self):
        args, __ = self.get_ip_by_host_mock.call_args
        self.assertEqual(args[0], 'a')

    def test_get_ip_by_host_called_exactly_once(self):
        self.assertEqual(self.get_ip_by_host_mock.call_count, 1)

    def test_exit_code_is_zero(self):
        self.assertEqual(self.result.exit_code, 0)