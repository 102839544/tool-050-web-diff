#!/usr/bin/env python3
"""
web-diff - 网页内容对比工具
工具编号: tool-050
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import urllib.request
import urllib.error

class App:
    def __init__(self, root):
        self.root = root
        root.title("网页内容对比工具 v1.0")
        root.geometry("900x700")
        self.setup_ui()
    
    def setup_ui(self):
        # 标题
        title_frame = tk.Frame(self.root, bg="#00BCD4", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        tk.Label(title_frame, text="🌐 网页内容对比工具", font=("Arial", 18, "bold"),
                 fg="white", bg="#00BCD4").pack(pady=15)
        
        # 主区域
        main = tk.Frame(self.root, padx=20, pady=15)
        main.pack(fill="both", expand=True)
        
        # URL输入
        url_frame = tk.Frame(main)
        url_frame.pack(fill="x", pady=10)
        
        tk.Label(url_frame, text="🔗 URL:", font=("Arial", 10, "bold")).pack(side="left")
        self.url_var = tk.StringVar()
        tk.Entry(url_frame, textvariable=self.url_var, width=60).pack(side="left", padx=10)
        tk.Button(url_frame, text="执行", command=self.execute,
                  bg="#00BCD4", fg="white", padx=20, pady=5).pack(side="left")
        
        # 结果区域
        result_frame = tk.LabelFrame(main, text="📄 结果", font=("Arial", 10, "bold"))
        result_frame.pack(fill="both", expand=True, pady=10)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD,
                                                      font=("Consolas", 10))
        self.result_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 进度
        self.progress = ttk.Progressbar(main, mode='indeterminate')
        self.progress.pack(fill="x", pady=10)
        
        # 操作按钮
        btn_frame = tk.Frame(main)
        btn_frame.pack(fill="x", pady=10)
        
        tk.Button(btn_frame, text="💾 保存结果", command=self.save_result,
                  bg="#4CAF50", fg="white", padx=15, pady=8).pack(side="left", padx=5)
        tk.Button(btn_frame, text="🗑️ 清空", command=self.clear_result,
                  bg="#f44336", fg="white", padx=15, pady=8).pack(side="left", padx=5)
        
        # 状态
        self.status_var = tk.StringVar(value="就绪")
        tk.Label(main, textvariable=self.status_var, fg="gray").pack(fill="x")
    
    def execute(self):
        url = self.url_var.get()
        if not url:
            messagebox.showwarning("提示", "请输入URL！")
            return
        
        self.status_var.set("处理中...")
        self.progress.start(10)
        
        try:
            if not url.startswith("http"):
                url = "https://" + url
            
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            with urllib.request.urlopen(req, timeout=10) as resp:
                content = resp.read().decode('utf-8', errors='ignore')
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(1.0, content[:5000])  # 限制显示
            
            self.status_var.set("✅ 完成")
        except Exception as e:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, f"错误: {str(e)}")
            self.status_var.set("❌ 失败")
        finally:
            self.progress.stop()
    
    def save_result(self):
        file = filedialog.asksaveasfilename(
            title="保存结果",
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if file:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(self.result_text.get(1.0, tk.END))
            messagebox.showinfo("成功", f"已保存到: {file}")
    
    def clear_result(self):
        self.result_text.delete(1.0, tk.END)
        self.status_var.set("已清空")

def main():
    root = tk.Tk()
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
