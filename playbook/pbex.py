# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import json
import yaml

from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from ansible.executor.task_queue_manager import TaskQueueManager

from inv_parser import inv_file
from option_parser import options_json


__all__ = ['AnsibleRunner']


class ResultCallback(CallbackBase):
    """
    customized callback
    """

    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        json_result = json.dumps({host.name: result._result}, indent=4)
        print json_result
        return json_result


class CustomInventory(Inventory):
    """
    host inventory for ansible.
    customize host input only.
    """

    def __init__(self, loader, variable_manager, host_list):
        super(CustomInventory, self).__init__(loader,
                                              variable_manager,
                                              host_list)
        self.host_list_file = host_list = inv_file(host_list)

    def get_host_list_file(self):
        return self.host_list_file


class CustomPlaybookExecutor(PlaybookExecutor):
    """
    customized pbex, just add customized callback
    """

    def __init__(self, playbooks, inventory, variable_manager, loader, options, passwords, stdout_callback):
        super(CustomPlaybookExecutor, self).__init__(playbooks, inventory, variable_manager, loader, options, passwords)
        self._stdout_callback = stdout_callback
        if options.listhosts or options.listtasks or options.listtags or options.syntax:
            self._tqm = None
        else:
            self._tqm = TaskQueueManager(inventory=inventory, variable_manager=variable_manager, loader=loader, options=options, passwords=self.passwords, stdout_callback=self._stdout_callback)


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
    """
    runner for ansible
    """

    def __init__(self, ansible_option=None, vault_pass='', run_data=None,
                 host_list='', playbooks=''):
        if not ansible_option:
            ansible_option = "../conf/default_ansible_option.json"
        ansible_option = options_json(ansible_option)
        ansible_option = yaml.safe_load(ansible_option)
        self.options = Options()
        _options = [x for x in dir(self.options) if not x.startswith("__")]
        for k, v in ansible_option.items():
            if k in _options:
                self.options.k = v

        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.passwords = dict(vault_pass=vault_pass)
        self.variable_manager.extra_vars = run_data

        self.inventory = CustomInventory(
                             loader=self.loader,
                             variable_manager=self.variable_manager,
                             host_list=host_list
                         )
        os.remove(self.inventory.get_host_list_file())
        self.variable_manager.set_inventory(self.inventory)
        self.result_callback = ResultCallback()
        self.pbex = CustomPlaybookExecutor(
                        playbooks=[playbooks],
                        inventory=self.inventory,
                        variable_manager=self.variable_manager,
                        loader=self.loader,
                        options=self.options,
                        passwords=self.passwords,
                        stdout_callback=self.result_callback)

    def run(self):
        result = self.pbex.run()
        return result
