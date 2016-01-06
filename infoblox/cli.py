# -*- coding: utf-8 -*-
import click
from .infoblox import Infoblox


@click.group()
@click.option('--ipaddr', envvar='IB_IPADDR',
              help='IP address of the infoblox API')
@click.option('--user', envvar='IB_USER',
              help='Infoblox API username')
@click.option('--password', envvar='IB_PASSWORD',
              help='Infoblox API password')
@click.option('--wapi-version', envvar='IB_WAPI_VERSION', default='1.6',
             help='Infoblox API version')
@click.option('--dns-view', envvar='IB_DNS_VIEW', default='default',
             help='Default DNS view')
@click.option('--network-view', envvar='IB_NETWORK_VIEW', default='default',
             help='Default network view')
@click.option('--verify-ssl/--no-verify-ssl', envvar='IB_VERIFY_SSL',
             default=False, help='Enable SSL verification')
@click.pass_context
def cli(ctx, ipaddr, user, password, wapi_version, dns_view, network_view, verify_ssl):
    '''Clinfobloxs is a command line interface for the Infoblox API.'''
    ctx.obj = Infoblox(ipaddr, user, password, wapi_version,
                       dns_view, network_view, verify_ssl)

@cli.group()
def cname():
    '''Create and delete CNAME records'''
    pass

@cname.command('create')
@click.argument('fqdn')
@click.argument('name')
@click.pass_obj
def create_cname(api, fqdn, name):
    '''Create a CNAME record.'''
    click.echo('adding cname "%s" for %s' % (name, fqdn))
    api.create_cname_record(fqdn, name)

@cname.command('delete')
@click.argument('fqdn')
@click.pass_obj
def delete_cname(api, fqdn):
    '''Delete a CNAME record.'''
    click.echo('deleting cname for %s' % (fqdn,))
    api.delete_cname_record(fqdn)

@cname.command('update')
@click.argument('old_fqdn')
@click.argument('new_fqdn')
@click.pass_obj
def update_cname(api, old_fqdn, new_fqdn):
    '''Update a CNAME record.'''
    click.echo ('updating cname from %s to %s' % (old_fqdn, new_fqdn))
    api.update_cname_record(fqdn)

@cli.group()
def hostrecord():
    ''' HOST records.'''
    pass

@hostrecord.command('create')
@click.argument('address')
@click.argument('fqdn')
@click.pass_obj
def create_host_record(api, address, fqdn):
    '''Create a host record.'''
    click.echo('creating host record %s = %s' % (address, fqdn))
    api.create_host_record(address, fqdn)

@hostrecord.command('delete')
@click.argument('fqdn')
@click.pass_obj
def delete_host_record(api, fqdn):
    '''Delete a host record.'''
    click.echo('deleting host record %s' % (fqdn,))
    api.delete_host_record(fqdn)

@hostrecord.command('add_alias')
@click.argument('host_fqdn')
@click.argument('alias_fqdn')
@click.pass_obj
def add_host_alias(api, host_fqdn, alias_fqdn):
    '''add a host record.'''
    click.echo('adding alias %s for host  %s' % (alias_fqdn, host_fqdn,))
    api.delete_host_record(host_fqdn, alias_fqdn)

@hostrecord.command('delete_alias')
@click.argument('host_fqdn')
@click.argument('host_alias')
@click.pass_obj
def delete_host_alias(api, host_fqdn, host_alias):
    '''Delete a host alias.'''
    click.echo('deleting alias %s for host  %s' % (host_fqdn, host_alias,))
    api.delete_host_record(host_fqdn, alias_fqdn)

@hostrecord.command('by_extattrs')
@click.argument('extattrs')
@click.pass_obj
def get_host_by_extattrs(api, extattrs):
    '''geting host by extensible attributes.'''
    click.echo('getting host by extensible attributes')
    api.get_host_by_extattrs(extattrs)

@hostrecord.command('by_regexp')
@click.argument('regexp')
@click.pass_obj
def get_host_by_regexp(api, regexp):
    '''geting host by fqdn regexp filter.'''
    click.echo('getting host by fqdn regexp filter')
    api.get_host_by_regexp(regexp)

@hostrecord.command('get')
@click.argument('fqdn')
@click.pass_obj
def get_host(api,  fqdn):
    '''get a host record.'''
    click.echo('get host record %s ' % (fqdn))
    print (api.get_host(fqdn))

@hostrecord.command('by_ip')
@click.argument('ip')
@click.pass_obj
def get_host_by_ip(api,ip):
    '''get a host by ip.'''
    click.echo('getting host record by ip %s ' % (ip))
    print (api.get_host_by_ip(ip))

@hostrecord.command('extattrs')
@click.argument('fqdn')
@click.pass_obj
def get_host_extattrs(api, fqdn):
    '''get host extensible attributes'''
    click.echo('getting host extensible attributes %s ' % (fqdn))
    print (api.get_host_extattrs(fqdn))

