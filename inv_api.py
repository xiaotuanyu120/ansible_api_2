import os
import json
from tempfile import NamedTemporaryFile


def inv_file(inv_data):
    """
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
        else:
            host = "%s\n" % host
            hosts_file.write(host)
    hosts_file.close()
    return hosts_file.name


def inv_json(inv_data_file):
    # if inv_data is file, convert it to json
    if os.path.isfile(inv_data_file):
        _inv_data = {"hosts":[], "groups":{}}
        group_tag = False
        with open(inv_data_file, "r") as f:
            for host in f:
                host = host.strip()
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
    elif isinstance(inv_data_file, list):
        return json.dumps(list)
    elif isinstance(inv_data_file, str):
        return inv_data_file
    else:
        print "inventory data input is wrong format"
        return
