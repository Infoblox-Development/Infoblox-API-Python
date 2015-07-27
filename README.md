# Infoblox API

This project implements the subset of Infoblox API via REST API

## Infoblox API python module

Class **Infoblox** implements the following methods:

- create_network
- delete_network
- create_networkcontainer
- delete_networkcontainer
- get_next_available_network
- create_host_record
- create_txt_record
- delete_host_record
- delete_txt_record
- add_host_alias
- delete_host_alias
- create_cname_record
- delete_cname_record
- update_cname_record
- create_dhcp_range
- delete_dhcp_range
- get_next_available_ip
- get_host
- get_host_by_ip
- get_ip_by_host
- get_host_by_extattrs
- get_host_by_regexp
- get_txt_by_regexp
- get_host_extattrs
- get_network
- get_network_by_ip
- get_network_by_extattrs
- get_network_extattrs
- update_network_extattrs
- delete_network_extattrs

* * *

### How to use

Example:

```
import infoblox

iba_api = infoblox.Infoblox('10.10.20.32', 'admin', 'secret', '1.6', 'internal', 'default')

try:
    ip = iba_api.create_host_record('192.168.0.0/24', 'mytest.example.com')
    print ip
except Exception as e:
    print e

```
