#!/usr/bin/env python3
from jinja2 import Environment, FileSystemLoader
from ruamel.yaml import YAML
import socket
import shlex
import subprocess
import time
from configparser import ConfigParser
import click
import py
import colorama
import sys

# asset_data_url = ("https://raw.githubusercontent.com/patchkez/kmdplatform/"
#    "master/yaml/data.yaml")

env = Environment(loader=FileSystemLoader('./dokomodo/templates/'), trim_blocks=True,
    lstrip_blocks=True)

config_dir = py.path.local('dokomodo/yaml')


class Config(object):
    def __init__(self, *args, **kwargs):
        # self.config = py.path.local('dokomodo').join('yaml').join('data.yaml')
        self.config = config_dir.join('data.yaml')
        # self.config_ini = py.path.local('dokomodo').join('yaml').join('config.ini')
        self.config_ini = config_dir.join('config.ini')

        super(Config, self).__init__(*args, **kwargs)

    def load(self):
        """Try to load the yaml"""
        yaml = YAML(typ='safe', pure=True)
        yaml.default_flow_style = True
        self.config_data = yaml.load(self.config.read())
        self.branches = self.config_data['assetchains']
        self.seed_ip = socket.gethostbyname(self.config_data['seed_host'])

    def load_ini(self):
        ini_parser = ConfigParser()
        ini_parser.read(str(self.config_ini))
        self.assetchains = ini_parser['ASSETCHAINS']
        self.mined_coins = self.assetchains['mined_coins'].split()
        self.delay_asset = float(self.assetchains['delay_asset'])


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
@click.option('-b', '--branch', required=True, type=click.Choice(['development', 'production']),
    prompt=True)
@pass_config
def generate_docker_compose(ctx, branch):
    """ TODO """
    filename = 'docker-compose_assets_' + branch + '.yml'
    click.echo('Writing new docker compose file into: %s' % filename)
    template = env.get_template('docker-compose-template.conf.j2')
    templatized_config = template.render(items=ctx.config_data['assetchains'][branch],
        seed_ip=ctx.seed_ip, mined=ctx.mined_coins)

    fo = open(filename, 'w')
    fo.write(templatized_config)
    fo.close()


@click.command('assetchains', short_help='Replacement for assetchains script')
@click.option('-b', '--branch', required=True, type=click.Choice(['development', 'production']),
    prompt=True)
@pass_config
def assetchains(ctx, branch):
    bash_template = env.get_template('assetchains.j2')
    bash_templatized_config = bash_template.render(items=ctx.config_data['assetchains'][branch],
        seed_ip=ctx.seed_ip, mined=ctx.mined_coins)

    # fa = open('assetchains', 'w')
    # fa.write(bash_templatized_config)
    # fa.close()

    # Remove empty strings
    assetchains = list(filter(None, bash_templatized_config.split("\n")))
    # Executed komodod commands with predefined sleep time
    for assetchain_command in assetchains:
        args = shlex.split(assetchain_command)
        try:
            subprocess.Popen(args)
        except OSError as exception:
            click.echo(exception)
            sys.exit(1)
        time.sleep(ctx.delay_asset)


# Add functions into cli() function which is main group for all commands
cli.add_command(generate_docker_compose)
cli.add_command(assetchains)


if __name__ == "__main__":
    cli()
