# 文件: number_formatter
# 作者: bao0
# 创建日期: 2025/3/21
# 描述: 这是一个数字格式化工具
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pyperclip


class NumberFormatterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("数字格式化工具")
        self.root.geometry("800x600")

        # 创建主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 创建输入区域
        input_label = ttk.Label(main_frame, text="输入数据（从Excel复制的数据）：")
        input_label.grid(row=0, column=0, sticky=tk.W, pady=5)

        self.input_text = scrolledtext.ScrolledText(main_frame, width=80, height=10)
        self.input_text.grid(row=1, column=0, columnspan=2, pady=5)

        # 创建按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="从剪贴板粘贴", command=self.paste_from_clipboard).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="格式化", command=self.format_numbers).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="复制结果", command=self.copy_to_clipboard).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="清空", command=self.clear_all).pack(side=tk.LEFT, padx=5)

        # 创建输出区域
        output_label = ttk.Label(main_frame, text="格式化结果：")
        output_label.grid(row=3, column=0, sticky=tk.W, pady=5)

        self.output_text = scrolledtext.ScrolledText(main_frame, width=80, height=10)
        self.output_text.grid(row=4, column=0, columnspan=2, pady=5)

        # 配置网格权重
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)

    def paste_from_clipboard(self):
        """从剪贴板粘贴数据"""
        try:
            clipboard_data = pyperclip.paste()
            self.input_text.delete(1.0, tk.END)
            self.input_text.insert(tk.END, clipboard_data)
        except Exception as e:
            messagebox.showerror("错误", f"从剪贴板粘贴失败：{str(e)}")

    def format_numbers(self):
        """格式化数字"""
        try:
            input_data = self.input_text.get(1.0, tk.END).strip()
            lines = input_data.split('\n')

            formatted_numbers = []
            for line in lines:
                # 分割每行的数字
                numbers = line.split()
                for num in numbers:
                    try:
                        # 尝试转换为浮点数并去掉小数点后的.0
                        num = float(num)
                        if num.is_integer():
                            formatted_num = str(int(num))
                        else:
                            formatted_num = str(num)
                        formatted_numbers.append(formatted_num)
                    except ValueError:
                        # 如果不是数字，保持原样
                        formatted_numbers.append(num)

            # 用逗号连接所有数字并显示结果
            result = ','.join(formatted_numbers)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, result)

        except Exception as e:
            messagebox.showerror("错误", f"格式化失败：{str(e)}")

    def copy_to_clipboard(self):
        """复制结果到剪贴板"""
        try:
            result = self.output_text.get(1.0, tk.END).strip()
            pyperclip.copy(result)
            messagebox.showinfo("成功", "结果已复制到剪贴板！")
        except Exception as e:
            messagebox.showerror("错误", f"复制到剪贴板失败：{str(e)}")

    def clear_all(self):
        """清空所有内容"""
        self.input_text.delete(1.0, tk.END)
        self.output_text.delete(1.0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = NumberFormatterGUI(root)
    root.mainloop()