@cli.group()
def network():
    ''' get network object fields'''
    pass

@network.command('create')
@click.argument('network')
@click.pass_obj
def create_network(api, network):
    '''create new network'''
    click.echo('creating network %s ' % (network))
    api.create_network(network)

@network.command('delete')
@click.argument('network')
@click.pass_obj
def delete_network(api, network):
    '''delete new network'''
    click.echo('deleting network %s ' % (network))
    api.delete_network(network)

@network.command('next_network')
@click.argument('networkcontainer')
@click.argument('cidr')
@click.pass_obj
def next_available_network(api, networkcontainer, cidr):
    ''' get next available network. '''
    click.echo('getting next available network in %s' % (networkcontainer))
    api.get_next_available_network(networkcontainer, cidr)

@network.command('get')
@click.argument('network')
@click.pass_obj
def get_networkobject(api, network):
    click.echo('getting networkobject %s ' % (network))
    print (api.get_network(network))

@network.command('by_ip')
@click.argument('ip')
@click.pass_obj
def get_network_by_ip(api, ip):
    click.echo('getting network by ip %s' % (ip))
    print (api.get_network_by_ip(ip))

@network.command('by_extattrs')
@click.argument('extattrs')
@click.pass_obj
def get_network_by_extattrs(api, extattrs):
    click.echo('getting network by extensible attributes %s' % (extattrs))
    print (api.get_network_by_extattrs(api, extattrs))

@network.command('extattrs')
@click.argument('network')
@click.pass_obj
def get_network_extattrs(api, network):
    click.echo('getting network extensible attributes %s' % (network))
    print (api.get_network_extattrs(network))

@network.command('update_extattrs')
@click.argument('network')
@click.argument('extattrs')
@click.pass_obj
def update_network_extattrs(api, network, extattrs):
    click.echo('updating network extensible attributes %s' % (extattrs))
    api.update_network_extattrs(network, extattrs)

@network.command('delete_extattrs')
@click.argument('network')
@click.argument('extattrs')
@click.pass_obj
def delete_network_extattrs(api, network, extattrs):
    click.echo('deleting network extensible attributes %s' % (extattrs))
    api.delete_network_extattrs(network, extattrs)

@cli.group()
def networkcontainer():
    ''' network container'''
    pass

@networkcontainer.command('create')
@click.argument('networkcontainer')
@click.pass_obj
def create_networkcontainer(api, networkcontainer):
    click.echo('creating network container %s ' % (networkcontainer))
    api.create_networkcontainer(networkcontainer)

@networkcontainer.command('delete')
@click.argument('networkcontainer')
@click.pass_obj
def delete_networkcontainer(api, networkcontainer):
    click.echo('deleting network container %s ' % (networkcontainer))
    api.delete_networkcontainer(networkcontainer)

@cli.group()
def txtrecord():
    ''' DNS text record '''
    pass

@txtrecord.command('create')
@click.argument('text')
@click.argument('fqdn')
@click.pass_obj
def create_txt_record(api, text, fqdn):
    click.echo('creating text record %s for host %s ' % (text, fqdn))
    api.create_txt_record(text, fqdn)

@txtrecord.command('delete')
@click.argument('fqdn')
@click.pass_obj
def delete_txt_record(api, fqdn):
    click.echo('deleting text record for host %s ' % (fqdn))
    api.delete_txt_record(fqdn)

@txtrecord.command('by_regexp')
@click.argument('regexp')
@click.pass_obj
def get_txt_by_regexp(api, regexp):
    click.echo('getting text record by regexp  %s ' % (regexp))
    print (api.get_txt_by_regexp(regexp))

@cli.group()
def dhcp():
    ''' DHCP range '''
    pass

@dhcp.command('create')
@click.argument('start_ip_v4') 
@click.argument('end_ip_v4') 
@click.pass_obj
def create_dhcp_range(api, start_ip_v4, end_ip_v4):
    click.echo('creating DHCP IP range from %s to %s ' % (start_ip_v4, end_ip_v4))
    api.create_dhcp_range(start_ip_v4, end_ip_v4)

@dhcp.command('delete')
@click.argument('start_ip_v4') 
@click.argument('end_ip_v4') 
@click.pass_obj
def delete_dhcp_range(api, start_ip_v4, end_ip_v4):
    click.echo('deleting DHCP IP range from %s to %s ' % (start_ip_v4, end_ip_v4))
    api.delete_dhcp_range(start_ip_v4, end_ip_v4)

@cli.group()
def ip():
    '''IP address.'''
    pass

@ip.command('next_ip')
@click.argument('network')
@click.pass_obj
def get_next_available_ip(api, network):
    click.echo('getting next available ip in %s ' % (network))
    print (api.get_next_available_ip(network))

@ip.command('by_host')
@click.argument('fqdn')
@click.pass_obj
def get_ip_by_host(api, fqdn):
    click.echo('getting ip for host  %s ' % (fqdn))
    print (api.get_ip_by_host(fqdn))

