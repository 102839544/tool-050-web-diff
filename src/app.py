#!/usr/bin/env python3
"""
网页内容对比工具 - 检测网页变化
"""
import sys, hashlib, tkinter as tk
from tkinter import messagebox, scrolledtext
import urllib.request
from datetime import datetime

class App:
    def __init__(self, root):
        self.root = root
        root.title("网页内容对比工具 v1.0")
        root.geometry("750x550")
        self.snapshots = {}
        self.build_ui()
    
    def build_ui(self):
        f = tk.Frame(self.root, bg="#512da8", height=50)
        f.pack(fill="x")
        tk.Label(f, text="🔄 网页内容对比工具", font=("Arial",14,"bold"),
                 fg="white", bg="#512da8").pack(pady=12)
        
        main = tk.Frame(self.root, padx=15, pady=10)
        main.pack(fill="both", expand=True)
        
        # URL输入
        uf = tk.Frame(main)
        uf.pack(fill="x", pady=5)
        tk.Label(uf, text="网址：").pack(side="left")
        self.url_entry = tk.Entry(uf, font=("Arial",10), width=50)
        self.url_entry.pack(side="left", padx=5, fill="x", expand=True)
        self.url_entry.insert(0, "https://example.com")
        
        bf = tk.Frame(main)
        bf.pack(fill="x", pady=5)
        tk.Button(bf, text="抓取快照", command=self.take_snapshot,
                  bg="#512da8", fg="white", padx=15).pack(side="left", padx=5)
        tk.Button(bf, text="对比变化", command=self.compare,
                  bg="#4caf50", fg="white", padx=15).pack(side="left", padx=5)
        
        # 快照列表
        lf = tk.LabelFrame(main, text="快照记录", padx=5, pady=5)
        lf.pack(fill="x", pady=10)
        self.lb = tk.Listbox(lf, font=("Consolas",9), height=4)
        self.lb.pack(fill="x")
        
        # 结果
        tk.Label(main, text="内容：", font=("Arial",10,"bold")).pack(anchor="w")
        self.content_txt = scrolledtext.ScrolledText(main, font=("Consolas",9), height=15)
        self.content_txt.pack(fill="both", expand=True)
        
        self.status = tk.Label(main, text="抓取网页快照并对比变化",
                               font=("Arial",10), fg="gray")
        self.status.pack()
    
    def take_snapshot(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("提示", "请输入网址")
            return
        
        try:
            self.status.config(text="抓取中...")
            self.root.update()
            
            req = urllib.request.Request(url, headers={
                "User-Agent": "WebDiff/1.0"
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = resp.read().decode("utf-8", errors="ignore")
            
            content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            key = f"{timestamp} (hash:{content_hash})"
            self.snapshots[key] = content
            self.lb.insert(0, key)
            
            self.content_txt.delete(1.0, "end")
            self.content_txt.insert(1.0, f"Hash: {content_hash}\n\n{content[:2000]}")
            
            self.status.config(text=f"✅ 快照已保存（Hash: {content_hash}）")
        except Exception as e:
            messagebox.showerror("错误", str(e))
            self.status.config(text="❌ 抓取失败")
    
    def compare(self):
        items = self.lb.curselection()
        if len(items) < 2:
            messagebox.showwarning("提示", "请选择两个快照进行对比（按住Ctrl多选）")
            return
        
        key1 = self.lb.get(items[0])
        key2 = self.lb.get(items[1])
        content1 = self.snapshots.get(key1, "")
        content2 = self.snapshots.get(key2, "")
        
        # 简单对比
        lines1 = content1.split("\n")
        lines2 = content2.split("\n")
        
        result = f"对比结果：\n"
        result += f"快照1: {key1}\n"
        result += f"快照2: {key2}\n\n"
        
        if content1 == content2:
            result += "✅ 内容完全相同，无变化"
        else:
            result += f"❌ 内容有变化\n"
            result += f"快照1: {len(lines1)} 行\n"
            result += f"快照2: {len(lines2)} 行\n"
            result += f"字符差异: {abs(len(content1) - len(content2))}"
        
        self.content_txt.delete(1.0, "end")
        self.content_txt.insert(1.0, result)
        self.status.config(text="对比完成")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
