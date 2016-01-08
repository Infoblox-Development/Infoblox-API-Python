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

# infoblox.infoblox Module


## infoblox.infoblox.Infoblox Objects



##### `__init__(self, iba_ipaddr, iba_user, iba_password, iba_wapi_version, iba_dns_view, iba_network_view, iba_verify_ssl=False)` 

> Class initialization method
>        :param iba_ipaddr: IBA IP address of management interface
>        :param iba_user: IBA user name
>        :param iba_password: IBA user password
>        :param iba_wapi_version: IBA WAPI version (example: 1.0)
>        :param iba_dns_view: IBA default view
>        :param iba_network_view: IBA default network view
>        :param iba_verify_ssl: IBA SSL certificate validation (example: False)



##### `add_host_alias(self, host_fqdn, alias_fqdn)` 

> Implements IBA REST API call to add an alias to IBA host record
>        :param host_fqdn: host record name in FQDN
>        :param alias_fqdn: host record name in FQDN



##### `create_cname_record(self, canonical, name)` 

> Implements IBA REST API call to create IBA cname record
>        :param canonical: canonical name in FQDN format
>        :param name: the name for a CNAME record in FQDN format



##### `create_dhcp_range(self, start_ip_v4, end_ip_v4)` 

> Implements IBA REST API call to add DHCP range for given
>            start and end addresses
>        :param start_ip_v4: IP v4 address
>        :param end_ip_v4: IP v4 address



##### `create_host_record(self, address, fqdn)` 

> Implements IBA REST API call to create IBA host record
>        Returns IP v4 address assigned to the host
>        :param address: IP v4 address or NET v4 address in CIDR format to get
>            next_available_ip from
>        :param fqdn: hostname in FQDN



##### `create_network(self, network)` 

> Implements IBA REST API call to create DHCP network object
>        :param network: network in CIDR format



##### `create_networkcontainer(self, networkcontainer)` 

> Implements IBA REST API call to create DHCP network containert object
>        :param networkcontainer: network container in CIDR format



##### `create_txt_record(self, text, fqdn)` 

> Implements IBA REST API call to create IBA txt record
>        Returns IP v4 address assigned to the host
>        :param text: free text to be added to the record
>        :param fqdn: hostname in FQDN



##### `delete_cname_record(self, fqdn)` 

> Implements IBA REST API call to delete IBA cname record
>        :param fqdn: cname in FQDN



##### `delete_dhcp_range(self, start_ip_v4, end_ip_v4)` 

> Implements IBA REST API call to delete DHCP range for given
>            start and end addresses
>        :param start_ip_v4: IP v4 address
>        :param end_ip_v4: IP v4 address



##### `delete_host_alias(self, host_fqdn, alias_fqdn)` 

> Implements IBA REST API call to add an alias to IBA host record
>        :param host_fqdn: host record name in FQDN
>        :param alias_fqdn: host record name in FQDN



##### `delete_host_record(self, fqdn)` 

> Implements IBA REST API call to delete IBA host record
>        :param fqdn: hostname in FQDN



##### `delete_network(self, network)` 

> Implements IBA REST API call to delete DHCP network object
>        :param network: network in CIDR format



##### `delete_network_extattrs(self, network, attributes)` 

> Implements IBA REST API call to delete network extensible attributes
>        :param network: network in CIDR format
>        :param attributes: array of extensible attribute names



##### `delete_networkcontainer(self, networkcontainer)` 

> Implements IBA REST API call to delete DHCP network container object
>        :param networkcontainer: network container in CIDR format



##### `delete_txt_record(self, fqdn)` 

> Implements IBA REST API call to delete IBA TXT record
>        :param fqdn: hostname in FQDN



##### `get_host(self, fqdn, fields=None)` 

> Implements IBA REST API call to retrieve host record fields
>        Returns hash table of fields with field name as a hash key
>        :param fqdn: hostname in FQDN
>        :param fields: comma-separated list of field names (optional)



##### `get_host_by_extattrs(self, attributes)` 

