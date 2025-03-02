> 🚀 **前提条件**：修改主机的代理端口为 **8080** ⚙️  
> （确保代理设置正确，才能愉快地开始爬取哦！）

### 🌟 **Step 1**  
在 `exam_id.csv`文件 输入你需要爬取的考试号 ✍️  
📌 小贴士：考试号要写对，不然会抓不到数据的啦！

### 🌟 **Step 2**  
进入 `proxy_script.py` 所在根目录，然后运行：  
```bash
mitmdump -s proxy_script.py
```  
💻 这步会启动代理脚本，准备好捕捉数据吧！

### 🌟 **Step 3**  
刷新需要爬取的 **雨课堂** 的 exam 页面 ✨  
完成后，会自动生成对应的 `雨课堂测试-id-{exam—id}.txt` 文件 📄  
🎯 数据到手，离成功又近了一步！

### 🌟 **Step 4**  
运行 `file_transform.py`，生成对应的 `雨课堂测试-id-{exam—id}.docx` 文档 📜  
