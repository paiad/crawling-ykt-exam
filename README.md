> 🚀 **前提条件**：在执行**Step2**时，应先修改主机的代理端口为 **8080**

## 获得考试内容
### Step -1
- 根据requirements.txt下载相应的依赖
```bash
pip install -r requirements.txt
```

### Step 0
- 在根目录下分别创建n个空的文件夹，分别命名为：txt、res、md。

### Step 1
- 在 `exam_id.csv`文件 输入你需要爬取的考试号

### Step 2
1. 修改主机的代理端口： **8080**
2. 进入项目所在根目录，然后运行：  
```bash
mitmdump -s proxy_script.py
```
>[!tip]
> 运行以上命令之后，为了使客户端信任 mitmproxy 提供的 CA 证书，从而拦截和解密 HTTPS 请求的具体内容。
> - 访问网址[http://mitm.it](http://mitm.it), 根据系统下载并安装相应的证书

### Step 3
- 刷新需要爬取的 **雨课堂** 的 exam 页面
完成后，会自动生成对应的 `雨课堂测试-id-{exam—id}.txt` 文件(txt dic)

>[!note]
> 上述完成后，此后只要设置好 port: 8080，然后在填写exam_id正确的情况下，运行以下命令，并在此之后刷新对应考试页面
```bash
mitmdump -s proxy_script.py
```
即可得到对应的雨课堂测试-id-xxxxxx.txt(txt dic)

## 获得考试笔记
>[!important]
> 填写exam_id -> run md_script.py (获得考试内容及答案笔记)

```bash
mitmdump -s md_script.py
```