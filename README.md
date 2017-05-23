# ansible_api_2 项目简介
ansible api 2.0 相比 ansible api 1.0 改变很大，按照官方的话讲，新的api 2.0更加易于维护和扩展，也更加稳定。并且他们无意去封装一个类似于api 1.0中的runner类。

ansible api 2.0带来复杂性的同时，灵活性也大大增加，我们可以灵活组建自己的runner类。虽然官方提供了一个[api2的示例](http://docs.ansible.com/ansible/dev_guide/developing_api.html)，但是这个文档过于简陋，并且直接在代码里面直接写play的方式并不好用(可能是由于我水平低)。而根据[这篇api2研究文档](https://serversforhackers.com/running-ansible-2-programmatically)受到的启发，显然playbook_executor的方式更简单易用一些，我们需要做的仅仅是管理好我们的playbook文件，并将它们传到我们自己的api封装的runner中。ansible_api_2综合各种解决方案的优点和缺点采取了playbook_executor的方法。

---
## QUICK START
### 1. 获取项目文件
``` bash
git clone https://github.com/xiaotuanyu120/ansible_api_2.git
pip install -r ansible_api_2/requirements.txt
```
当获取了ansible_api_2的项目代码后，你可以将ansible_api_2目录中的conf,pb_data,playbook这三个目录mv到你自己的项目下合适的位置上。

关于上面三个目录，下面是详细介绍：
- conf, 里面存放的是playbook运行需要的options的一些配置信息，以json文件格式存放，配置可以参照`conf/default_ansible_option.json`内容
- playbook, 主要的项目代码，里面是ansible_api_2封装的自己的runner
- pb_data, 这个目录用于存放playbook运行所需要的yaml文件,roles目录和变量文件等，就和本地使用ansible所创建的目录一样


### 2. 关于传入给Runner的数据
#### 1) ansible_option
ansible_option是ansible需要的options参数，主要包含了一些类似于"become"、"become_method"、"private_key_file"等配置。  
可接收json数据或者json文件。  
> 详细配置可参照`conf/default_ansible_option.json`  
> 推荐将配置文件以json格式放置在conf下面,conf目录最好和playbook目录同级

#### 2) run_data
run_data是ansible需要的extra_vars参数，run_data必须是dict类型。

#### 3) host_list
host_list是ansible需要的inventory数据，可接收json数据，list或inventory文件  
json格式类似于:  
'[{"groupA": ["192.168.0.11", "w1 ansible_host=192.168.0.22 ansible_port=222"]}, {"groupB": ["192.168.0.11"]}, "192.168.0.1"]'
> 如果是inventory文件的话，推荐放置在pb_data目录下

#### 4) playbooks
playbooks是ansible需要的playbook文件，仅可接收yaml文件
> 推荐放置在pb_data目录下

### 3. DEMO
以下是一个调用示例
``` python
from playbook import Runner


ansible_option = "conf/your_ansible_option.json"
run_data = {'role': 'your_role', 'host': 'your_host'}
host_list='pb_data/hosts'
playbooks="pb_data/test.yml"

runner = Runner(ansible_option=ansible_option,
                run_data=run_data,
                host_list=host_list,
                playbooks=playbooks)

runner.run()
```
