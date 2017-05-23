import os
import json
from tempfile import NamedTemporaryFile


__all__ = ['inv_file']


def inv_file(inv_data):
    """
    provide inventory file.

    accept data:
    - inventory file
    - string(string of a list)
    - list

    save inv_data to to a file, return file name.

    inv_data must be json like this:
    '''[{"groupA": ["192.168.0.11",
    "w1 ansible_host=192.168.0.22 ansible_port=222"]},
    {"groupB": ["192.168.0.11"]}, "192.168.0.1"]'''

    we can define group or single host in this data structure
    """
    inv_data = inv_json(inv_data)
    if not inv_data:
        return
    hosts = json.loads(inv_data)
    hosts_file = NamedTemporaryFile(delete=False)
    for host in hosts:
        if isinstance(host, dict):
            for group, sub_hosts in host.items():
                group = "[%s]\n" % group
                hosts_file.write(group)
                for sub_host in sub_hosts:
                    sub_host = "%s\n" % sub_host
                    hosts_file.write(sub_host)
                hosts_file.write('\n')
        else:
            host = "%s\n\n" % host
            hosts_file.write(host)
    hosts_file.close()
    return hosts_file.name


def inv_json(inv_data):
    # if inv_data is file, convert it to json
    if os.path.isfile(str(inv_data)):
        _inv_data = {"hosts":[], "groups":{}}
        group_tag = False
        with open(inv_data, "r") as f:
            for host in f:
                host = host.strip()
                if not host:
                    continue
                if host.startswith("[") and host.endswith("]"):
                    group_tag = False
                    host= host.split("[")[1].split("]")[0]
                    if not host in _inv_data["groups"].keys():
                        _inv_data["groups"][host] = []
                        group = host
                        group_tag = True
                    else:
                        print "%s duplicated" % host
                        break
                elif not group_tag:
                    _inv_data["hosts"].append(host)
                else:
                    _inv_data["groups"][group].append(host)
        inv_data = [x for x in _inv_data["hosts"]]
        for group in _inv_data["groups"].keys():
            inv_data.append({group:_inv_data["groups"][group]})
        return json.dumps(inv_data)
    elif isinstance(inv_data, list):
        return json.dumps(inv_data)
    elif isinstance(inv_data, str):
        return inv_data
    else:
        print("Wrong format!")
        return
