import unittest 
import unittest.mock
import click
import cli 


class TestCli(unittest.TestCase):

    @patch('cli.get_host.api')
    def test_get_host(self, _api):
        fqdn = 'test fqdn'
        cli.get_host(fqdn)
        _api.return_value.get_host.assert_called_with(fqdn)



