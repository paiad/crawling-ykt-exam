import customtkinter as ctk
from tkinter import messagebox
import csv
import os

CSV_FILE = "exam_id.csv"

# 设置外观模式
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")


class ExamIdEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Exam ID管理器")

        # 设置窗口大小
        window_width = 400
        window_height = 180

        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # 计算居中位置
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # 设置窗口位置和大小
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)

        # 初始化CSV文件
        self.check_csv_file()

        # 创建UI组件
        self.create_widgets()

        # 加载现有exam_id
        self.load_existing_id()

    def check_csv_file(self):
        """检查并创建CSV文件"""
        if not os.path.exists(CSV_FILE):
            with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["exam_id"])

    def create_widgets(self):
        """创建界面组件"""
        # 主容器
        main_frame = ctk.CTkFrame(self.root, corner_radius=10)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # 标题
        title_label = ctk.CTkLabel(
            main_frame,
            text="Exam ID管理器",
            font=("微软雅黑", 18, "bold")
        )
        title_label.pack(pady=(0, 15))

        # 输入框架
        input_frame = ctk.CTkFrame(main_frame, corner_radius=8)
        input_frame.pack(padx=10, fill="x")

        ctk.CTkLabel(input_frame, text="Exam ID:", font=("微软雅黑", 14)).pack(side="left", padx=5)
        self.id_entry = ctk.CTkEntry(
            input_frame,
            width=300,
            height=35,
            font=("微软雅黑", 14),
            corner_radius=6
        )
        self.id_entry.pack(side="right", padx=5, pady=5, fill="x", expand=True)

        # 保存按钮
        self.save_button = ctk.CTkButton(
            main_frame,
            text="保存修改",
            command=self.save_exam_id,
            font=("微软雅黑", 14),
            height=40,
            corner_radius=10,
            fg_color="#2E8B57",
            hover_color="#3CB371"
        )
        self.save_button.pack(pady=15, fill="x", padx=50)

    def load_existing_id(self):
        """加载已存在的exam_id"""
        try:
            with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader)  # 跳过标题
                row = next(reader, None)
                if row:
                    self.id_entry.delete(0, "end")
                    self.id_entry.insert(0, row[0])
        except Exception as e:
            messagebox.showerror("错误", f"读取文件失败: {str(e)}")

    def save_exam_id(self):
        """保存输入的exam_id到CSV"""
        exam_id = self.id_entry.get().strip()
        if not exam_id:
            messagebox.showwarning("警告", "请输入有效的Exam ID")
            return

        try:
            with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["exam_id"])
                writer.writerow([exam_id])
            messagebox.showinfo("成功", "Exam ID已成功保存")
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {str(e)}")


if __name__ == "__main__":
    root = ctk.CTk()
    app = ExamIdEditor(root)
    root.mainloop()
