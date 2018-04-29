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
import requests
import json
import re


new_asset_data_url = ("https://raw.githubusercontent.com/patchkez/SuperNET/"
    "separate_json_data_dev_cherrypick/iguana/coins/tmp_cleanup/assetchains_data.yml")
yamlname = 'assetchains_data.yaml'

env = Environment(loader=FileSystemLoader('./dokomodo/templates/'), trim_blocks=True,
    lstrip_blocks=True)

config_dir = path.local('/yaml_data')
if config_dir.check() is False:
    config_dir = path.local('dokomodo/yaml')

global dump


# TEMPORARY CODE
# Temporary - download yaml file with iguana addcoin methods and supplies
def download_assets_data():
    global dump
    file = requests.get(new_asset_data_url, stream=True)
    # dump = file.raw
    dump = file.text


def save_assets_data():
    global dump
    newyaml = path.local(config_dir).join(yamlname)

    try:
        myfile2 = newyaml.open(mode='w', ensure=True)
        myfile2.write(dump)
    except OSError as exception:
        click.echo('File could not be opened in write mode or be written: {}'.format(exception))
    del dump


click.echo('Downloading preparsed {} as {}'.format(new_asset_data_url, yamlname))
download_assets_data()
save_assets_data()


# This is common function for sending rpc requests to bitcoind and komodod
def send_request(rpc_host, rpc_port, rpc_user, rpc_password):
    # assetchain_rpcuser = 'rpcuser'
    # assetchain_rpcpassword = 'rpcpassword'

    # request_url = (
    #     'http://' + asset_rpcuser + ':' + asset_rpcpassword + '@' + assetchain_name + ':' +
    #     assetchain_rpcport)

    return AuthServiceProxy("http://{}:{}@{}:{}".format(rpc_user,
        rpc_password, rpc_host, int(rpc_port)))

    # try:
    #    # rpc_connection.sendmany("", ctx.sendtomany_recipients)
    #    click.echo(rpc_connection.getinfo())
    # except JSONRPCException as e:
    #    click.echo("Error: %s" % e.error['message'])


# Common fucntion for sending any http API request e.g. to iguana
def post_rpc(url, payload, auth):
    try:
        r = requests.post(url, data=json.dumps(payload), auth=auth)
        return(json.loads(r.text))
    except Exception as e:
        print("Couldn't connect to " + url, e)
    exit(0)


# Common functions for getting data from web servers
def get_rpc(url):
    try:
        r = requests.get(url)
        # return(json.loads(r.text))
        return(r.text)
    except Exception as e:
        print("Couldn't connect to " + url, e)
    exit(0)


class Config(object):
    def __init__(self, *args, **kwargs):
        self.config = config_dir.join('data.yaml')
        self.new_config = config_dir.join('assetchains_data.yaml')
        self.config_ini = config_dir.join('config.ini')

        super(Config, self).__init__(*args, **kwargs)

    def load(self):
        """Try to load the yaml"""
        # Configure yaml loader
        yaml = YAML(typ='safe', pure=True)
        yaml.default_flow_style = True
        yaml.width = 8096  # or some other big enough value to prevent line-wrap
        # Try to read yaml file
        try:
            self.config_data = yaml.load(self.config.read())
        except OSError as exception:
            click.echo('{} yaml file could not be read: {}'.format(self.config.read, exception))
        self.branches = self.config_data['assetchains']
        self.seed_ip = gethostbyname(self.config_data['seed_host'])

    def load_new_asset(self):
        """Try to load the yaml"""
        # Configure yaml loader
        yaml = YAML(typ='safe', pure=True)
        yaml.default_flow_style = True
        # Try to read yaml file
        try:
            self.new_config_data = yaml.load(self.new_config.read())
        except OSError as exception:
            click.echo('{} yaml file could not be read: {}'.format(self.config.read, exception))
        # self.branches = self.new_config_data['assetchains']
        # self.seed_ip = gethostbyname(self.config_data['seed_host'])
        # self.supply = self
        self.seed_ip2 = gethostbyname(self.new_config_data['seed_ip'])

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
        self.rpc_bind = self.assetchains['rpc_bind']
        self.rpc_allowip = self.assetchains['rpc_allowip']
        self.write_path_conf = self.assetchains['write_path_conf']
        self.iguana = ini_parser['IGUANA']
        self.production_coins = self.iguana['production_coins']
        self.development_coins = self.iguana['development_coins']
        self.iguana_url = self.iguana['iguana_url']
        self.iguana_home_dir = self.iguana['iguana_home_dir']

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
    config.load_new_asset()
    config.load_ini()


