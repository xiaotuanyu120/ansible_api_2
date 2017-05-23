#
# runner for ansible to run playbook.
#
# EXAMPLE USAGE:
# ansible_option = "../conf/ansible_option.json"
# run_data = {'role': 'test', 'host': 'webserver'}
# host_list='../../ansible_play/hosts'
# playbooks="../../ansible_play/test.yml"
#

from pbex import AnsibleRunner

__all__ = ['Runner']


class Runner(object):

    def __init__(self, ansible_option='', run_data='', host_list='',
                 playbooks=''):
        self.ansible_runner = AnsibleRunner(
                                  ansible_option=ansible_option,
                                  run_data=run_data,
                                  host_list=host_list,
                                  playbooks=playbooks
                              )

    def run(self):
        result = self.ansible_runner.run()
        return result