> Implements IBA REST API call to find host by it's extensible attributes
>        Returns array of hosts in FQDN
>        :param attributes: comma-separated list of attrubutes name/value
>            pairs in the format:
>            attr_name=attr_value - exact match for attribute value
>            attr_name:=attr_value - case insensitive match for attribute value
>            attr_name~=regular_expression - match attribute value by regular
>                expression
>            attr_name>=attr_value - search by number greater than value
>            attr_name<=attr_value - search by number less than value
>            attr_name!=attr_value - search by number not equal of value



##### `get_host_by_ip(self, ip_v4)` 

> Implements IBA REST API call to find hostname by IP address
>        Returns array of host names in FQDN associated with given IP address
>        :param ip_v4: IP v4 address



##### `get_host_by_regexp(self, fqdn)` 

> Implements IBA REST API call to retrieve host records by fqdn regexp filter
>        Returns array of host names in FQDN matched to given regexp filter
>        :param fqdn: hostname in FQDN or FQDN regexp filter



##### `get_host_extattrs(self, fqdn, attributes=None)` 

> Implements IBA REST API call to retrieve host extensible attributes
>        Returns hash table of attributes with attribute name as a hash key
>        :param fqdn: hostname in FQDN
>        :param attributes: array of extensible attribute names (optional)



##### `get_ip_by_host(self, fqdn)` 

> Implements IBA REST API call to find IP addresses by hostname
>        Returns array of IP v4 addresses associated with given hostname
>        :param fqdn: hostname in FQDN



##### `get_network(self, network, fields=None)` 

> Implements IBA REST API call to retrieve network object fields
>        Returns hash table of fields with field name as a hash key
>        :param network: network in CIDR format
>        :param fields: comma-separated list of field names
>            (optional, returns network in CIDR format and netmask if
>             not specified)



##### `get_network_by_extattrs(self, attributes)` 

> Implements IBA REST API call to find a network by it's
>            extensible attributes
>        Returns array of networks in CIDR format
>        :param attributes: comma-separated list of attrubutes name/value
>            pairs in the format:
>            attr_name=attr_value - exact match for attribute value
>            attr_name:=attr_value - case insensitive match for attribute value
>            attr_name~=regular_expression - match attribute value by regular
>                expression
>            attr_name>=attr_value - search by number greater than value
>            attr_name<=attr_value - search by number less than value
>            attr_name!=attr_value - search by number not equal of value



##### `get_network_by_ip(self, ip_v4)` 

> Implements IBA REST API call to find network by IP address which
>            belongs to this network
>        Returns network in CIDR format
>        :param ip_v4: IP v4 address



##### `get_network_extattrs(self, network, attributes=None)` 

> Implements IBA REST API call to retrieve network extensible attributes
>        Returns hash table of attributes with attribute name as a hash key
>        :param network: network in CIDR format
>        :param attributes: array of extensible attribute names (optional)



##### `get_next_available_ip(self, network)` 

> Implements IBA next_available_ip REST API call
>        Returns IP v4 address
>        :param network: network in CIDR format



##### `get_next_available_network(self, networkcontainer, cidr)` 

> Implements IBA REST API call to retrieve next available network
>            of network container
>        Returns network address in CIDR format
>        :param networkcontainer: network container address in CIDR format
>        :param cidr: requested network length (from 0 to 32)



##### `get_txt_by_regexp(self, fqdn)` 

> Implements IBA REST API call to retrieve TXT records by fqdn
>            regexp filter
>        Returns dictonary of host names in FQDN matched to given regexp
>            filter with the TXT value
>        :param fqdn: hostname in FQDN or FQDN regexp filter



##### `update_cname_record(self, canonical, name)` 

> Implements IBA REST API call to update or repoint IBA cname record
>        :param canonical: canonical name in FQDN format
>        :param name: the name for the new CNAME record in FQDN format



##### `update_network_extattrs(self, network, attributes)` 

> Implements IBA REST API call to add or update network extensible attributes
>        :param network: network in CIDR format
>        :param attributes: hash table of extensible attributes with attribute
>            name as a hash key



## infoblox.infoblox.InfobloxBadInputParameter Objects



## infoblox.infoblox.InfobloxGeneralException Objects



## infoblox.infoblox.InfobloxNoIPavailableException Objects



## infoblox.infoblox.InfobloxNoNetworkAvailableException Objects



## infoblox.infoblox.InfobloxNotFoundException Objects