@click.command('generate_docker_compose',
    short_help='OLD - Generates docker-compose file with all assetchains')
@click.option('-b', '--branch', required=True, type=click.Choice(['development', 'production',
    'test']),
    prompt=True)
@pass_config
def generate_docker_compose(ctx, branch):
    """ TODO """
    filename = 'docker-compose-assets-' + branch + '.yml'
    dirname = "./"
    click.echo('Writing new docker compose file into: {}'.format(filename))
    template = env.get_template('docker-compose-template.conf.j2')
    templatized_config = template.render(items=ctx.config_data['assetchains'][branch],
        seed_ip=ctx.seed_ip, mined=ctx.mined_coins, btcpubkey=ctx.btcpubkey)

    ctx.write_config(dirname, filename=filename, templatized_config=templatized_config)


@click.command('generate_new_docker_compose',
    short_help='PROD - Generates docker-compose file with all assetchains')
@click.option('-b', '--branch', required=True, type=click.Choice(['development', 'production',
    'test']), prompt=True)
@click.option('-a', '--asset', required=False, help='name of assetchain in capital \
    letters e.g. SUPERNET')
@click.option('-i', '--image', required=True, help='name of image used for assetchains, \
    it must match image name you use for komodod e.g. kmdplatform_komodod_dev or \
    kmdplatform_komodod')
@pass_config
def generate_new_docker_compose(ctx, branch, asset, image):
    """ TODO """
    filename = 'docker-compose-assets-' + branch + '.yml'
    dirname = "./"
    click.echo('Writing new docker compose file into: {}'.format(filename))

    yaml = YAML(typ='safe', pure=True)
    yaml.default_flow_style = True
    dic = {}

    def filtered_yaml():
        coins = branch + '_coins_assets'
        for assetchain_key in ctx.assetchains[coins].split(', '):
            x = ctx.new_config_data['assetchains'][assetchain_key]
            dic[assetchain_key] = x
            if asset and asset == assetchain_key:
                pass
            elif asset:
                pass
            else:
                pass
        return dic

    template = env.get_template('docker-compose-new-template.conf.j2')
    templatized_config = template.render(items=filtered_yaml(),
        seed_ip=ctx.seed_ip2, mined=ctx.mined_coins, btcpubkey=ctx.btcpubkey, image_name=image)
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
            # rpcbind=ctx.rpc_bind,
            rpcbind=assetchain_name,
            rpcallowip=ctx.rpc_allowip,
            # rpcport=ctx.config_data['assetchains'][branch][assetchain_name]['rpc_port'],
            rpcport=ctx.new_config_data['assetchains'][assetchain_name]['iguana_payload'][
                'rpc'],
            btcpubkey=ctx.btcpubkey
        )

        ctx.write_config(dirname, filename, asset_templatized_config)

        # return click.echo(asset_templatized_config)
        return asset_templatized_config

    coins = branch + '_coins_assets'
    for assetchain_key in ctx.assetchains[coins].split(', '):
        # for assetchain_name in ctx.config_data['assetchains'][branch]:
        if asset and asset == assetchain_key:
            click.echo('Writing CONFIG_FILE: {}'.format(assetchain_key))
            templatize(assetchain_key)
        elif asset:
            pass
        else:
            click.echo('Writing CONFIG_FILE: {}'.format(assetchain_key))
            templatize(assetchain_key)


@click.command('importprivkey', short_help='Importprivkey into assetchains')
@click.option('-b', '--branch', required=True, type=click.Choice(['development', 'production',
    'test']))
@click.option('-a', '--asset', required=False)
@click.option('-h', '--rpchost', prompt=True, hide_input=False, confirmation_prompt=False,
        help='RPC host')
@click.option('-u', '--rpcuser', prompt=True, hide_input=False, confirmation_prompt=False,
        help='RPC username')
@click.option('-r', '--rpcpassword', prompt=True, hide_input=False, confirmation_prompt=False,
        help='RPC password')
@click.option('-k', '--btcdprivkey', prompt=True, hide_input=True, confirmation_prompt=True,
        help='BTCD privkey')
