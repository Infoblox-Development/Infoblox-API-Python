#
# Copyright 2014 "Igor Feoktistov" <ifeoktistov@yahoo.com>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import re
import requests
import json

class InfobloxNotFoundException(Exception):
    pass

class InfobloxNoIPavailableException(Exception):
    pass

class InfobloxNoNetworkAvailableException(Exception):
    pass

class InfobloxGeneralException(Exception):
    pass

class InfobloxBadInputParameter(Exception):
    pass

class Infoblox(object):
    """ Implements the following subset of Infoblox IPAM API via REST API
	create_network
	delete_network
	create_networkcontainer
	delete_networkcontainer
	get_next_available_network
	create_host_record
	create_txt_record
	delete_txt_record
	delete_host_record
	add_host_alias
	delete_host_alias
	create_cname_record
	delete_cname_record
        update_cname_record
	create_dhcp_range
	delete_dhcp_range
	get_next_available_ip
	get_host
	get_host_by_ip
	get_ip_by_host
	get_host_by_regexp
	get_txt_by_regexp
	get_host_by_extattrs
	get_host_extattrs
	get_network
	get_network_by_ip
	get_network_by_extattrs
	get_network_extattrs
	update_network_extattrs
	delete_network_extattrs
    """

    def __init__(self, iba_ipaddr, iba_user, iba_password, iba_wapi_version, iba_dns_view, iba_network_view, iba_verify_ssl=False):
	""" Class initialization method
	:param iba_ipaddr: IBA IP address of management interface
	:param iba_user: IBA user name
	:param iba_password: IBA user password
	:param iba_wapi_version: IBA WAPI version (example: 1.0)
	:param iba_dns_view: IBA default view
	:param iba_network_view: IBA default network view
        :param iba_verify_ssl: IBA SSL certificate validation (example: False)
	"""
	self.iba_host = iba_ipaddr
	self.iba_user = iba_user
	self.iba_password = iba_password
	self.iba_wapi_version = iba_wapi_version
	self.iba_dns_view = iba_dns_view
	self.iba_network_view = iba_network_view
        self.iba_verify_ssl = iba_verify_ssl

    def get_next_available_ip(self, network):
	""" Implements IBA next_available_ip REST API call
	Returns IP v4 address
	:param network: network in CIDR format
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/network?network=' + network + '&network_view=' + self.iba_network_view
	try:
	    r = requests.get(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
	    r_json = r.json()
	    if r.status_code == 200:
		if len(r_json) > 0:
		    net_ref = r_json[0]['_ref']
		    rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/' + net_ref + '?_function=next_available_ip&num=1'
		    r = requests.post(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
		    r_json = r.json()
		    if r.status_code == 200:
			ip_v4 = r_json['ips'][0]
			return ip_v4
		    else:
			if 'text' in r_json:
			    if 'code' in r_json and r_json['code'] == 'Client.Ibap.Data':
				raise InfobloxNoIPavailableException(r_json['text'])
			    else:
				raise InfobloxGeneralException(r_json['text'])
			else:
			    r.raise_for_status()
		else:
		    raise InfobloxNotFoundException("No requested network found: " + network)
	    else:
		if 'text' in r_json:
		    raise InfobloxGeneralException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def create_host_record(self, address, fqdn):
	""" Implements IBA REST API call to create IBA host record
	Returns IP v4 address assigned to the host
	:param address: IP v4 address or NET v4 address in CIDR format to get next_available_ip from
	:param fqdn: hostname in FQDN
	"""
	if re.match("^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\/[0-9]+$", address):
	    ipv4addr = 'func:nextavailableip:' + address
	else:
	    if re.match("^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$", address):
		ipv4addr = address
	    else:
		raise InfobloxBadInputParameter('Expected IP or NET address in CIDR format')
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/record:host' + '?_return_fields=ipv4addrs'
	payload = '{"ipv4addrs": [{"configure_for_dhcp": false,"ipv4addr": "' + ipv4addr + '"}],"name": "' + fqdn + '","view": "' + self.iba_dns_view + '"}'
	try:
	    r = requests.post(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl, data=payload)
	    r_json = r.json()
	    if r.status_code == 200 or r.status_code == 201:
	    	return r_json['ipv4addrs'][0]['ipv4addr']
	    else:
		if 'text' in r_json:
		    raise InfobloxGeneralException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def create_txt_record(self, text, fqdn):
	""" Implements IBA REST API call to create IBA txt record
	Returns IP v4 address assigned to the host
	:param text: free text to be added to the record
	:param fqdn: hostname in FQDN
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/record:txt'
	payload = '{"text": "' +  text + '","name": "' + fqdn + '","view": "' + self.iba_dns_view + '"}'
	try:
	    r = requests.post(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl, data=payload)
	    r_json = r.json()
	    if r.status_code == 200 or r.status_code == 201:
	    	return
	    else:
		if 'text' in r_json:
		    raise InfobloxGeneralException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def delete_host_record(self, fqdn):
	""" Implements IBA REST API call to delete IBA host record
	:param fqdn: hostname in FQDN
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/record:host?name=' + fqdn + '&view=' + self.iba_dns_view
	try:
	    r = requests.get(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
	    r_json = r.json()
	    if r.status_code == 200:
		if len(r_json) > 0:
		    host_ref = r_json[0]['_ref']
		    if host_ref and re.match("record:host\/[^:]+:([^\/]+)\/", host_ref).group(1) == fqdn:
			rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/' + host_ref
			r = requests.delete(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
			if r.status_code == 200:
			    return
			else:
			    if 'text' in r_json:
				raise InfobloxGeneralException(r_json['text'])
			    else:
				r.raise_for_status()
		    else:
			raise InfobloxGeneralException("Received unexpected host reference: " + host_ref)
		else:
		    raise InfobloxNotFoundException("No requested host found: " + fqdn)
	    else:
		if 'text' in r_json:
		    raise InfobloxGeneralException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def delete_txt_record(self, fqdn):
	""" Implements IBA REST API call to delete IBA TXT record
	:param fqdn: hostname in FQDN
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/record:txt?name=' + fqdn + '&view=' + self.iba_dns_view
	try:
	    r = requests.get(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
	    r_json = r.json()
	    if r.status_code == 200:
		if len(r_json) > 0:
		    host_ref = r_json[0]['_ref']
		    if host_ref and re.match("record:txt\/[^:]+:([^\/]+)\/", host_ref).group(1) == fqdn:
			rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/' + host_ref
			r = requests.delete(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
			if r.status_code == 200:
			    return
			else:
			    if 'text' in r_json:
				raise InfobloxGeneralException(r_json['text'])
			    else:
				r.raise_for_status()
		    else:
			raise InfobloxGeneralException("Received unexpected host reference: " + host_ref)
		else:
		    raise InfobloxNotFoundException("No requested host found: " + fqdn)
	    else:
		if 'text' in r_json:
		    raise InfobloxGeneralException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def add_host_alias(self, host_fqdn, alias_fqdn):
	""" Implements IBA REST API call to add an alias to IBA host record
	:param host_fqdn: host record name in FQDN
	:param alias_fqdn: host record name in FQDN
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/record:host?name=' + host_fqdn + '&view=' + self.iba_dns_view + '&_return_fields=name,aliases'
	try:
	    r = requests.get(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
	    r_json = r.json()
	    if r.status_code == 200:
		if len(r_json) > 0:
		    host_ref = r_json[0]['_ref']
		    if host_ref and re.match("record:host\/[^:]+:([^\/]+)\/", host_ref).group(1) == host_fqdn:
			if 'aliases' in r_json[0]:
			    aliases = r_json[0]['aliases']
			    aliases.append(alias_fqdn)
			    payload = '{"aliases": ' + json.JSONEncoder().encode(aliases) + '}'
			else:
			    payload = '{"aliases": ["' + alias_fqdn + '"]}'
			rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/' + host_ref
			r = requests.put(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl, data=payload)
			if r.status_code == 200:
			    return
			else:
			    if 'text' in r_json:
				raise InfobloxGeneralException(r_json['text'])
			    else:
				r.raise_for_status()
		    else:
			raise InfobloxGeneralException("Received unexpected host reference: " + host_ref)
		else:
		    raise InfobloxNotFoundException("No requested host found: " + host_fqdn)
	    else:
		if 'text' in r_json:
		    raise InfobloxGeneralException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def delete_host_alias(self, host_fqdn, alias_fqdn):
	""" Implements IBA REST API call to add an alias to IBA host record
	:param host_fqdn: host record name in FQDN
	:param alias_fqdn: host record name in FQDN
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/record:host?name=' + host_fqdn + '&view=' + self.iba_dns_view + '&_return_fields=name,aliases'
	try:
	    r = requests.get(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
	    r_json = r.json()
	    if r.status_code == 200:
		if len(r_json) > 0:
		    host_ref = r_json[0]['_ref']
		    if host_ref and re.match("record:host\/[^:]+:([^\/]+)\/", host_ref).group(1) == host_fqdn:
			if 'aliases' in r_json[0]:
			    aliases = r_json[0]['aliases']
			    aliases.remove(alias_fqdn)
			    payload = '{"aliases": ' + json.JSONEncoder().encode(aliases) + '}'
			    rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/' + host_ref
			    r = requests.put(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl, data=payload)
			    if r.status_code == 200:
				return
			    else:
				if 'text' in r_json:
				    raise InfobloxGeneralException(r_json['text'])
				else:
				    r.raise_for_status()
			else:
			    raise InfobloxNotFoundException("No requested host alias found: " + alias_fqdn)
		    else:
			raise InfobloxGeneralException("Received unexpected host reference: " + host_ref)
		else:
		    raise InfobloxNotFoundException("No requested host found: " + host_fqdn)
	    else:
		if 'text' in r_json:
		    raise InfobloxGeneralException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def create_cname_record(self, canonical, name):
	""" Implements IBA REST API call to create IBA cname record
	:param canonical: canonical name in FQDN format
	:param name: the name for a CNAME record in FQDN format
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/record:cname'
	payload = '{"canonical": "' + canonical + '","name": "' + name + '","view": "' + self.iba_dns_view + '"}'
	try:
	    r = requests.post(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl, data=payload)
	    r_json = r.json()
	    if r.status_code == 200 or r.status_code == 201:
		return
	    else:
		if 'text' in r_json:
		    raise InfobloxGeneralException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def delete_cname_record(self, fqdn):
	""" Implements IBA REST API call to delete IBA cname record
	:param fqdn: cname in FQDN
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/record:cname?name=' + fqdn + '&view=' + self.iba_dns_view
	try:
	    r = requests.get(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
	    r_json = r.json()
	    if r.status_code == 200:
		if len(r_json) > 0:
		    cname_ref = r_json[0]['_ref']
		    if cname_ref and re.match("record:cname\/[^:]+:([^\/]+)\/", cname_ref).group(1) == fqdn:
			rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/' + cname_ref
			r = requests.delete(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
			if r.status_code == 200:
			    return
			else:
			    if 'text' in r_json:
				raise InfobloxGeneralException(r_json['text'])
			    else:
				r.raise_for_status()
		    else:
			raise InfobloxGeneralException("Received unexpected cname record  reference: " + cname_ref)
		else:
		    raise InfobloxNotFoundException("No requested cname record found: " + fqdn)
	    else:
		if 'text' in r_json:
		    raise InfobloxGeneralException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def update_cname_record(self, canonical, name):
        """ Implements IBA REST API call to update or repoint IBA cname record
        :param canonical: canonical name in FQDN format
        :param name: the name for the new CNAME record in FQDN format
        """
        rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/record:cname'
        payload = json.dumps({'name': name})
        try:
            r = requests.get(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl, data=payload)
            r_json = r.json()
            # RFC1912 - A CNAME can not coexist with any other data, we should expect utmost one entry
            if r.status_code == 200 and len(r_json) == 1:
                ibx_cname = r.json()[0]
                cname_ref = ibx_cname['_ref']
                payload = '{"canonical": ' + json.JSONEncoder().encode(canonical) + '}'
                rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/' + cname_ref
                r = requests.put(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl, data=payload)
                if r.status_code == 200 or r.status_code == 201:
                    return
                else:
                    r.raise_for_status()
            elif len(r_json) == 0:
              raise InfobloxNotFoundException("CNAME: " + name + " not found.")
            else:
                if 'text' in r_json:
                    raise InfobloxGeneralException(r_json['text'])
                else:
                    r.raise_for_status()
        except ValueError:
            raise Exception(r)
        except Exception:
            raise

    def create_dhcp_range(self, start_ip_v4, end_ip_v4):
	""" Implements IBA REST API call to add DHCP range for given start and end addresses
	:param start_ip_v4: IP v4 address
	:param end_ip_v4: IP v4 address
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/range'
	payload = '{"start_addr": "' + start_ip_v4 + '","end_addr": "' + end_ip_v4 + '"}'
	try:
	    r = requests.post(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl, data=payload)
	    r_json = r.json()
	    if r.status_code == 200 or r.status_code == 201:
		return
	    else:
		if 'text' in r_json:
		    raise InfobloxGeneralException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def delete_dhcp_range(self, start_ip_v4, end_ip_v4):
	""" Implements IBA REST API call to delete DHCP range for given start and end addresses
	:param start_ip_v4: IP v4 address
	:param end_ip_v4: IP v4 address
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/range?start_addr=' + start_ip_v4 + '?end_addr=' + end_ip_v4 + '&network_view=' + self.iba_network_view
	try:
	    r = requests.get(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
	    r_json = r.json()
	    if r.status_code == 200:
		if len(r_json) > 0:
		    range_ref = r_json[0]['_ref']
		    if range_ref:
			rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/' + range_ref
			r = requests.delete(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
			if r.status_code == 200:
			    return
			else:
			    if 'text' in r_json:
				raise InfobloxGeneralException(r_json['text'])
			    else:
				r.raise_for_status()
		    else:
			raise InfobloxGeneralException("No range reference received in IBA reply")
		else:
		    raise InfobloxNotFoundException("No requested range found: " + start_ip_v4 + "-" + end_ip_v4)
	    else:
		if 'text' in r_json:
		    raise InfobloxGeneralException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def get_host(self, fqdn, fields=None):
	""" Implements IBA REST API call to retrieve host record fields
	Returns hash table of fields with field name as a hash key
	:param fqdn: hostname in FQDN
	:param fields: comma-separated list of field names (optional)
	"""
	if fields:
	    rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/record:host?name=' + fqdn + '&view=' + self.iba_dns_view + '&_return_fields=' + fields
	else:
	    rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/record:host?name=' + fqdn + '&view=' + self.iba_dns_view
	try:
	    r = requests.get(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
	    r_json = r.json()
	    if r.status_code == 200:
		if len(r_json) > 0:
		    return r_json[0]
		else:
		    raise InfobloxNotFoundException("No hosts found: " + fqdn)
	    else:
		if 'text' in r_json:
		    raise InfobloxNotFoundException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def get_host_by_regexp(self, fqdn):
	""" Implements IBA REST API call to retrieve host records by fqdn regexp filter
	Returns array of host names in FQDN matched to given regexp filter
	:param fqdn: hostname in FQDN or FQDN regexp filter
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/record:host?name~=' + fqdn + '&view=' + self.iba_dns_view
	hosts = []
	try:
	    r = requests.get(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
	    r_json = r.json()
	    if r.status_code == 200:
		if len(r_json) > 0:
		    for host in r_json:
			hosts.append(host['name'])
		    return hosts
		else:
		    raise InfobloxNotFoundException("No hosts found for regexp filter: " + fqdn)
	    else:
		if 'text' in r_json:
		    raise InfobloxGeneralException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def get_txt_by_regexp(self, fqdn):
	""" Implements IBA REST API call to retrieve TXT records by fqdn regexp filter
	Returns dictonary of host names in FQDN matched to given regexp filter with the TXT value
	:param fqdn: hostname in FQDN or FQDN regexp filter
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/record:txt?name~=' + fqdn + '&view=' + self.iba_dns_view
	hosts = {}
	try:
	    r = requests.get(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
	    r_json = r.json()
	    if r.status_code == 200:
		if len(r_json) > 0:
		    for host in r_json:
			hosts[host['name']] = host['text']
		    return hosts
		else:
		    raise InfobloxNotFoundException("No txt records found for regexp filter: " + fqdn)
	    else:
		if 'text' in r_json:
		    raise InfobloxGeneralException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def get_host_by_ip(self, ip_v4):
	""" Implements IBA REST API call to find hostname by IP address
	Returns array of host names in FQDN associated with given IP address
	:param ip_v4: IP v4 address
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/ipv4address?ip_address=' + ip_v4 + '&network_view=' + self.iba_network_view
	try:
	    r = requests.get(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
	    r_json = r.json()
	    if r.status_code == 200:
		if len(r_json) > 0:
		    if len(r_json[0]['names']) > 0:
			return r_json[0]['names']
		    else:
			raise InfobloxNotFoundException("No host records found for IP: " + ip_v4)
		else:
		    raise InfobloxNotFoundException("No IP found: " + ip_v4)
	    else:
		if 'text' in r_json:
		    raise InfobloxGeneralException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def get_ip_by_host(self, fqdn):
	""" Implements IBA REST API call to find IP addresses by hostname
	Returns array of IP v4 addresses associated with given hostname
	:param fqdn: hostname in FQDN
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/record:host?name=' + fqdn + '&view=' + self.iba_dns_view
	ipv4addrs = []
	try:
	    r = requests.get(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
	    r_json = r.json()
	    if r.status_code == 200:
		if len(r_json) > 0:
		    if len(r_json[0]['ipv4addrs']) > 0:
			for ipv4addr in r_json[0]['ipv4addrs']:
			    ipv4addrs.append(ipv4addr['ipv4addr'])
			return ipv4addrs
		    else:
			raise InfobloxNotFoundException("No host records found for FQDN: " + fqdn)
		else:
		    raise InfobloxNotFoundException("No hosts found: " + fqdn)
	    else:
		if 'text' in r_json:
		    raise InfobloxGeneralException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def get_host_extattrs(self, fqdn, attributes=None):
	""" Implements IBA REST API call to retrieve host extensible attributes
	Returns hash table of attributes with attribute name as a hash key
	:param fqdn: hostname in FQDN
	:param attributes: array of extensible attribute names (optional)
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/record:host?name=' + fqdn + '&view=' + self.iba_dns_view + '&_return_fields=name,extattrs'
	try:
	    r = requests.get(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
	    r_json = r.json()
	    if r.status_code == 200:
		if len(r_json) > 0:
		    extattrs = {}
		    if attributes:
			for attribute in attributes:
			    if attribute in r_json[0]['extattrs']:
				extattrs[attribute] = r_json[0]['extattrs'][attribute]['value']
			    else:
				raise InfobloxNotFoundException("No requested attribute found: " + attribute)
		    else:
			for attribute in r_json[0]['extattrs'].keys():
			    extattrs[attribute] = r_json[0]['extattrs'][attribute]['value']
		    return extattrs
		else:
		    raise InfobloxNotFoundException("No requested host found: " + fqdn)
	    else:
		if 'text' in r_json:
		    raise InfobloxNotFoundException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def get_network(self, network, fields=None):
	""" Implements IBA REST API call to retrieve network object fields
	Returns hash table of fields with field name as a hash key
	:param network: network in CIDR format
	:param fields: comma-separated list of field names
			(optional, returns network in CIDR format and netmask if not specified)
	"""
	if not fields:
	    fields = 'network,netmask'
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/network?network=' + network + '&network_view=' + self.iba_network_view + '&_return_fields=' + fields
	try:
	    r = requests.get(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
	    r_json = r.json()
	    if r.status_code == 200:
		if len(r_json) > 0:
		    return r_json[0]
		else:
		    raise InfobloxNotFoundException("No requested network found: " + network)
	    else:
		if 'text' in r_json:
		    raise InfobloxNotFoundException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def get_network_by_ip(self, ip_v4):
	""" Implements IBA REST API call to find network by IP address which belongs to this network
	Returns network in CIDR format
	:param ip_v4: IP v4 address
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/ipv4address?ip_address=' + ip_v4 + '&network_view=' + self.iba_network_view
	try:
	    r = requests.get(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
	    r_json = r.json()
	    if r.status_code == 200:
		if len(r_json) > 0:
		    if 'network' in r_json[0]:
			return r_json[0]['network']
		    else:
			raise InfobloxNotFoundException("No network found for IP: " + ip_v4)
		else:
		    raise InfobloxNotFoundException("No IP found: " + ip_v4)
	    else:
		if 'text' in r_json:
		    raise InfobloxNotFoundException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def get_network_by_extattrs(self, attributes):
	""" Implements IBA REST API call to find a network by it's extensible attributes
	Returns array of networks in CIDR format
	:param attributes: comma-separated list of attrubutes name/value pairs in the format:
		attr_name=attr_value - exact match for attribute value
		attr_name:=attr_value - case insensitive match for attribute value
		attr_name~=regular_expression - match attribute value by regular expression
		attr_name>=attr_value - search by number greater than value
		attr_name<=attr_value - search by number less than value
		attr_name!=attr_value - search by number not equal of value
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/network?*' + "&*".join(attributes.split(",")) + '&network_view=' + self.iba_network_view
	networks = []
	try:
	    r = requests.get(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
	    r_json = r.json()
	    if r.status_code == 200:
		if len(r_json) > 0:
		    for network in r_json:
			if 'network' in network:
			    networks.append(network['network'])
		    return networks
		else:
		    raise InfobloxNotFoundException("No networks found for extensible attributes: " + attributes)
	    else:
		if 'text' in r_json:
		    raise InfobloxGeneralException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def get_host_by_extattrs(self, attributes):
	""" Implements IBA REST API call to find host by it's extensible attributes
	Returns array of hosts in FQDN
	:param attributes: comma-separated list of attrubutes name/value pairs in the format:
		attr_name=attr_value - exact match for attribute value
		attr_name:=attr_value - case insensitive match for attribute value
		attr_name~=regular_expression - match attribute value by regular expression
		attr_name>=attr_value - search by number greater than value
		attr_name<=attr_value - search by number less than value
		attr_name!=attr_value - search by number not equal of value
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/record:host?*' + "&*".join(attributes.split(",")) + '&view=' + self.iba_dns_view
	hosts = []
	try:
	    r = requests.get(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
	    r_json = r.json()
	    if r.status_code == 200:
		if len(r_json) > 0:
		    for host in r_json:
			if 'name' in host:
			    hosts.append(host['name'])
		    return hosts
		else:
		    raise InfobloxNotFoundException("No hosts found for extensible attributes: " + attributes)
	    else:
		if 'text' in r_json:
		    raise InfobloxNotFoundException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def get_network_extattrs(self, network, attributes=None):
	""" Implements IBA REST API call to retrieve network extensible attributes
	Returns hash table of attributes with attribute name as a hash key
	:param network: network in CIDR format
	:param attributes: array of extensible attribute names (optional)
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/network?network=' + network + '&network_view=' + self.iba_network_view + '&_return_fields=network,extattrs'
	try:
	    r = requests.get(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
	    r_json = r.json()
	    if r.status_code == 200:
		if len(r_json) > 0:
		    extattrs = {}
		    if attributes:
			for attribute in attributes:
			    if attribute in r_json[0]['extattrs']:
				extattrs[attribute] = r_json[0]['extattrs'][attribute]['value']
			    else:
				raise InfobloxNotFoundException("No requested attribute found: " + attribute)
		    else:
			for attribute in r_json[0]['extattrs'].keys():
			    extattrs[attribute] = r_json[0]['extattrs'][attribute]['value']
		    return extattrs
		else:
		    raise InfobloxNotFoundException("No requested network found: " + network)
	    else:
		if 'text' in r_json:
		    raise InfobloxNotFoundException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def update_network_extattrs(self, network, attributes):
	""" Implements IBA REST API call to add or update network extensible attributes
	:param network: network in CIDR format
	:param attributes: hash table of extensible attributes with attribute name as a hash key
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/network?network=' + network + '&network_view=' + self.iba_network_view + '&_return_fields=network,extattrs'
	extattrs = {}
	try:
	    r = requests.get(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
	    r_json = r.json()
	    if r.status_code == 200:
		if len(r_json) > 0:
		    network_ref = r_json[0]['_ref']
		    if network_ref:
			extattrs = r_json[0]['extattrs']
			for attr_name, attr_value in attributes.iteritems():
			    extattrs[attr_name]['value'] = attr_value
			payload = '{"extattrs": ' + json.JSONEncoder().encode(extattrs) + '}'
			rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/' + network_ref
			r = requests.put(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl, data=payload)
			if r.status_code == 200:
			    return
			else:
			    if 'text' in r_json:
				raise InfobloxGeneralException(r_json['text'])
			    else:
				r.raise_for_status()
		    else:
			raise InfobloxGeneralException("No network reference received in IBA reply for network: " + network)
		else:
		    raise InfobloxNotFoundException("No requested network found: " + network)
	    else:
		if 'text' in r_json:
		    raise InfobloxGeneralException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def delete_network_extattrs(self, network, attributes):
	""" Implements IBA REST API call to delete network extensible attributes
	:param network: network in CIDR format
	:param attributes: array of extensible attribute names
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/network?network=' + network + '&network_view=' + self.iba_network_view + '&_return_fields=network,extattrs'
	try:
	    r = requests.get(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
	    r_json = r.json()
	    if r.status_code == 200:
		if len(r_json) > 0:
		    network_ref = r_json[0]['_ref']
		    if network_ref:
			extattrs = r_json[0]['extattrs']
			for attribute in attributes:
			    if attribute in extattrs:
				del extattrs[attribute]
			payload = '{"extattrs": ' + json.JSONEncoder().encode(extattrs) + '}'
			rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/' + network_ref
			r = requests.put(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl, data=payload)
			if r.status_code == 200:
			    return
			else:
			    if 'text' in r_json:
				raise InfobloxGeneralException(r_json['text'])
			    else:
				r.raise_for_status()
		    else:
			raise InfobloxGeneralException("No network reference received in IBA reply for network: " + network)
		else:
		    raise InfobloxNotFoundException("No requested network found: " + network)
	    else:
		if 'text' in r_json:
		    raise InfobloxGeneralException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def create_network(self, network):
	""" Implements IBA REST API call to create DHCP network object
	:param network: network in CIDR format
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/network'
	payload = '{"network": "' + network + '","network_view": "' + self.iba_network_view + '"}'
	try:
	    r = requests.post(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl, data=payload)
	    r_json = r.json()
	    if r.status_code == 200 or r.status_code == 201:
		return
	    else:
		if 'text' in r_json:
		    raise InfobloxGeneralException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def delete_network(self, network):
	""" Implements IBA REST API call to delete DHCP network object
	:param network: network in CIDR format
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/network?network=' + network + '&network_view=' + self.iba_network_view
	try:
	    r = requests.get(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
	    r_json = r.json()
	    if r.status_code == 200:
		if len(r_json) > 0:
		    network_ref = r_json[0]['_ref']
		    if network_ref:
			rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/' + network_ref
			r = requests.delete(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
			if r.status_code == 200:
			    return
			else:
			    if 'text' in r_json:
				raise InfobloxGeneralException(r_json['text'])
			    else:
				r.raise_for_status()
		    else:
			raise InfobloxGeneralException("No network reference received in IBA reply for network: " + network)
		else:
		    raise InfobloxNotFoundException("No network found: " + network)
	    else:
		if 'text' in r_json:
		    raise InfobloxGeneralException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def create_networkcontainer(self, networkcontainer, comment):
	""" Implements IBA REST API call to create DHCP network containert object
	:param networkcontainer: network container in CIDR format
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/networkcontainer'
	payload = '{"network": "' + networkcontainer + '", "comment": "'  + comment + '","network_view": "' + self.iba_network_view + '"}'
	print(rest_url, payload)
	try:
	    r = requests.post(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl, data=payload)
	    r_json = r.json()
	    if r.status_code == 200 or r.status_code == 201:
		return
	    else:
		if 'text' in r_json:
		    raise InfobloxGeneralException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def list_networkcontainer(self, octect):
	""" Implements IBA REST API call to list all container in a network
    example uri: https://infoblox/wapi/v2.6/networkcontainer?network~=10&_return_type=json
	:param octect: first octect from container ie 10 for a 10.0.0.0/8 network
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/networkcontainer?network~=' + octect
	print(rest_url)
	try:
	    r = requests.get(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
	    r_json = r.json()
	    if r.status_code == 200 or r.status_code == 201:
			for i in range(len(r_json)):
					print(r_json[i]['network'])
	    else:
		if 'text' in r_json:
		    raise InfobloxGeneralException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def delete_networkcontainer(self, networkcontainer):
	""" Implements IBA REST API call to delete DHCP network container object
	:param networkcontainer: network container in CIDR format
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/networkcontainer?network=' + networkcontainer + '&network_view=' + self.iba_network_view
	try:
	    r = requests.get(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
	    r_json = r.json()
	    if r.status_code == 200:
		if len(r_json) > 0:
		    network_ref = r_json[0]['_ref']
		    if network_ref:
			rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/' + network_ref
			r = requests.delete(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
			if r.status_code == 200:
			    return
			else:
			    if 'text' in r_json:
				raise InfobloxGeneralException(r_json['text'])
			    else:
				r.raise_for_status()
		    else:
			raise InfobloxGeneralException("No network container reference received in IBA reply for network container: " + networkcontainer)
		else:
		    raise InfobloxNotFoundException("No network container found: " + networkcontainer)
	    else:
		if 'text' in r_json:
		    raise InfobloxGeneralException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise

    def get_next_available_network(self, networkcontainer, cidr):
	""" Implements IBA REST API call to retrieve next available network of network container
	Returns network address in CIDR format
	:param networkcontainer: network container address in CIDR format
	:param cidr: requested network length (from 0 to 32)
	"""
	rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/networkcontainer?network=' + networkcontainer + '&network_view=' + self.iba_network_view
    	try:
	    r = requests.get(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
	    r_json = r.json()
	    if r.status_code == 200:
		if len(r_json) > 0:
		    net_ref = r_json[0]['_ref']
		    rest_url = 'https://' + self.iba_host + '/wapi/v' + self.iba_wapi_version + '/' + net_ref + '?_function=next_available_network&cidr=' + str(cidr) + '&num=1'
		    r = requests.post(url=rest_url, auth=(self.iba_user, self.iba_password), verify=self.iba_verify_ssl)
		    r_json = r.json()
		    if r.status_code == 200:
			network = r_json['networks'][0]
			return network
		    else:
			if 'text' in r_json:
			    if 'code' in r_json and r_json['code'] == 'Client.Ibap.Data':
				raise InfobloxNoNetworkAvailableException(r_json['text'])
			    else:
				raise InfobloxGeneralException(r_json['text'])
			else:
			    r.raise_for_status()
		else:
		    raise InfobloxNotFoundException("No requested network container found: " + networkcontainer)
	    else:
		if 'text' in r_json:
		    raise InfobloxGeneralException(r_json['text'])
		else:
		    r.raise_for_status()
	except ValueError:
	    raise Exception(r)
	except Exception:
	    raise
