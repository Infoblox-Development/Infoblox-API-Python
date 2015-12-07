# -*- coding: utf-8 -*-
import click
from infoblox.infoblox import Infoblox


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


@cli.group()
def hostrecord():
    '''Create and delete HOST records.'''
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
