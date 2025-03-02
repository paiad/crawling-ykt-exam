> 前提条件：修改主机的代理端口为8080
### Step1
在exam_id.csv输入你需要爬取的考试号

### Step2
进入proxy_script.py所在目录
```bash
mitmdump -s proxy_script.py
```
### Step3
刷新需要爬取的雨课堂的exam的页面，会生成对应的`雨课堂测试-id-{exam—id}.txt文件`

### Step4
运行file_transform.py，生成对应的`雨课堂测试-id-{exam—id}.docx文档`