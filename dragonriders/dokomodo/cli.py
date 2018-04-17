#!/usr/bin/env python3
from jinja2 import Environment, FileSystemLoader
from ruamel.yaml import YAML
from socket import gethostbyname
from shlex import split
from subprocess import Popen
from time import sleep
from configparser import ConfigParser
import click
from py import path
from sys import exit
from os import path as expander
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


# asset_data_url = ("https://raw.githubusercontent.com/patchkez/kmdplatform/"
#    "master/yaml/data.yaml")

env = Environment(loader=FileSystemLoader('./dokomodo/templates/'), trim_blocks=True,
    lstrip_blocks=True)

config_dir = path.local('/yaml_data')
if config_dir.check() is False:
    config_dir = path.local('dokomodo/yaml')


class Config(object):
    def __init__(self, *args, **kwargs):
        self.config = config_dir.join('data.yaml')
        self.config_ini = config_dir.join('config.ini')

        super(Config, self).__init__(*args, **kwargs)

    def load(self):
        """Try to load the yaml"""
        # Configure yaml loader
        yaml = YAML(typ='safe', pure=True)
        yaml.default_flow_style = True
        # Try to read yaml file
        try:
            self.config_data = yaml.load(self.config.read())
        except OSError as exception:
            click.echo('{} yaml file could not be read: {}'.format(self.config.read, exception))
        self.branches = self.config_data['assetchains']
        self.seed_ip = gethostbyname(self.config_data['seed_host'])

    def load_ini(self):
        # initialize INI parser
        ini_parser = ConfigParser()
        # Try to read ini file
        try:
            ini_parser.read(str(self.config_ini))
        except OSError as exception:
            click.echo('{} file could not be read: {}'.format(self.config_ini, exception))

        self.btcpubkey = ini_parser['DEFAULT']['btcpubkey']

        self.assetchains = ini_parser['ASSETCHAINS']
        self.mined_coins = self.assetchains['mined_coins'].split()
        self.delay_asset = float(self.assetchains['delay_asset'])
        self.rpc_username = self.assetchains['rpc_username']
        self.rpc_password = self.assetchains['rpc_password']
        self.write_path_conf = self.assetchains['write_path_conf']

        self.scaling_tests = ini_parser['SCALING_TESTING']
        self.sendtomany_recipients = self.scaling_tests['sendtomany_recipients']
        self.number_of_requests = self.scaling_tests['number_of_requests']
        self.delay_between_requests = self.scaling_tests['delay_between_requests']

    def write_config(self, dirname, filename, templatized_config):
        # If directory is not set, set it to current directory
        if dirname is False:
            dirname = './'
        # Expand ~ to full path
        dirname_expanded = expander.expanduser(dirname)
        # Construct full path - directory + filename
        temppath = path.local(dirname_expanded).join(filename)
        # Try to open config in write mode
        try:
            myfile = temppath.open(mode='w', ensure=True)
            myfile.write(templatized_config)
        except OSError as exception:
            click.echo('File could not be opened in write mode or be written: {}'.format(exception))


# This is click thing, it will create decorator named pass_config from our Config class
# This decorator is then passed to every function which needs to access attributes from Config class
pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@pass_config
def cli(config):
    config.load()
    config.load_ini()


@click.command('generate_docker_compose',
    short_help='Generates docker-compose file with all assetchains')
@click.option('-b', '--branch', required=True, type=click.Choice(['development', 'production',
    'test']),
    prompt=True)
@pass_config
def generate_docker_compose(ctx, branch):
    """ TODO """
    filename = 'docker-compose_assets_' + branch + '.yml'
    dirname = "./"
    click.echo('Writing new docker compose file into: {}'.format(filename))
    template = env.get_template('docker-compose-template.conf.j2')
    templatized_config = template.render(items=ctx.config_data['assetchains'][branch],
        seed_ip=ctx.seed_ip, mined=ctx.mined_coins, btcpubkey=ctx.btcpubkey)

    ctx.write_config(dirname, filename=filename, templatized_config=templatized_config)


