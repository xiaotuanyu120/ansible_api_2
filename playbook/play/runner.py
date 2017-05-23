# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import json

from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase

from playbook.inv_parser import inv_file
from .vart_parser import var_file


class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in
    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result
        This method could store the result in an instance attribute for
        retrieval later
        """
        host = result._host
        print json.dumps({host.name: result._result}, indent=4)


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
        """
        初始化ansible信息，主要是提供playbook_executor类使用的
        options, variable_manager, loader, passwords
        """
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
        # os.environ['ANSIBLE_CONFIG'] =

    def init_variable(self, var_data):
        var_temp_file = var_file(var_data)
        self.variable_manager.add_group_vars_file(var_temp_file, self.loader)

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

    def init_play(self, hosts, module, name='', args=''):
        run_data = dict(
            name = name,
            hosts = hosts,
            gather_facts = 'no',
            tasks = [
                dict(action=dict(module=module, args=args),
                     register='task_out'),
                dict(action=dict(module='debug',
                                 args=dict(msg='{{task_out.stdout}}')))
             ]
        )
        play = Play().load(
            run_data,
            variable_manager=self.variable_manager,
            loader=self.loader
        )
        return play

    def run_play(self, play):
        results_callback = ResultCallback()
        tqm = None
        try:
            tqm = TaskQueueManager(
                      inventory=self.inventory,
                      variable_manager=self.variable_manager,
                      loader=self.loader,
                      options=self.options,
                      passwords=self.passwords,
                    #   stdout_callback=results_callback,
                  )
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
        return result


if __name__ == "__main__":
    runner = AnsibleRunner(connection='ssh',
                           forks=100,
                           become="yes",
                           become_method="sudo",
                           become_user="root",
                           remote_user="gsmcupdate",
                           private_key_file='/root/.ssh/id_rsa',
                           run_data={'role':'test', 'host':'webserver'})
    runner.init_inventory(host_list='../ansible_play/hosts')
    # runner.init_variable('../ansible_play/group_vars/all')

    play = runner.init_play(
        hosts='webserver',
        module="shell",
        args = "ls"
        # args=dict(name="vim", state="latest"),
    )
    runner.run_play(play)
