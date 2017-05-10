# ansible api 2 研究

---

### pbex_runner
主程序，使用playbook_executor来直接执行一个playbook文件  
使用时需要传入inventory的json信息和playbook文件的目录路径

---

### inv_api
接收inventory文件的json信息，返回一个临时文件名称，被pbex_runner调用  
json格式类似于:  
'[{"groupA": ["192.168.0.11", "w1 ansible_host=192.168.0.22 ansible_port=222"]}, {"groupB": ["192.168.0.11"]}, "192.168.0.1"]'
