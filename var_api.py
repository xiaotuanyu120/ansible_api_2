# coding=utf-8

import os
import json
import yaml

from tempfile import NamedTemporaryFile


class MyDumper(yaml.Dumper):
    """
    customize Dumper to make yaml.dump() with indent style
    """
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


def var_file(var_data):
    """
    provide variable file.

    accept data:
    - yaml file
    - str(string of a list)
    - list

    save var_data to a file, return file name
    """
    var_data = var_json(var_data)
    if not var_data:
        return
    var_data = yaml.safe_load(var_data)

    var_f = NamedTemporaryFile(delete=False)
    yaml.dump(var_data, var_f,
              allow_unicode=True,
              Dumper=MyDumper,
              default_flow_style=False,
              explicit_start="---")
    var_f.close()
    return var_f.name


def var_json(var_data):
    "convert var_data to json"
    if os.path.isfile(var_data):
        with open(var_data, 'r') as stream:
            try:
                _var_data = yaml.load(stream)
            except yaml.YAMLError as e:
                raise e
                return
        return json.dumps(_var_data)
    elif isinstance(var_data, list):
        return json.dumps(list)
    elif isinstance(var_data, str):
        return var_data
    else:
        print("Wrong format!")
        return


if __name__ == '__main__':
    result = var_file("./test.yml")
    print(result)
