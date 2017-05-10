import json
from tempfile import NamedTemporaryFile


def inv_file(hosts_data)
    """
    hosts_data must be json like this:
    '[{"groupA": ["192.168.0.11", "w1 ansible_host=192.168.0.22 ansible_port=222"]}, {"groupB": ["192.168.0.11"]}, "192.168.0.1"]'

    we can define group or single host in this data structure
    """
    hosts = json.loads(hosts_data)
    hosts_file = NamedTemporaryFile(delete=False)
    for line in hosts:
        if isinstance(line, dict):
            for group, items in line.items():
                group = "[%s]" % group
                hosts_file.write(group)
                for item in items:
                    hosts_file.write(item)
        else:
            hosts_file.write(line)
    hosts_file.close()
    return host_file.name
