# ansible_api_2

---

## 0. 项目简介
`ansible api 2.0`相比`ansible api 1.0`改变很大，按照官方的话讲，`ansible api 2.0`更加易于维护和扩展，也更加稳定。  

`ansible api 2.0`中更多的是把ansible使用的原生类提供出来，并且声称他们无意去封装一个类似于api 1.0中的runner类，而是把更多的精力放在了他们应该努力的地方。  

这样的话，如果希望使用api，我们就只能自己去封装自己的ansible runner。`ansible_api_2`就是希望能够实现一个比较简单易用的runner2.0。

`ansible api 2.0`带来复杂性的同时，灵活性也大大增加，我们可以灵活组建自己的runner类。  

虽然官方提供了一个[api2的示例](http://docs.ansible.com/ansible/dev_guide/developing_api.html)，但是这个文档过于简陋，并且直接在代码里面直接写play的方式并不好用(可能是由于我水平低)。而根据这篇[api2研究文档](https://serversforhackers.com/running-ansible-2-programmatically)受到的启发，显然playbook_executor的方式更简单易用一些，我们需要做的仅仅是管理好我们的playbook文件，并将它们传到我们自己的api封装的runner中。  

`ansible_api_2`希望更多的关注在playbook yaml文件的编写、hosts和运行时传入的参数(extra_vars)上，这样更贴近我们手动管理ansible的方式。于是最终采用了playbook_executor直接来执行playbook yaml文件这种方法。
> 对于playbook的yaml文件是手动编写模版还是系统生成，要结合自己的环境来考量。

---
## 1. QUICK START
### 1. 获取ansible_api_2
``` bash
# 假设我们的项目目录是myapp
cd myapp

# 下载ansible_api_2
git clone https://github.com/xiaotuanyu120/ansible_api_2.git
mv ansible_api_2/conf .
mv ansible_api_2/pb_data .
mv ansible_api_2/playbook .

# 安装依赖包
pip install -r ansible_api_2/requirements.txt

# (可选)删除ansible_api_2
rm -rf ansible_api_2
#之所以要删除ansible_api_2目录，是因为我们只需要使用到上面的
#conf、pb_data、playbook这三个目录，其他文件可删除
```
> 当然，你也可以移动ansible_api_2/{conf|pb_data|playbook}到其他位置，只要确保它在你的项目中，并且你可以import它。

> 关于上面三个目录，下面是详细介绍：
> - conf, 里面存放的是playbook运行需要的options的一些配置信息，以json文件格式存放，配置可以参照`conf/default_ansible_option.json`内容
> - playbook, 主要的项目代码，里面是ansible_api_2封装的自己的runner
> - pb_data, 这个目录用于存放playbook运行所需要的yaml文件,roles目录和变量文件等，就和本地使用ansible所创建的目录一样

---

### 2. 关于传入给Runner的数据
#### 1) 配置ansible_option
ansible_option是ansible需要的options参数，主要包含了一些类似于"become"、"become_method"、"private_key_file"等配置。  
可接收json数据或者json文件。  

ansible_option示例：
```
{
   "connection":"paramiko",
   "module_path":"",
   "forks":100,
   "become":"",
   "become_method":"",
   "become_user":"",
   "remote_user":"",
   "check":"",
   "private_key_file":""
}
```
> 详细配置可参照`conf/default_ansible_option.json`  
推荐将配置文件以json格式放置在conf下面,conf目录最好和playbook目录同级  
各option的详细说明参见[ansible文档](http://docs.ansible.com/ansible/intro_configuration.html)

> 如果使用了passphrase包含的key文件，可以增加两个参数
```
{
   "connection":"paramiko",
   ......
   "private_key_file":"path/to/keyfile",
   "ansible_ssh_user":"user",
   "ansible_password":"password",
}
```

#### 2) run_data
run_data是ansible需要的extra_vars参数，run_data必须是dict类型。  

run_data示例
```
{'role': 'your_role', 'host': 'your_host'}
```

#### 3) host_list
host_list是ansible需要的inventory数据。  
> 可接收json数据，list或inventory文件  

host_list示例
``` json
'[{"groupA": ["192.168.0.11", "w1 ansible_host=192.168.0.22 ansible_port=222"]}, {"groupB": ["192.168.0.11"]}, "192.168.0.1"]'
```
> 如果是inventory文件的话，推荐放置在pb_data目录下

#### 4) playbooks
playbooks是ansible需要的playbook文件，仅可接收yaml文件
> 推荐放置在pb_data目录下

### 3. 代码DEMO
以下是一个调用示例`myapp/anisble_api2_test.py`
``` python
from playbook import Runner


ansible_option = "conf/default_ansible_option.json"
run_data = {'role': 'web_restart', 'host': 'web'}
host_list='pb_data/hosts'
playbooks="pb_data/tomcat_restart.yml"

runner = Runner(ansible_option=ansible_option,
                run_data=run_data,
                host_list=host_list,
                playbooks=playbooks)

runner.run()
```
