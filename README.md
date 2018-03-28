## Komodotools repository
Purpose of this repository is to collect scripts/tools from Notary Nodes operators.
We would like to get rid of scripts in [komodo](https://github.com/jl777/komodo) and [iguana](https://github.com/jl777/SuperNET) repositories. These supposed to serve as examples in the past. 

Because we did not decide what the best management tooling is, we will keep different ideas separated in directories until we fix problems which will converge to common tools.

## Contribution
- normal Github workflow is followed (fork this repo, create branch, make changes and push back to your repo, create PR, review, merge, repeat)
- if you see similar script to one which exists in repo, try to implement your changes against it
- each directory must contain README.md file with description how to install/use your scripts
- update this README.md and add brief description what your script/tool does
- try to keep only one version of file which would work in test and prod environments
- once your scripts are merged into this repository, refer to it and push all updates here 
- try to separate data/configs from code, if the data/configs will change, your scripts should still work without rewriting them

## Directories content
### kolo
It was Kolo's idea to create this repository and here is his concept how it should work.

### dragonriders
 - dokomodo - script written in Python [Click](http://click.pocoo.org) framework. 
   - write funtcions which will become commands
   - supports dev and prod environments
   - assetchains data stored in yaml data file and ini config for configuration (you can enable mining for specific chains) 
   - there is Config Class which takes care of parsing config/data files so no need to do it in you functions
   - many other features supported by Click framework

### a-team 
 - complete step-by-step guide with bash installation scripts

### ansible-playbooks
 - This is demonstration that central yaml file can be used by other tools. I expect people to start using Ansible for system configuration.

## Contacts
Ideas can be discussed in [#notarynode](https://komodo-platform.slack.com) Slack channel, but please all code proposals discuss via PRs on Github.
