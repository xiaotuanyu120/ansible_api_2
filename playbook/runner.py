# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor

from inv_parser import inv_file


class Options(object):
    def __init__(self, vault_pass='', connection='local', module_path='',
                 forks=100, become=None, become_method=None, become_user=None,
                 remote_user=None, check=False, listhosts=None, listtasks=None,
                 listtags=None, syntax=None, private_key_file=None):
        self.connection = connection
        self.module_path = module_path
        self.forks = forks
        self.become = become
        self.become_method = become_method
        self.become_user = become_user
        self.remote_user = remote_user
        self.check = check
        self.listhosts = listhosts
        self.listtasks = listtasks
        self.listtags = listtags
        self.syntax = syntax
        self.private_key_file = private_key_file


class AnsibleRunner(object):
    def __init__(self, vault_pass='', connection='local', module_path='',
                 forks=100, become=None, become_method=None, become_user=None,
                 remote_user=None, check=False, private_key_file=None,
                 run_data=None):
        self.options = Options(
            connection = connection,
            forks = forks,
            become = become,
            become_method = become_method,
            become_user = become_user,
            remote_user = remote_user,
            private_key_file = private_key_file,
        )

        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.passwords = dict(vault_pass=vault_pass, ansible_ssh_pass='123456')
        self.variable_manager.extra_vars = run_data

    def init_inventory(self, host_list='localhost'):
        """
        host_list accept json or file
        """
        host_list = inv_file(host_list)
        self.inventory = Inventory(loader=self.loader,
                                   variable_manager=self.variable_manager,
                                   host_list=host_list)
        os.remove(host_list)
        self.variable_manager.set_inventory(self.inventory)

    def init_playbook(self, playbooks):
        """
        playbooks accept yaml file
        """
        self.pbex = PlaybookExecutor(playbooks=[playbooks],
                                     inventory=self.inventory,
                                     variable_manager=self.variable_manager,
                                     loader=self.loader,
                                     options=self.options,
                                     passwords=self.passwords)

    def run_playbook(self):
        result = self.pbex.run()
        return result


if __name__ == "__main__":
    runner = AnsibleRunner(connection='paramiko',
                           forks=100,
                           become="yes",
                           become_method="sudo",
                           become_user="root",
                           remote_user="gsmcupdate",
                           private_key_file='/root/.ssh/id_rsa',
                           run_data={'role':'test', 'host':'webserver'})
    runner.init_inventory(host_list='../ansible_play/hosts')
    runner.init_playbook(playbooks="../ansible_play/test.yml")
    result = runner.run_playbook()
