> 🚀 **前提条件**：在执行Step2时，应先修改主机的代理端口为 **8080** 
> 
> （确保代理设置正确，才能愉快地开始爬取哦！）

## 获得考试内容
### 🌟 **Step -1**
- 根据requirements.txt下载相应的依赖
```bash
pip install -r requirements.txt
```

### 🌟 **Step 0**
- 在根目录下分别创建n个空的文件夹，分别命名为：txt、md、cache、contrast、res。

### 🌟 **Step 1**  
- 在 `exam_id.csv`文件 输入你需要爬取的考试号
### 🌟 **Step 2**
- 进入项目所在根目录，然后运行：  
```bash
mitmdump -s proxy_script.py
```
**Important**:
>运行以上命令之后，为了使客户端信任 mitmproxy 提供的 CA 证书，从而拦截和解密 HTTPS 请求的具体内容。
- 访问网址[http://mitm.it](http://mitm.it), 根据系统下载并安装相应的证书
### 🌟 **Step 3**
- 刷新需要爬取的 **雨课堂** 的 exam 页面
完成后，会自动生成对应的 `雨课堂测试-id-{exam—id}.txt` 文件(txt文件夹下)

>之后只要配置port: 8080，然后在填写exam_id正确的情况下，运行以下命令，
```bash
mitmdump -s proxy_script.py
```
即可得到对应的雨课堂测试-id-xxxxxx.txt(位于txt dic)

## 获得考试笔记
>[!important]
> 填写exam_id -> run md_script.py (获得考试内容及答案笔记)

```bash
mitmdump -s md_script.py
```  

## 快速校对答案(Options)
### other.csv
填写other的Token，执行paiad_http.py(tools)
>[!note]
> exam_id -> cache_res.py -> 得到 personal.csv-> contrast.py(tools) -> commit.py

输入exam_id后，执行以下命令，会在cache文件夹中出现personal.csv文件
```bash
mitmdump -s cache_res.py
```  

拿到别人的csv文件，命名为other.csv，放置于cache目录下，之后执行run contrast.py，接下来执行以下命令
```bash
mitmdump -s commit.py
```
可以获得标注别人不一样的考试文档