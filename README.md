# ansible api 2 研究
api 2.0时代和1.0时代改变特别多，相当于把很多原生的类拿出来用，自己要想跟api1.0时代一样方便的话，需要自己去封装。  
带来复杂性的同时，灵活性也大大增加，我们可以很方便的基于play来创建自己的task或者直接写成yaml文件，然后用playbook_executor来加载yaml文件执行，很多方案，就看我们自己希望如何去使用，当然，加载文件的是最方便的，因为一旦我们考虑使用ansible api，就基本上已经形成了成熟的ansible playbook的文件体系了。  

本项目目前封装的api在ansible需要的三个输入部分做了以下处理
- ansible配置和ssh部分目前是写死在程序里面
- inventory部分可接受文件或者json数据(格式参见inv_api中的介绍)或者list
- playbook目前是用文件或者路径

---

### pbex_runner
主程序，使用playbook_executor来直接执行一个playbook文件  
使用时需要传入以下参数：
- inventory的json信息或者inventory文件
- playbook文件的目录路径
- playbook使用的extra_vars参数(run_data)

---

### inv_api
接收inventory文件的json信息，返回一个临时文件名称，被pbex_runner调用  
json格式类似于:  
'[{"groupA": ["192.168.0.11", "w1 ansible_host=192.168.0.22 ansible_port=222"]}, {"groupB": ["192.168.0.11"]}, "192.168.0.1"]'