@click.command('assetchains', short_help='Replacement for assetchains script')
@click.option('-b', '--branch', required=True, type=click.Choice(['development', 'production',
    'test']),
    prompt=True)
@pass_config
def assetchains(ctx, branch):
    bash_template = env.get_template('assetchains.j2')
    bash_templatized_config = bash_template.render(items=ctx.config_data['assetchains'][branch],
        seed_ip=ctx.seed_ip, mined=ctx.mined_coins, btcpubkey=ctx.btcpubkey)

    # Remove empty strings
    assetchains = list(filter(None, bash_templatized_config.split("\n")))
    # Executed komodod commands with predefined sleep time
    for assetchain_command in assetchains:
        args = split(assetchain_command)
        try:
            Popen(args)
        except OSError as exception:
            click.echo(exception)
            exit(1)
        sleep(ctx.delay_asset)


@click.command('generate_assetchains_conf', short_help='Generates configuration file for \
    assetchains')
@click.option('-b', '--branch', required=True, type=click.Choice(['development', 'production',
    'test']))
@click.option('-a', '--asset', required=False)
@pass_config
def generate_assetchains_conf(ctx, branch, asset):
    asset_template = env.get_template('assetchains_config.j2')

    def templatize(assetchain_name):
        dirname = ctx.write_path_conf + '/' + assetchain_name
        filename = assetchain_name + '.conf'
        asset_templatized_config = asset_template.render(
            rpcuser=ctx.rpc_username,
            rpcpassword=ctx.rpc_password,
            rpcport=ctx.config_data['assetchains'][branch][assetchain_name]['rpc_port'],
            btcpubkey=ctx.btcpubkey
        )

        ctx.write_config(dirname, filename, asset_templatized_config)

        # return click.echo(asset_templatized_config)
        return asset_templatized_config

    for assetchain_name in ctx.config_data['assetchains'][branch]:
        if asset and asset == assetchain_name:
            click.echo('Writing CONFIG_FILE: {}'.format(assetchain_name))
            templatize(assetchain_name)
        elif asset:
            pass
        else:
            click.echo('Writing CONFIG_FILE: {}'.format(assetchain_name))
            templatize(assetchain_name)


@click.command('sendmany_assetchains', short_help='Import private key into assetchains')
@click.option('-b', '--branch', required=True, type=click.Choice(['development', 'production',
    'test']))
@click.option('-a', '--asset', required=False)
@pass_config
def sendmany_assetchains(ctx, branch, asset):

    def send_request(assetchain_name, assetchain_rpcport):
        assetchain_rpcuser = 'rpcuser'
        assetchain_rpcpassword = 'rpcpassword'

        # request_url = (
        #     'http://' + asset_rpcuser + ':' + asset_rpcpassword + '@' + assetchain_name + ':' +
        #     assetchain_rpcport)

        rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s" % (assetchain_rpcuser,
            assetchain_rpcpassword, assetchain_name, int(assetchain_rpcport)))

        try:
            rpc_connection.sendmany("", ctx.sendtomany_recipients)
        except JSONRPCException as e:
            click.echo("Error: %s" % e.error['message'])

    counter = 0
    while counter < float(ctx.number_of_requests):
        # click.echo(ctx.config_data['assetchains'][branch])
        for assetchain_name in ctx.config_data['assetchains'][branch]:
            # click.echo(type(assetchain_name))
            rpc_port = ctx.config_data['assetchains'][branch][assetchain_name]['rpc_port']
            if asset and asset == assetchain_name:
                click.echo('Sending request to: {}'.format(assetchain_name))
                send_request(assetchain_name, rpc_port)
            elif asset:
                pass
            else:
                click.echo('Sending request to: {}'.format(assetchain_name))
                send_request(assetchain_name, rpc_port)
        counter += 1
        sleep(ctx.delay_between_requests)


# Add functions into cli() function which is main group for all commands
cli.add_command(generate_docker_compose)
cli.add_command(assetchains)
cli.add_command(generate_assetchains_conf)
cli.add_command(sendmany_assetchains)


if __name__ == "__main__":
    cli()
