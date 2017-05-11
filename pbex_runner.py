# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor

from inv_api import inv_file


class AnsibleRunner(object):
    def __init__(self, vault_pass='', connection='local', module_path='',
                 forks=100, become=None, become_method=None, become_user=None,
                 remote_user=None, check=False, listhosts=None, listtasks=None,
                 listtags=None, syntax=None, private_key_file=None):
        """
        初始化ansible信息，主要是提供playbook_executor类使用的
        options, variable_manager, loader, passwords
        """
        Options = namedtuple('Options',
                             ['connection',
                              'module_path',
                              'forks',
                              'become',
                              'become_method',
                              'become_user',
                              'remote_user',
                              'check',
                              'listhosts',
                              'listtasks',
                              'listtags',
                              'syntax',
                              'private_key_file'])
        self.options = Options(connection=connection,
                               module_path=module_path,
                               forks=forks,
                               become=become,
                               become_method=become_method,
                               become_user=become_user,
                               remote_user=remote_user,
                               check=check,
                               listhosts=listhosts,
                               listtasks=listtasks,
                               listtags=listtags,
                               syntax=syntax,
                               private_key_file=private_key_file)
        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.passwords = dict(vault_pass=vault_pass)

    def init_inventory(self, host_list='localhost'):
        """
        初始化inventory
        host_list接受json数据传递给inv_api的inv_file
        """
        host_list = inv_file(host_list)
        self.inventory = Inventory(loader=self.loader,
                                   variable_manager=self.variable_manager,
                                   host_list=host_list)
        os.remove(host_list)
        self.variable_manager.set_inventory(self.inventory)

    def init_playbook(self, playbooks):
        """
        使用playbook exexutor来直接执行playbook文件
        playbooks需要转换成list，否则无法被迭代，playbooks是一个文件或者路径
        """
        self.pbex = PlaybookExecutor(playbooks=[playbooks],
                                     inventory=self.inventory,
                                     variable_manager=self.variable_manager,
                                     loader=self.loader,
                                     options=self.options,
                                     passwords=self.passwords)

    def run_it(self):
        result = self.pbex.run()
        return result


if __name__ == "__main__":
    runner = AnsibleRunner(connection='paramiko', forks=100, become="yes",
                           become_method="sudo", become_user="root",
                           remote_user="gsmcupdate",
                           private_key_file='/root/.ssh/id_rsa')
    runner.init_inventory(host_list='./hosts')
    runner.init_playbook(playbooks="./test.yml")
    result = runner.run_it()
