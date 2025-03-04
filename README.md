> 🚀 **前提条件**：修改主机的代理端口为 **8080** ⚙️  
> （确保代理设置正确，才能愉快地开始爬取哦！）

### 🌟 **Step -1**
配置自己的虚拟环境
```bash
python -m venv mitm_env
```
激活虚拟环境
```bahs
mitm_env\Scripts\activate
```
下载相应的依赖
```bash
pip install mitmproxy
pip install pandas
pip install python-docx   
```


### 🌟 **Step 0**
🍄 在根目录下分别创建`4`个空的文件夹，分别命名为：txt、docs、md、deepseek。
![img](https://cdn.jsdelivr.net/gh/paiad/picture-bed@main/img/ykt-url-v2.png)

### 🌟 **Step 1**  
在 `exam_id.csv`文件 输入你需要爬取的考试号 ✍️ 
![img](https://cdn.jsdelivr.net/gh/paiad/picture-bed@main/img/ykt-url-v4.png)
📌 小贴士：考试号要写对，不然会抓不到数据的啦！

### 🌟 **Step 2**
进入 `proxy_script.py` 所在根目录，然后运行：  
```bash
mitmdump -s proxy_script.py
```  
![img](https://cdn.jsdelivr.net/gh/paiad/picture-bed@main/img/ykt-url-v3.png)
💻 这步会启动代理脚本，准备好捕捉数据吧！

### 🌟 **Step 3**  
刷新需要爬取的 **雨课堂** 的 exam 页面 ✨  
![img](https://cdn.jsdelivr.net/gh/paiad/picture-bed@main/img/ykt-url-v1.png)
完成后，会自动生成对应的 `雨课堂测试-id-{exam—id}.txt` 文件 📄  
🎯 数据到手，离成功又近了一步！

### 🌟 **Step 4**  
🍃 运行 `file_transform.py`，生成对应的 `雨课堂测试-id-{exam—id}.docx` 文档 📜  

### 🌟 **Step 5**(可选)
🍀 运行 `deepseek_deal.py`，将 API_KEY 换为自己的即可实现对应测试问题的答案生成 ✅### 🌟 **Step 5**(可选)

🍀 运行 `md_proxy.py`，可获得md文件夹下的对应的md文档 ✅
