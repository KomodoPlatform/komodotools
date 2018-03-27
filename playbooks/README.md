## Ansible playbooks/roles for setting up Notary Node
This is demonstration that central yaml file can be used by other tools.

### How to use it
- install Ansible localy
- modify inventory file and execute: 
```
ansible-playbook -i inventory setup_notary_node.yml -e env=production
```

env is variable which can be set to production or development, check how yaml file with assetchains is structured.
