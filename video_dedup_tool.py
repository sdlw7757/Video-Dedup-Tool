import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import random
import string
import json
import queue
from pathlib import Path
import threading
import re
import hashlib
import webbrowser

# GitHub 仓库地址与标志图标（48x48 PNG，base64 内嵌，无需额外的图片文件）
GITHUB_REPO_URL = "https://github.com/sdlw7757/Video-Dedup-Tool"
GITHUB_LOGO_PNG_B64 = "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"


class VideoDedupTool:
    def __init__(self, root):
        self.root = root
        self.root.title("视频去重工具 - Video Deduplication Tool")
        # 窗口大小自适应屏幕，避免在小屏幕上超出可见区域
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        win_w = min(1700, screen_w - 80)
        win_h = min(1500, screen_h - 80)
        pos_x = max((screen_w - win_w) // 2, 0)
        pos_y = max((screen_h - win_h) // 2, 0)
        self.root.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
        self.root.resizable(True, True)  # 允许调整窗口大小
        self.root.configure(bg='#f0f0f0')
        
        # 获取项目根目录（提前计算，便于以绝对路径定位图标等资源）
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        
        # 设置窗口图标（如果存在的话）
        try:
            self.root.iconbitmap(default=os.path.join(self.project_root, 'icon.ico'))
        except Exception:
            pass
        
        # 文件列表数据: iid -> {"path": 绝对路径, "status": 状态文本}
        self.file_items = {}
        self.file_paths = set()  # 已添加文件的绝对路径集合，用于 O(1) 去重
        
        # UI 更新队列（工作线程 -> 主线程，避免跨线程直接操作控件）
        self._ui_queue = queue.Queue()
        
        # 处理状态控制
        self.is_processing = False
        self.cancel_requested = False
        self.current_process = None
        
        # 功能选项变量（默认勾选时间跳跃和修改MD5值）
        self.mirror_var = tk.BooleanVar()
        self.rgb_shift_var = tk.BooleanVar()
        self.time_jump_var = tk.BooleanVar(value=True)  # 默认勾选
        self.md5_change_var = tk.BooleanVar(value=True)  # 默认勾选
        
        # 新增功能变量
        self.mask_invert_var = tk.BooleanVar()  # 蒙版倒置
        self.mask_invert_value = tk.DoubleVar(value=0.03)  # 蒙版倒置值，默认0.03
        self.frame_sampling_var = tk.BooleanVar()  # 视频抽针
        self.frame_sampling_value = tk.IntVar(value=5)  # 抽针间隔，默认5帧
        self.frame_sampling_random_var = tk.BooleanVar(value=True)  # 随机抽针间隔
        
        # 高级选项
        self.randomize_var = tk.BooleanVar(value=True)  # 参数随机化（每个文件独立取值）
        self.audio_process_var = tk.BooleanVar()  # 音频基础处理（音量微调 + 重采样，不变调）
        
        # 创建界面
        self.create_modern_widgets()
        
        # FFmpeg路径 (使用项目集成的FFmpeg)
        self.ffmpeg_path = os.path.join(self.project_root, "ffmpeg-8.0", "bin", "ffmpeg.exe")
        self.ffprobe_path = os.path.join(self.project_root, "ffmpeg-8.0", "bin", "ffprobe.exe")
        
        # Python路径 (使用项目集成的Python)
        self.python_path = os.path.join(self.project_root, "python", "python.exe")
        
        # 启动 UI 更新队列的消费循环（主线程）
        self.root.after(50, self._drain_ui_queue)
        
        self.log_message(f"项目根目录: {self.project_root}")
        self.log_message(f"FFmpeg路径: {self.ffmpeg_path}")
        self.log_message(f"FFprobe路径: {self.ffprobe_path}")
        self.log_message(f"Python路径: {self.python_path}")
        
        # 检查必要组件
        self.check_dependencies()
        
    # 媒体二进制文件的最小体积（Git LFS 占位文件约 130 字节，会通过简单的存在性检查）
    MIN_BINARY_SIZE = 10000

    # FFmpeg 输出中被视为错误/警告的关键字（仅这些行会写入日志）
    FFMPEG_ERROR_KEYWORDS = (
        'error', 'Error', 'ERROR', 'Invalid', 'invalid', 'failed', 'Failed',
        'not found', 'No such', 'Unable', 'Permission denied', 'deprecated',
    )

    def _is_valid_binary(self, path):
        """校验可执行文件不仅存在，而且体积正常（避免 LFS 占位文件通过检查）"""
        try:
            return os.path.exists(path) and os.path.getsize(path) > self.MIN_BINARY_SIZE
        except OSError:
            return False
        
    def check_dependencies(self):
        """检查必要组件是否可用"""
        missing_components = []
        
        if not self._is_valid_binary(self.ffmpeg_path):
            missing_components.append("FFmpeg (ffmpeg-8.0\\bin\\ffmpeg.exe)")
            
        if not self._is_valid_binary(self.ffprobe_path):
            missing_components.append("FFprobe (ffmpeg-8.0\\bin\\ffprobe.exe)")
            
        # 自带 Python 缺失不算致命：start.bat 支持回退到系统 Python / py 启动器
        if not self._is_valid_binary(self.python_path):
            self.log_message(
                "提示: 未检测到可用的自带 Python（python\\python.exe），"
                "当前使用系统 Python 运行，不影响功能。"
            )
            
        if missing_components:
            missing_list = "\n".join(missing_components)
            error_msg = (
                f"缺少或损坏以下必要组件:\n{missing_list}\n\n"
                "请确保 FFmpeg 组件已完整下载（GitHub ZIP 下载的大文件可能只是占位文件，"
                "需通过 git lfs pull 获取真实程序）。"
            )
            self.log_message(error_msg)
            messagebox.showerror("错误", error_msg)
            
    def create_modern_widgets(self):
        """创建现代化界面组件"""
        # 主框架
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=8)
        
        # 标题区域
        title_frame = tk.Frame(main_frame, bg='#2c3e50', relief=tk.RAISED, bd=0)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            title_frame, 
            text="视频去重工具", 
            font=('Arial', 20, 'bold'), 
            fg='white', 
            bg='#2c3e50',
            pady=15
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame, 
            text="Video Deduplication Tool", 
            font=('Arial', 12), 
            fg='#ecf0f1', 
            bg='#2c3e50',
            pady=5
        )
        subtitle_label.pack()
        
        # GitHub 仓库超链接（带 GitHub 标志，点击打开浏览器）
        github_frame = tk.Frame(title_frame, bg='#2c3e50')
        github_frame.place(relx=1.0, rely=0.0, anchor='ne', x=-15, y=14)
        
        try:
            self.github_icon = tk.PhotoImage(data=GITHUB_LOGO_PNG_B64)
            github_icon_label = tk.Label(github_frame, image=self.github_icon, bg='#2c3e50', cursor='hand2')
            github_icon_label.pack(side=tk.LEFT, padx=(0, 6))
        except Exception:
            github_icon_label = None
        
        github_link_label = tk.Label(
            github_frame,
            text="GitHub 仓库",
            font=('Arial', 10, 'underline'),
            fg='#5dade2',
            bg='#2c3e50',
            cursor='hand2'
        )
        github_link_label.pack(side=tk.LEFT)
        
        for widget in (github_icon_label, github_link_label):
            if widget is not None:
                widget.bind('<Button-1>', lambda event: webbrowser.open(GITHUB_REPO_URL))
        
        # 内容区域
        content_frame = tk.Frame(main_frame, bg='#f0f0f0')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧功能区域
        left_frame = tk.Frame(content_frame, bg='#f0f0f0')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # 右侧说明区域
        right_frame = tk.Frame(content_frame, bg='#f0f0f0', width=250)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        right_frame.pack_propagate(False)
        
        # 文件列表区域
        file_frame = tk.LabelFrame(left_frame, text="文件列表", font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        file_frame.pack(fill=tk.X, pady=(0, 8))
        
        # 工具栏
        toolbar = tk.Frame(file_frame, bg='#f0f0f0')
        toolbar.pack(fill=tk.X, padx=10, pady=(6, 4))
        
        def make_tool_btn(text, command):
            return tk.Button(toolbar, text=text, command=command, bg='#3498db', fg='white',
                             font=('Arial', 9, 'bold'), relief=tk.FLAT, padx=10, pady=3, cursor='hand2')
        
        make_tool_btn("添加文件", self.add_files).pack(side=tk.LEFT)
        make_tool_btn("添加文件夹", self.add_folder).pack(side=tk.LEFT, padx=(6, 0))
        make_tool_btn("移除选中", self.remove_selected).pack(side=tk.LEFT, padx=(6, 0))
        make_tool_btn("清空列表", self.clear_file_list).pack(side=tk.LEFT, padx=(6, 0))
        
        self.count_label = tk.Label(toolbar, text="共 0 个文件", font=('Arial', 9), fg='#7f8c8d', bg='#f0f0f0')
        self.count_label.pack(side=tk.RIGHT)
        
        # 文件列表（Treeview）
        list_container = tk.Frame(file_frame, bg='#f0f0f0')
        list_container.pack(fill=tk.X, padx=10, pady=(0, 8))
        
        self.file_tree = ttk.Treeview(list_container, columns=("name", "status"), show="headings",
                                      height=4, selectmode="extended")
        self.file_tree.heading("name", text="文件名")
        self.file_tree.heading("status", text="状态")
        self.file_tree.column("name", anchor=tk.W, width=420)
        self.file_tree.column("status", anchor=tk.CENTER, width=80, stretch=False)
        self.file_tree.tag_configure('running', foreground='#e67e22')
        self.file_tree.tag_configure('done', foreground='#27ae60')
        self.file_tree.tag_configure('failed', foreground='#e74c3c')
        
        tree_scroll = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=tree_scroll.set)
        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 功能选择区域
        func_frame = tk.LabelFrame(left_frame, text="去重功能", font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        func_frame.pack(fill=tk.X, pady=(0, 8))
        
        # 功能选项容器
        func_container = tk.Frame(func_frame, bg='#f0f0f0')
        func_container.pack(fill=tk.X, padx=10, pady=8)
        
        # 创建功能选项
        funcs = [
            ("水平镜像", "让视频进行左右镜像翻转", self.mirror_var),
            ("RGB偏移", "让视频RGB颜色通道按设置偏移", self.rgb_shift_var),
            ("时间跳跃", "让视频中的帧进行周期性的变速波动", self.time_jump_var),
            ("修改MD5值", "通过重新编码和添加元数据修改文件MD5值", self.md5_change_var),
            ("蒙版倒置", "倒置视频透明度 (0-1)", self.mask_invert_var),
            ("视频抽针", "每隔指定帧数抽取一帧", self.frame_sampling_var)
        ]
        
        for name, desc, var in funcs:
            func_item_frame = tk.Frame(func_container, bg='#f0f0f0')
            func_item_frame.pack(fill=tk.X, pady=3)
            
            checkbox = tk.Checkbutton(func_item_frame, variable=var, bg='#f0f0f0', activebackground='#f0f0f0')
            checkbox.pack(side=tk.LEFT)
            
            func_text_frame = tk.Frame(func_item_frame, bg='#f0f0f0')
            func_text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            tk.Label(func_text_frame, text=name, font=('Arial', 10, 'bold'), bg='#f0f0f0', anchor=tk.W).pack(anchor=tk.W)
            tk.Label(func_text_frame, text=desc, font=('Arial', 9), fg='#7f8c8d', bg='#f0f0f0', anchor=tk.W).pack(anchor=tk.W)
            
            # 为蒙版倒置和视频抽针添加参数输入框
            if name == "蒙版倒置":
                mask_frame = tk.Frame(func_item_frame, bg='#f0f0f0')
                mask_frame.pack(side=tk.RIGHT, padx=(10, 0))
                tk.Label(mask_frame, text="值:", font=('Arial', 9), bg='#f0f0f0').pack(side=tk.LEFT)
                mask_entry = tk.Entry(mask_frame, textvariable=self.mask_invert_value, width=8, font=('Arial', 9))
                mask_entry.pack(side=tk.LEFT, padx=(3, 0))
                
            elif name == "视频抽针":
                sampling_frame = tk.Frame(func_item_frame, bg='#f0f0f0')
                sampling_frame.pack(side=tk.RIGHT, padx=(10, 0))
                tk.Label(sampling_frame, text="间隔:", font=('Arial', 9), bg='#f0f0f0').pack(side=tk.LEFT)
                sampling_entry = tk.Entry(sampling_frame, textvariable=self.frame_sampling_value, width=5, font=('Arial', 9))
                sampling_entry.pack(side=tk.LEFT, padx=(3, 0))
                tk.Label(sampling_frame, text="帧", font=('Arial', 9), bg='#f0f0f0').pack(side=tk.LEFT, padx=(3, 0))
                
                # 随机间隔复选框
                random_checkbox = tk.Checkbutton(sampling_frame, text="随机间隔", variable=self.frame_sampling_random_var, bg='#f0f0f0', activebackground='#f0f0f0')
                random_checkbox.pack(side=tk.LEFT, padx=(5, 0))
        
        # 高级选项区域
        adv_frame = tk.LabelFrame(left_frame, text="高级选项", font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        adv_frame.pack(fill=tk.X, pady=(0, 8))
        
        adv_container = tk.Frame(adv_frame, bg='#f0f0f0')
        adv_container.pack(fill=tk.X, padx=10, pady=6)
        
        tk.Checkbutton(
            adv_container, text="参数随机化：为每个文件独立在安全区间取值，避免批量输出彼此相似",
            variable=self.randomize_var, bg='#f0f0f0', activebackground='#f0f0f0', anchor=tk.W,
            font=('Arial', 9), justify=tk.LEFT
        ).pack(fill=tk.X)
        
        tk.Checkbutton(
            adv_container, text="音频基础处理：音量微调 + 重采样（不改变音调与速度）",
            variable=self.audio_process_var, bg='#f0f0f0', activebackground='#f0f0f0', anchor=tk.W,
            font=('Arial', 9), justify=tk.LEFT
        ).pack(fill=tk.X)
        
        # 处理按钮区域
        button_frame = tk.Frame(left_frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, pady=(0, 8))
        
        # 创建按钮容器以水平排列按钮
        buttons_container = tk.Frame(button_frame, bg='#f0f0f0')
        buttons_container.pack(pady=2)
        
        self.process_btn = tk.Button(
            buttons_container, 
            text="开始处理", 
            command=self.start_processing,
            bg='#27ae60', 
            fg='white', 
            font=('Arial', 11, 'bold'), 
            relief=tk.FLAT, 
            padx=18, 
            pady=6,
            cursor='hand2'
        )
        self.process_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        # 取消按钮
        self.cancel_btn = tk.Button(
            buttons_container, 
            text="取消", 
            command=self.cancel_processing,
            bg='#e67e22', 
            fg='white', 
            font=('Arial', 11, 'bold'), 
            relief=tk.FLAT, 
            padx=18, 
            pady=6,
            cursor='hand2',
            state='disabled'
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        # 清空按钮
        self.clear_btn = tk.Button(
            buttons_container, 
            text="清空", 
            command=self.clear_all,
            bg='#e74c3c', 
            fg='white', 
            font=('Arial', 11, 'bold'), 
            relief=tk.FLAT, 
            padx=18, 
            pady=6,
            cursor='hand2'
        )
        self.clear_btn.pack(side=tk.LEFT)
        
        # 进度区域
        progress_frame = tk.Frame(left_frame, bg='#f0f0f0')
        progress_frame.pack(fill=tk.X, pady=(0, 8))
        
        # 进度条和百分比
        progress_container = tk.Frame(progress_frame, bg='#f0f0f0')
        progress_container.pack(fill=tk.X, pady=2)
        
        self.progress = ttk.Progressbar(progress_container, mode='determinate')
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.progress_label = tk.Label(progress_container, text="0%", font=('Arial', 10, 'bold'), width=5, bg='#f0f0f0')
        self.progress_label.pack(side=tk.RIGHT, padx=(10, 0))
        
        # 状态标签
        self.status_label = tk.Label(
            left_frame, 
            text="请添加视频文件并选择功能", 
            font=('Arial', 10), 
            fg='#7f8c8d', 
            bg='#f0f0f0'
        )
        self.status_label.pack(pady=(0, 8))
        
        # 日志区域
        log_frame = tk.LabelFrame(left_frame, text="处理日志", font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        log_container = tk.Frame(log_frame, bg='#f0f0f0')
        log_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)
        
        self.log_text = tk.Text(log_container, height=4, font=('Consolas', 9), bg='#ffffff', fg='#2c3e50')
        scrollbar = tk.Scrollbar(log_container, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 右侧说明区域
        info_frame = tk.LabelFrame(right_frame, text="功能说明", font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        info_container = tk.Frame(info_frame, bg='#f0f0f0')
        info_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        info_text = tk.Text(info_container, font=('Arial', 9), bg='#f8f9fa', fg='#34495e', wrap=tk.WORD, relief=tk.FLAT)
        info_text.pack(fill=tk.BOTH, expand=True)
        
        # 插入功能说明
        info_content = """文件列表：
支持批量添加文件/文件夹（递归扫描），每项显示处理状态。输出保存到源文件同目录，命名为 原名_dedup.扩展名，已存在时自动加序号避免覆盖。

时间跳跃：
让视频中的帧进行周期性的变速波动（肉眼看不到），通过使用minterpolate滤镜创建微妙的时间波动效果，在保持视频总时长不变的情况下，创建微妙的帧速率变化。

RGB偏移：
让视频 RGB 颜色通道按设置偏移，达到换色目的。通过对RGB通道进行轻微的空间偏移来产生视觉差异。

水平镜像：
让视频进行左右镜像翻转，改变视频的视觉内容但保持内容完整性。

修改MD5值：
通过重新编码视频并添加随机元数据，规避平台重复检测。确保输出文件的MD5值与原文件不同。

蒙版倒置：
通过调整视频透明度来创建视觉变化效果。

视频抽针：
通过抽取特定帧来创建视频变化，减少视频内容（保留原时间戳，不补帧）。

参数随机化：
为每个文件独立在安全区间随机取值（CRF/GOP/B帧/RGB偏移/抽针间隔等），避免批量输出彼此相似。

音频基础处理：
仅做音量微调（volume）与重采样（aresample），不改变音调与播放速度。
"""
        info_text.insert(tk.END, info_content)
        info_text.config(state='disabled')
        
    VIDEO_EXTENSIONS = ('.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm',
                        '.m4v', '.ts', '.mpg', '.mpeg', '.3gp', '.rmvb', '.rm')

    def add_files(self):
        """添加一个或多个视频文件到列表"""
        if self.is_processing:
            messagebox.showwarning("提示", "正在处理中，无法修改列表")
            return
        paths = filedialog.askopenfilenames(
            title="选择视频文件",
            filetypes=[
                ("视频文件", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm *.m4v *.ts *.mpg *.mpeg"),
                ("所有文件", "*.*")
            ]
        )
        if not paths:
            return
        added = sum(1 for p in paths if self._add_path_to_list(p, refresh=False))
        self._update_count()
        self.log_message(f"已添加 {added} 个文件，当前共 {len(self.file_items)} 个")

    def add_folder(self):
        """递归扫描文件夹并添加其中的视频文件"""
        if self.is_processing:
            messagebox.showwarning("提示", "正在处理中，无法修改列表")
            return
        folder = filedialog.askdirectory(title="选择文件夹（将递归扫描其中的视频文件）")
        if not folder:
            return
        added = 0
        skipped = 0
        for root_dir, _dirs, filenames in os.walk(folder):
            for name in filenames:
                if name.lower().endswith(self.VIDEO_EXTENSIONS):
                    if self._add_path_to_list(os.path.join(root_dir, name), refresh=False):
                        added += 1
                    else:
                        skipped += 1
        self._update_count()
        msg = f"从文件夹添加 {added} 个视频，当前共 {len(self.file_items)} 个"
        if skipped:
            msg += f"（跳过重复 {skipped} 个）"
        self.log_message(msg)

    def _add_path_to_list(self, path, refresh=True):
        """将路径加入列表，重复则跳过；返回是否新增"""
        abs_path = os.path.abspath(path)
        if abs_path in self.file_paths:
            return False
        iid = self.file_tree.insert("", tk.END, values=(os.path.basename(abs_path), "待处理"))
        self.file_items[iid] = {"path": abs_path, "status": "待处理"}
        self.file_paths.add(abs_path)
        if refresh:
            self._update_count()
        return True

    def remove_selected(self):
        """移除列表中选中的文件"""
        if self.is_processing:
            messagebox.showwarning("提示", "正在处理中，无法修改列表")
            return
        selected = self.file_tree.selection()
        if not selected:
            return
        for iid in selected:
            info = self.file_items.pop(iid, None)
            if info:
                self.file_paths.discard(info["path"])
            self.file_tree.delete(iid)
        self._update_count()

    def clear_file_list(self):
        """清空文件列表"""
        if self.is_processing:
            messagebox.showwarning("提示", "正在处理中，无法修改列表")
            return
        self.file_tree.delete(*self.file_tree.get_children())
        self.file_items.clear()
        self.file_paths.clear()
        self._update_count()

    def _update_count(self):
        """刷新文件计数标签"""
        self.count_label.config(text=f"共 {len(self.file_items)} 个文件")

    def _set_item_status(self, iid, status):
        """更新列表中某个文件的状态（必须在主线程调用）"""
        info = self.file_items.get(iid)
        if not info:
            return
        info["status"] = status
        tag = {"处理中": "running", "完成": "done", "失败": "failed"}.get(status, "")
        self.file_tree.item(iid, values=(os.path.basename(info["path"]), status), tags=(tag,))

    def _post(self, fn):
        """把 UI 更新回调投递到主线程队列（供工作线程调用）"""
        self._ui_queue.put(fn)

    def _drain_ui_queue(self):
        """在主线程中消费 UI 更新队列（tkinter 不支持从其他线程直接操作控件）"""
        try:
            while True:
                try:
                    fn = self._ui_queue.get_nowait()
                except queue.Empty:
                    break
                try:
                    fn()
                except Exception as e:
                    print(f"UI 更新失败: {e}")
        finally:
            self.root.after(50, self._drain_ui_queue)

    def start_processing(self):
        """开始批量处理（在新线程中）"""
        if self.is_processing:
            return
        if not self.file_items:
            messagebox.showerror("错误", "请先添加要处理的视频文件")
            return
        if not any([self.mirror_var.get(), self.rgb_shift_var.get(),
                    self.time_jump_var.get(), self.md5_change_var.get(),
                    self.mask_invert_var.get(), self.frame_sampling_var.get(),
                    self.audio_process_var.get()]):
            messagebox.showerror("错误", "请至少选择一个功能")
            return
        if not self._is_valid_binary(self.ffmpeg_path) or not self._is_valid_binary(self.ffprobe_path):
            messagebox.showerror(
                "错误",
                "FFmpeg / FFprobe 组件缺失或损坏，请检查 ffmpeg-8.0\\bin 目录"
            )
            return

        # 预先校验并规范化用户输入的数值参数，避免工作线程内抛出难懂的异常
        try:
            mask_value = float(self.mask_invert_value.get())
            sampling_value = int(self.frame_sampling_value.get())
        except (tk.TclError, ValueError):
            messagebox.showerror("错误", "“蒙版倒置值”与“抽针间隔”必须是有效数字")
            return
        if self.mask_invert_var.get() and not (0 < mask_value <= 1):
            messagebox.showerror("错误", "蒙版倒置值需大于 0 且不超过 1")
            return
        if self.frame_sampling_var.get() and sampling_value < 2:
            messagebox.showerror("错误", "抽针间隔必须是大于等于 2 的整数")
            return
        self.mask_invert_value.set(mask_value)
        self.frame_sampling_value.set(sampling_value)

        self.is_processing = True
        self.cancel_requested = False
        self.current_process = None
        self.process_btn.config(state='disabled', bg='#95a5a6', text="处理中...")
        self.cancel_btn.config(state='normal')
        self.clear_btn.config(state='disabled')
        threading.Thread(target=self._process_queue, daemon=True).start()

    def cancel_processing(self):
        """请求取消剩余任务并终止当前 ffmpeg 进程"""
        if not self.is_processing:
            return
        self.cancel_requested = True
        self.cancel_btn.config(state='disabled')
        self.log_message("已请求取消，正在停止当前任务...")
        proc = self.current_process
        if proc is not None and proc.poll() is None:
            try:
                proc.terminate()
            except Exception:
                pass

    def _process_queue(self):
        """串行处理列表中的每个文件（工作线程）"""
        items = list(self.file_items.items())
        total = len(items)
        success = 0
        failed = 0
        self.log_message(f"开始批量处理，共 {total} 个文件")
        self._post(lambda: self.status_label.config(text=f"正在处理 0/{total}...", fg='#e67e22'))

        for idx, (iid, info) in enumerate(items, start=1):
            if self.cancel_requested:
                self.log_message("已取消剩余任务")
                break
            input_path = info["path"]
            if not os.path.exists(input_path):
                self._post(lambda iid=iid: self._set_item_status(iid, "失败"))
                self.log_message(f"[{idx}/{total}] 文件不存在，跳过: {input_path}")
                failed += 1
                continue

            self._post(lambda iid=iid: self._set_item_status(iid, "处理中"))
            self._post(lambda iid=iid: self.file_tree.see(iid))
            self._post(lambda i=idx, t=total: self.status_label.config(text=f"正在处理 {i}/{t}...", fg='#e67e22'))
            self.log_message(f"===== [{idx}/{total}] {os.path.basename(input_path)} =====")

            try:
                output_path = self._build_output_path(input_path)
                self._process_single(input_path, output_path)
                self._post(lambda iid=iid: self._set_item_status(iid, "完成"))
                success += 1
            except Exception as e:
                self.log_message(f"处理失败: {e}")
                if self.cancel_requested:
                    self._post(lambda iid=iid: self._set_item_status(iid, "待处理"))
                else:
                    self._post(lambda iid=iid: self._set_item_status(iid, "失败"))
                    failed += 1

        self._post(lambda: self._on_queue_finished(success, failed, total))

    def _on_queue_finished(self, success, failed, total):
        """批量处理结束后的 UI 复位（主线程）"""
        self.is_processing = False
        self.cancel_requested = False
        self.current_process = None
        self.process_btn.config(state='normal', bg='#27ae60', text="开始处理")
        self.cancel_btn.config(state='disabled')
        self.clear_btn.config(state='normal')
        self.progress.stop()
        self.progress.config(mode='determinate')
        self.progress['value'] = 100
        self.progress_label.config(text="100%")
        summary = f"处理结束：成功 {success}，失败 {failed}，共 {total}"
        self.status_label.config(text=summary, fg='#27ae60' if failed == 0 else '#e67e22')
        self.log_message(summary)
        # 稍后再复位进度条，让用户能看到完成状态
        self.root.after(1000, self._reset_progress)
        messagebox.showinfo("完成", summary)

    def _reset_progress(self):
        """复位进度条"""
        self.progress['value'] = 0
        self.progress_label.config(text="0%")

    def _build_output_path(self, input_path):
        """生成与源文件同目录的输出路径，已存在时自动加序号避免覆盖"""
        p = Path(input_path)
        candidate = p.parent / f"{p.stem}_dedup{p.suffix}"
        if not candidate.exists():
            return str(candidate)
        n = 1
        while True:
            candidate = p.parent / f"{p.stem}_dedup_{n}{p.suffix}"
            if not candidate.exists():
                return str(candidate)
            n += 1

    def _build_params(self, source_fps=0.0):
        """生成单个文件的处理参数（随机化开启时每个文件独立取值）"""
        r = self.randomize_var.get()

        def pick(lo, hi, fixed):
            return random.uniform(lo, hi) if r else fixed

        # RGB 通道偏移量
        if r:
            rgb_offsets = tuple(random.choice([-3, -2, -1, 1, 2, 3]) for _ in range(6))
        else:
            rgb_offsets = (2, -1, 1, 1, -2, 2)

        # 蒙版倒置值：在用户设定值附近轻微浮动（保持在 (0, 1] 合法区间）
        mask_base = min(1.0, max(0.0001, float(self.mask_invert_value.get())))
        if r:
            mask = round(min(1.0, random.uniform(mask_base * 0.6, mask_base * 1.4)), 4)
        else:
            mask = round(mask_base, 4)

        # 抽针间隔：无论是否随机都必须 >= 2，否则 mod(n, 0) 会产出 0 帧的空文件
        sampling_base = max(2, int(self.frame_sampling_value.get()))
        if r:
            sampling = random.randint(sampling_base, sampling_base + 3)
        else:
            sampling = sampling_base

        # 时间跳跃以源帧率为基准（避免把 60fps 源砍成 30fps），随机化时加 ±1% 微抖动
        fps_base = source_fps if source_fps > 0 else 30.0
        fps = round(fps_base * (random.uniform(0.99, 1.01) if r else 1.0), 3)

        return {
            "crf": int(pick(20, 26, 23)),
            "gop": int(pick(48, 72, 60)),
            "bf": int(pick(1, 3, 2)),
            "fps": fps,
            "rgb_offsets": rgb_offsets,
            "mask": mask,
            "sampling": sampling,
            "audio_vol": round(pick(0.98, 1.02, 1.0), 4),
            "audio_sr": random.choice([44100, 48000]) if r else 48000,
        }

    def _file_md5(self, file_path):
        """计算文件 MD5"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def _probe_media(self, video_path):
        """探测媒体信息：是否含音轨、源视频帧率"""
        info = {"has_audio": False, "fps": 0.0}
        try:
            cmd = [self.ffprobe_path, '-v', 'error', '-show_streams', '-of', 'json', video_path]
            result = subprocess.run(cmd, capture_output=True, text=True,
                                    encoding='utf-8', errors='replace')
            if result.returncode != 0 or not result.stdout.strip():
                return info

            for stream in json.loads(result.stdout).get("streams", []):
                codec_type = stream.get("codec_type")
                if codec_type == "audio":
                    info["has_audio"] = True
                elif codec_type == "video" and info["fps"] <= 0:
                    # 跳过内嵌封面图（attached_pic），它不是真正的视频流
                    if stream.get("disposition", {}).get("attached_pic", 0):
                        continue
                    rate = stream.get("avg_frame_rate") or stream.get("r_frame_rate") or ""
                    num, _, den = rate.partition("/")
                    try:
                        den_value = float(den) if den else 1.0
                        if den_value > 0:
                            info["fps"] = float(num) / den_value
                    except (TypeError, ValueError):
                        info["fps"] = 0.0
        except Exception as e:
            print(f"探测媒体信息失败: {e}")
        return info
            
    # 支持内嵌缩略图的容器
    SUPPORTED_THUMB_CONTAINERS = ('.mp4', '.mov', '.m4v', '.mkv')

    def _process_single(self, input_path, output_path):
        """处理单个视频文件（工作线程）"""
        media = self._probe_media(input_path)
        has_audio = media["has_audio"]
        params = self._build_params(media["fps"])

        self.log_message(f"输入文件: {input_path}")
        self.log_message(f"输出文件: {output_path}")
        self.log_message(
            f"源帧率: {media['fps']:.3f} fps，音轨: {'有' if has_audio else '无'}"
        )

        # 是否需要嵌入缩略图（与主转码合并为一次 ffmpeg 调用，避免二次读写整个文件）
        need_thumb = (
            Path(output_path).suffix.lower() in self.SUPPORTED_THUMB_CONTAINERS
            and any([self.mirror_var.get(), self.rgb_shift_var.get(),
                     self.time_jump_var.get(), self.md5_change_var.get(),
                     self.mask_invert_var.get(), self.frame_sampling_var.get(),
                     self.audio_process_var.get() and has_audio])
        )
        thumb_path = None
        if need_thumb:
            thumb_path = self._extract_thumbnail(input_path)
            if thumb_path is None:
                self.log_message("提取缩略图失败，本次不嵌入缩略图")

        try:
            self._run_single_ffmpeg(input_path, output_path, params, has_audio, thumb_path)
        finally:
            if thumb_path and os.path.exists(thumb_path):
                try:
                    os.remove(thumb_path)
                except OSError:
                    pass

        if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            raise Exception("输出文件未生成或为空（参数可能不合法）")

        # MD5 对比
        try:
            src_md5 = self._file_md5(input_path)
            out_md5 = self._file_md5(output_path)
            self.log_message(f"原始MD5: {src_md5}")
            self.log_message(f"新文件MD5: {out_md5}")
            self.log_message("MD5 已变化" if src_md5 != out_md5 else "警告: MD5 未发生变化")
        except Exception as e:
            self.log_message(f"计算MD5失败: {e}")

        self.log_message("视频处理成功完成")

    def _run_single_ffmpeg(self, input_path, output_path, params, has_audio, thumb_path):
        """组装并执行单次 ffmpeg 命令（含可选缩略图嵌入）"""
        cmd = [self.ffmpeg_path, '-y', '-i', input_path]
        if thumb_path:
            cmd.extend(['-i', thumb_path])

        # 视频滤镜链
        filters = []
        if self.mirror_var.get():
            filters.append("hflip")
            self.log_message("应用水平镜像效果")

        if self.rgb_shift_var.get():
            rh, gh, bh, rv, gv, bv = params["rgb_offsets"]
            filters.append(f"rgbashift=rh={rh}:gh={gh}:bh={bh}:rv={rv}:gv={gv}:bv={bv}")
            self.log_message(f"应用RGB偏移效果 {params['rgb_offsets']}")

        if self.time_jump_var.get():
            filters.append(
                f"minterpolate=fps={params['fps']}:mi_mode=blend:mc_mode=aobmc:"
                f"me_mode=bidir:mb_size=16:search_param=32"
            )
            self.log_message("应用时间跳跃效果 (周期性变速波动)")

        if self.mask_invert_var.get():
            filters.append(f"colorchannelmixer=aa={params['mask']}")
            self.log_message(f"应用蒙版倒置效果 (透明度: {params['mask']})")

        if self.frame_sampling_var.get():
            interval = params["sampling"]
            if self.frame_sampling_random_var.get():
                filters.append(f"select='not(mod(n,{interval}+floor(random(0)*6)))'")
                self.log_message(f"应用视频抽针效果 (随机间隔: {interval}-{interval + 5}帧)")
            else:
                filters.append(f"select='not(mod(n,{interval}))'")
                self.log_message(f"应用视频抽针效果 (固定间隔: {interval}帧)")

        if filters:
            # 有缩略图输入时，滤镜只能作用于第 0 个视频流，否则会应用到静态图片
            cmd.extend(['-filter:v:0' if thumb_path else '-vf', ','.join(filters)])

        # 音频基础处理：仅音量微调 + 重采样，不改变音调与速度
        audio_on = self.audio_process_var.get() and has_audio
        if audio_on:
            af = f"volume={params['audio_vol']},aresample={params['audio_sr']}"
            cmd.extend(['-af', af])
            self.log_message(f"应用音频处理: {af}")
        elif self.audio_process_var.get():
            self.log_message("未检测到音轨，跳过音频处理")

        # 显式映射流：嵌入缩略图时避免默认流选择丢掉图片；大写 V 表示排除内嵌封面
        if thumb_path:
            cmd.extend(['-map', '0:V:0', '-map', '0:a?', '-map', '1:v:0'])

        # 编码与元数据层增强
        video_encode = self.md5_change_var.get() or bool(filters)
        if video_encode or audio_on:
            cmd.extend(['-map_metadata', '-1', '-map_chapters', '-1'])
            if video_encode:
                # 有缩略图时用流限定符 ":0" 精确指定第 0 个视频流，
                # 避免 -profile/-pix_fmt/-g/-bf 等被应用到 mjpeg 图片流
                vs = ':0' if thumb_path else ''
                cmd.extend([
                    f'-c:v{vs}', 'libx264',
                    f'-preset:v{vs}', 'ultrafast',
                    f'-crf:v{vs}', str(params["crf"]),
                    f'-profile:v{vs}', 'high',
                    f'-pix_fmt:v{vs}', 'yuv420p',
                    f'-g:v{vs}', str(params["gop"]),
                    f'-bf:v{vs}', str(params["bf"]),
                    '-metadata', f"title=Processed_{self._generate_random_string(8)}",
                    '-metadata', "comment=Video processed with dedup tool",
                ])
                self.log_message(
                    f"重新编码视频（CRF={params['crf']}, GOP={params['gop']}, B帧={params['bf']}, profile=high, yuv420p）"
                )
            else:
                cmd.extend(['-c:v', 'copy'])
            cmd.extend(['-c:a', 'aac', '-b:a', '128k'] if audio_on else ['-c:a', 'copy'])
        else:
            cmd.extend(['-c', 'copy'])
            self.log_message("直接复制视频流")

        # 第二路视频流作为内嵌缩略图
        if thumb_path:
            cmd.extend(['-c:v:1', 'mjpeg', '-disposition:v:1', 'attached_pic'])

        # 使用 select 抽针时保留原时间戳，避免默认补帧导致抽针失效
        if self.frame_sampling_var.get():
            cmd.extend(['-fps_mode', 'vfr'])

        cmd.append(output_path)
        self.log_message(f"执行命令: {' '.join(cmd)}")

        self._run_ffmpeg_with_progress(cmd, input_path)

        if thumb_path:
            self.log_message("缩略图已随转码一并嵌入")

    def _extract_thumbnail(self, video_path):
        """提取一帧作为缩略图，返回临时文件路径；失败返回 None"""
        stamp = self._generate_random_string(8)
        thumb_path = os.path.join(
            os.path.dirname(video_path),
            f"{Path(video_path).stem}_thumb_{stamp}.jpg"
        )
        cmd = [
            self.ffmpeg_path, '-y', '-ss', '00:00:01', '-i', video_path,
            '-frames:v', '1', '-an', '-vf', 'thumbnail,setsar=1',
            '-q:v', '2', thumb_path
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True,
                                    encoding='utf-8', errors='replace')
            if result.returncode == 0 and os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 0:
                return thumb_path
            self.log_message(f"提取缩略图失败: {result.stderr.strip()[:200]}")
        except Exception as e:
            self.log_message(f"提取缩略图时出错: {e}")
        if os.path.exists(thumb_path):
            try:
                os.remove(thumb_path)
            except OSError:
                pass
        return None
        
    def _run_ffmpeg_with_progress(self, cmd, input_path):
        """运行 FFmpeg 并监控进度（只记录错误信息，避免进度行刷屏）"""
        duration = self._get_video_duration(input_path)
        if duration <= 0:
            self.log_message("无法获取视频时长，进度条使用不确定模式")
            self._post(self._start_indeterminate_progress)
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       text=True, encoding='utf-8', errors='replace')
            self.current_process = process
            _, stderr = process.communicate()
            self.current_process = None
            self._post(self._stop_indeterminate_progress)
            self._log_ffmpeg_errors(stderr)
            if process.returncode != 0:
                if self.cancel_requested:
                    raise Exception("任务已被取消")
                raise Exception(f"FFmpeg处理失败，返回码: {process.returncode}")
            return

        self.log_message(f"视频时长: {duration:.2f} 秒")

        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True, encoding='utf-8', errors='replace', bufsize=1
        )
        self.current_process = process

        error_lines = []
        while True:
            if process.stderr is None:
                process.wait()
                break
            output = process.stderr.readline()
            if output == '' and process.poll() is not None:
                break
            if not output:
                continue
            # 解析进度（不写入日志）
            time_match = re.search(r"time=([0-9:.]+)", output)
            if time_match:
                current_time = self._time_str_to_seconds(time_match.group(1))
                if current_time >= 0:
                    percent = min(100, int((current_time / duration) * 100))
                    self._post(lambda p=percent: self._update_progress(p))
            # 仅收集疑似错误/警告的行，且限制条数
            if len(error_lines) < 20 and any(k in output for k in self.FFMPEG_ERROR_KEYWORDS):
                error_lines.append(output.strip())

        rc = process.poll()
        self.current_process = None
        if rc != 0:
            _, stderr = process.communicate()
            self._log_ffmpeg_errors('\n'.join(error_lines) + '\n' + (stderr or ''))
            if self.cancel_requested:
                raise Exception("任务已被取消")
            raise Exception(f"FFmpeg处理失败，返回码: {rc}")
        self._log_ffmpeg_errors('\n'.join(error_lines))

    def _start_indeterminate_progress(self):
        """进入不确定模式进度条"""
        self.progress.config(mode='indeterminate')
        self.progress.start(50)

    def _stop_indeterminate_progress(self):
        """退出不确定模式进度条"""
        self.progress.stop()
        self.progress.config(mode='determinate')
        self.progress['value'] = 0
        self.progress_label.config(text="0%")

    def _log_ffmpeg_errors(self, text, max_chars=1000):
        """仅在存在错误/警告信息时写入日志，并限制长度"""
        cleaned = (text or '').strip()
        if not cleaned:
            return
        self.log_message(f"FFmpeg: {cleaned[:max_chars]}")
            
    def _get_video_duration(self, video_path):
        """获取视频时长（秒）"""
        try:
            cmd = [
                self.ffprobe_path, 
                '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True,
                                    encoding='utf-8', errors='replace')
            if result.returncode == 0 and result.stdout.strip():
                return float(result.stdout.strip())
        except Exception as e:
            self.log_message(f"获取视频时长失败: {e}")
        return -1
        
    def _time_str_to_seconds(self, time_str):
        """将时间字符串转换为秒数"""
        try:
            # 格式: HH:MM:SS.mmm
            parts = time_str.split(':')
            if len(parts) == 3:
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds = float(parts[2])
                return hours * 3600 + minutes * 60 + seconds
        except Exception:
            pass
        return -1
        
    def _update_progress(self, percent):
        """更新进度条"""
        self.progress['value'] = percent
        self.progress_label.config(text=f"{percent}%")
        
    def _generate_random_string(self, length):
        """生成随机字符串"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        
    def log_message(self, message):
        """在日志区域添加消息（统一投递到主线程队列，兼容工作线程调用）"""
        self._post(lambda: self._update_log(message))
        
    def _update_log(self, message):
        """更新日志显示（限制最大行数，避免长时间运行后占用过多内存）"""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + '\n')
        # 超过上限时丢弃最早的 500 行
        if int(self.log_text.index('end-1c').split('.')[0]) > 2000:
            self.log_text.delete('1.0', '500.0')
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)
        
    def clear_all(self):
        """清空文件列表、功能选项与日志，回到初始状态"""
        if self.is_processing:
            messagebox.showwarning("提示", "正在处理中，请先取消后再清空")
            return
        
        # 清空文件列表
        self.file_tree.delete(*self.file_tree.get_children())
        self.file_items.clear()
        self.file_paths.clear()
        self._update_count()
        
        # 重置功能选项到默认值
        self.mirror_var.set(False)
        self.rgb_shift_var.set(False)
        self.time_jump_var.set(True)  # 默认勾选
        self.md5_change_var.set(True)   # 默认勾选
        self.mask_invert_var.set(False)
        self.frame_sampling_var.set(False)
        self.randomize_var.set(True)
        self.audio_process_var.set(False)
        
        # 重置功能参数到默认值
        self.mask_invert_value.set(0.03)
        self.frame_sampling_value.set(5)
        self.frame_sampling_random_var.set(True)
        
        # 重置进度条
        self.progress['value'] = 0
        self.progress_label.config(text="0%")
        
        # 重置状态标签
        self.status_label.config(text="请添加视频文件并选择功能", fg='#7f8c8d')
        
        # 清空日志
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        
        self.log_message("界面已清空并重置到初始状态")

def main():
    try:
        root = tk.Tk()
        app = VideoDedupTool(root)
        root.mainloop()
    except Exception as e:
        print(f"程序启动失败: {e}")
        input("按回车键退出...")

if __name__ == "__main__":
    main()