@pass_config
def importprivkey(ctx, branch, asset, rpchost, rpcuser, rpcpassword, btcdprivkey):

    coins = branch + '_coins_assets'
    for assetchain_key in ctx.assetchains[coins].split(', '):
        # method = 'importprivkey' + '(privkey=' + btcdprivkey + ' , rescan=False)'
        rpcport = int(ctx.new_config_data['assetchains'][assetchain_key]['iguana_payload']['rpc'])
        click.echo(ctx.new_config_data['assetchains'][assetchain_key]['iguana_payload']['rpc'])
        rpc = send_request(rpc_host=rpchost, rpc_port=rpcport, rpc_user=rpcuser,
            rpc_password=rpcpassword)

        if asset and asset == assetchain_key:
            click.echo('Sending request to: {}'.format(assetchain_key))
            # send_request(assetchain_name, rpc_port, method)
            click.echo(rpc.importprivkey(btcdprivkey, '', False))
        elif asset:
            pass
        else:
            click.echo('Sending request to: {}'.format(assetchain_key))
            click.echo(rpc.importprivkey(btcdprivkey, '', False))
            # send_request(assetchain_name, rpc_port, method)
            # click.echo(rpc.getinfo())
        sleep(1)


@click.command('start_iguana', short_help='Add all methods into iguana')
@click.option('-b', '--branch', required=True, type=click.Choice(['development', 'production']))
@click.option('-a', '--asset', required=False, help='name of assetchain in capital \
    letters e.g. SUPERNET')
@click.option('-p', '--password', prompt=True, hide_input=True, confirmation_prompt=True,
        help='iguana passphrase')
@click.option('-m', '--myip', required=False, prompt=True, hide_input=False,
        confirmation_prompt=False, help='provide public IP of your NN if run via SSH session')
@pass_config
def start_iguana(ctx, branch, asset, password, myip):
    url = ctx.iguana_url
    # No authentication is needed for iguana
    auth = ('', '')

    # My IP
    if myip:
        response = myip
    else:
        # get public IP address of this host
        myip = 'http://' + ctx.new_config_data['check_my_ip']
        response = get_rpc(myip).rstrip()

    click.echo('My IP address is: {}'.format(response))
    myipmethod = ctx.new_config_data['misc_methods']['supernet_myip']
    myipmethod['ipaddr'] = response
    # click.echo('MY IP method: {}'.format(myipmethod))
    post_rpc(url, myipmethod, auth)
    sleep(3)

    #  Add notaries
    for notary in ctx.new_config_data['misc_methods']['notaries']:
        click.echo('Adding notary: {}'.format(notary))
        post_rpc(url, ctx.new_config_data['misc_methods']['notaries'][notary], auth)

    # Walletpassphrase
    click.echo('Adding walletpassphrase!')
    wallet = ctx.new_config_data['misc_methods']['wallet_passphrase']
    # Replace password with the one provided by user
    wallet['params'][0] = password
    # click.echo(wallet)
    post_rpc(url, wallet, auth)

    # Add coins + DPOW
    coins = branch + '_coins'
    for assetchain_key in ctx.iguana[coins].split(', '):
        # Read only assetchains payloads
        payload = ctx.new_config_data['assetchains'][assetchain_key]['iguana_payload']

        # Replace ${HOME#/} with value in our INI file
        # remove first '/'
        home = re.sub(r"\/", "", ctx.iguana_home_dir, 1)
        # Read value of 'path' key
        line = payload['path']
        # Substitute
        newline = re.sub(r"\$\{HOME\#\/\}", home, line)
        # Update value in loaded dictionary
        ctx.new_config_data['assetchains'][assetchain_key]['iguana_payload']['path'] = newline

        # Dpow
        dpow = ctx.new_config_data['misc_methods']['dpow']
        dpow['pubkey'] = ctx.btcpubkey
        dpow['symbol'] = assetchain_key
    # click.echo(wallet)
        if asset and asset == assetchain_key:
            click.echo('Sending addcoin request to: {}'.format(assetchain_key))
            post_rpc(url, payload, auth)
            # sleep(3)
            click.echo('Sending dpow {} request to: {}'.format(dpow, assetchain_key))
            post_rpc(url, dpow, auth)
        elif asset:
            pass
        else:
            click.echo('Sending addcoin request to: {}'.format(assetchain_key))
            post_rpc(url, payload, auth)
            # sleep(10)
            click.echo('Sending dpow {} request to: {}'.format(dpow, assetchain_key))
            post_rpc(url, dpow, auth)
            # sleep(10)


# Add functions into cli() function which is main group for all commands
cli.add_command(generate_docker_compose)
cli.add_command(generate_new_docker_compose)
cli.add_command(assetchains)
cli.add_command(generate_assetchains_conf)
cli.add_command(importprivkey)
cli.add_command(start_iguana)


if __name__ == "__main__":
    cli()
