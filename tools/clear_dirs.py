import os
import shutil


def clear_directories():
    # 要清理的目录列表
    directories = ['../res', '../md', '../txt']

    # 获取当前工作目录
    current_dir = os.getcwd()

    # 遍历每个目录
    for dir_name in directories:
        dir_path = os.path.join(current_dir, dir_name)

        # 检查目录是否存在
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            print(f"正在清理目录: {dir_path}")
            try:
                # 遍历目录中的所有文件和子目录
                for item in os.listdir(dir_path):
                    item_path = os.path.join(dir_path, item)
                    # 如果是文件，直接删除
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                        print(f"已删除文件: {item_path}")
                    # 如果是子目录，使用shutil.rmtree删除
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                        print(f"已删除子目录: {item_path}")
                print(f"{dir_name} 目录清理完成")
            except Exception as e:
                print(f"清理 {dir_name} 时出错: {str(e)}")
        else:
            print(f"目录 {dir_name} 不存在，跳过")


if __name__ == "__main__":
    print("开始清理 res、md、txt 目录下的所有文件...")
    clear_directories()
    print("清理完成！")
