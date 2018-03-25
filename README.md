# DOkomodo - swiss army knife for Notary Nodes

Current komodo/iguana management scripts are not ideal and this is idea how to replace 
existing komodo/iguana scripts with universal framework. Python [Click](http://click.pocoo.org) 
framework was used which is ideal for creating CLI applications. Main idea of Click is that your
functions will become excutable as commands.

Features of DOkomodo:
- single data file in yaml format (easy to edit), sections for prod and dev environments - all data
 like list of assetchains and their ports will come here.
- repeating functions like e.g. loading list of assetchains do not have to be written again and again
- data file loaded only once and data accessed via instance attributes
- configuration in config.ini file allows you to say for which coins mining is enabled, you can disable
 minining completely or you can enable mining on randomly selected assetchains
- currently only 2 commands available

## Installation steps
### Enable python3 virtualenv
Virtualenv is directory which contains all python packages you need for your project.

Install virtualenv on Centos (as root user):
```
# yum install python34 python-pip
```

Install virtualenv on Ubuntu (as root):
```
# apt-get install python-pip
```

Now install virtualenv package:
```
# pip install -U virtualenv

```

Create our virtualenv
```
cd ~/venv_projects
virtualenv -p python3 komodotools_venv
```

This is how we activate our virtualenvironment. You can deactivate it with `deactivate` command:
```
source ~/venv_projects/komodotools_venv/bin/activate
```

### Clone this repository
Make sure you have activated your virtualenv before this step. 
```
cd ~/git_projects/
git clone <this_repo>.git && cd komodotools
pip install -Ur requirements.txt
pip install --editable .
```

requirements.txt file contains list of all python packages we need for this project. All python packages will be installed into virtualenv folder you created. They won't collide with your system python packages.

## How-to use it
Once your virtualenv is activated, type `dokomodo`:
```
$ dokomodo
Usage: dokomodo [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  assetchains              Replacement for assetchains script
  generate_docker_compose  Generates docker-compose file with all assetchains
```

Then you can continue specify subcommands:
```
$ dokomodo assetchains --help
Usage: dokomodo assetchains [OPTIONS]

Options:
  -b, --branch [development|production]
                                  [required]
  --help                          Show this message and exit.
```


