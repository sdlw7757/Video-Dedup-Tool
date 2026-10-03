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
GITHUB_LOGO_PNG_B64 = "iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAGz0lEQVRo3s1aaahUZRg+58zZZjmznXstzEjB8qLoGBW55AWlG4ihiGU/hBJuFtmiPywpkkj9Ixi0GCItSppLGqVF0K2MyK0Fy4uGW9hGoXf29ezTc27Xy+gs35m5M3M7MJ5x5nzf9zzv8nzv+82li8Ui1azLNE1ZN4wu3CcUqaKMj3xDX2Vpio65XK5LHMuexT3WrDXZkQwGeU5V1fsKqrLQMIy5lmVNxMc0aRjDMBdZlj3sFsRPBEHoo2labxQD3YgHAPamfKHwtKIqvRjfMRIjAHxUFMS3PW73GyD1d0sJmJYVyuay6xRFWYn/ClRzL0UUxa0+r2+Di2ESTSeQL+QfzOZyW/D8GKqFFzxyBSSehEcONIUA4lpMZzJbVE3tpdp48Tz/TkDyP4V8URomgJCRk8nkp4ZpzKBG4WJd7PGA378QuRGtmwAS9YZEKnkYHphMjeIFD/wSCgTngcTlit9XCZtAMp36fLTBD2GZDCx9uPsdEYBHGAzYg80oQv1PLmCZhmjYa2MjEoBMvqDr+vxKE4mCsM3r9T7LcZytELkmYszZc9pzC7zwVpWQng8VfL5mDmiaFgHTH/CWq+RNORSWEYvJIdf6c/nc4wVFWYs55AYlM+YWxU0ej3cbtD99da+JxqIDeOuqMEQPBYN38Rx/qoyAfY8nEsegODOrLNY/pqMzUmlzS2fSm0zDmM7x/HEox2nUOhdpmoq5GJf63zOmgOllhMJEzD9V17S7WZY7JUnS2kqb1kAsehoGmlIJB54/Jofl2cBzbS0ESy6pBn7wQZa9VGXCBFTisdoF1/AyXztSHpq5YFGVCcBgs2ys2Og+HM4B2/r5fG5dTXdTtNlO8alZFeRzL16NnEECqqZ1g1lN1YF3xrcLfbFoTSDUZNM1XeseJoDirNeBHkcwUGq5ZEIc8JpKrs0KywcJABgLNgtJAyCh7yLeM60mYKsRpHQH6TlI/WKEEctouj4Tb4IEuftL8kmr2xVCUKfV9pqEZioIw89gDEOfRZrQ4/FsRk2SbxcBeCEHlXmF9Jym6bNtD9xOyimRF3a3u3xwi+737bUJwjKdsUyzi2CNc9gDBtpNAJvhAMLoYk1hMa1JDDJ+TO34Z34frSIOO/l5ggdutGU0RCq0RrEQVQjfDxIgNefSKBLwkupBm4BWM4Op1jbxNWO8aN1MPGPCP3FCM3ErNjum3eCh8y6sSypfLkPeGZLCeJAs09pNADtthBRCKN3/YSBXZ4mZpKiL2k1A1VRiecO4mPMMx3I/EQmoyqNwqdC22LcsETX/CgfHLj8z6EWPOYjHceiV17SLAFrVNVhzLPnwiztKI0nZaDwWxYAAqfQISP4Foih+2VLhV9V7U+nUZ1X68tICM9Upd3TaSWzAC4cczM2ns5mD+UL+gVaBx9xL0V8fIoG3L2D+2D6WH5RHtyBur5RHeP1aWlDBS55MNrs/nkzsRSnb1SzgmqZNwZz7Mfc+rOF2WOztGD6VsF8Io36rpBPCAy/5JWl9Lp9fjAWWAPCy61MDCnYEzcdBgeeP4n0/Xo5KbsMw0HWZEcw7C+3sIoTxDIr8w0hpgdkvh+WIfTIxfKyCFm1pJpvZVyoGiPfNktf3MlRoLmrvHkjbqlriAcJzQLymKBSUwrx0JvMFVeVY01HD45MeQr/wwTUnc25R3A9Z+r5UZtErP4fFXgWor0BmDyx8oroi8LtI4Ic8e5jn+Ib7C1j/Oxtr2dEi3FGUfL4nbA9ft6GsgAfmwVscLNyLpP+zSs+803mzIu5qEL/hl/wrbaxlBIaseBIW2limy7ncesT6EV03Im63exXeb8Ekf9gRAUJnAP41fHbCKQo0SCcb7NI22hiv2Y3L48u3AQv0XXfUcQdid4HX49nj83g/QtqbHWG5C8C3hgLB2fheA5FsHViS9YJHePcBW5lxK/7AATUKxhLxI6Xnk7B4POD33w9LHy8hxiMmtbrjwDA4zO94HNY+A9W5B2uVEa+oBLBmEpbtwf1cyR4QTqZS3+K1HcndAxBji5bF4j4OeTKnVZsbMJwNB0M9lcBX9UCJpTqT2Nah03eSFsK2TmMxpx7g4QHVQWP/Y9AfWICQvlKVICHZBsC+G4nznoMK0tVMy0Nqd4awdi3wRAJDLiwgnB5BAi2zf5CoZbA68NE14j1mrxUKBh9G2BSI+Jyu6HF7dsuh8CQk8ZtV+mh2hEbX7Lnh8Un2Wo4t0eDfStySK+SfUVV1uZ3csFoaOSDjbjgZD/VyxeKxBMZKGJMQBGG71+15HeFS9xkUPZI/t0HcC5qud8PVv6G8vVCnEW4zTHM8z3HfIEzVRjH8C1sOVqWZ27j3AAAAAElFTkSuQmCC"


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
        # 窗口默认最大化（全屏）打开；仍可通过拖动标题栏或按钮手动调整大小
        self.root.state('zoomed')
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
        self.mask_invert_value = tk.DoubleVar(value=0.03)  # 蒙版透明度，默认0.03（0.03 = 3% 透明）
        self.frame_sampling_var = tk.BooleanVar()  # 视频抽针
        self.frame_sampling_value = tk.IntVar(value=5)  # 抽针间隔，默认5帧
        self.frame_sampling_random_var = tk.BooleanVar(value=True)  # 随机抽针间隔
        self.crop_var = tk.BooleanVar()  # 随机裁剪缩放（裁剪 1%-3% 后缩放回原分辨率）
        
        # 高级选项
        self.randomize_var = tk.BooleanVar(value=True)  # 参数随机化（每个文件独立取值）
        self.audio_process_var = tk.BooleanVar()  # 音频基础处理（音量微调 + 重采样，不变调）
        self.rounds_value = tk.IntVar(value=1)  # 处理轮数（多轮叠加，逐轮独立随机化）
        
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
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=6)
        
        # 标题区域
        title_frame = tk.Frame(main_frame, bg='#2c3e50', relief=tk.RAISED, bd=0)
        title_frame.pack(fill=tk.X, pady=(0, 12))
        
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
        file_frame.pack(fill=tk.X, pady=(0, 6))
        
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
        list_container.pack(fill=tk.X, padx=10, pady=(0, 6))
        
        self.file_tree = ttk.Treeview(list_container, columns=("name", "status"), show="headings",
                                      height=3, selectmode="extended")
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
            ("时间跳跃", "轻微调整帧率节奏（不插值重建，画质几乎无损）", self.time_jump_var),
            ("修改MD5值", "通过重新编码和添加元数据修改文件MD5值", self.md5_change_var),
            ("蒙版倒置", "降低画面透明度并叠加到黑底 (0-0.5)", self.mask_invert_var),
            ("视频抽针", "每隔指定帧数抽掉 1 帧并自动补帧（时长、帧率保持不变，播放流畅）", self.frame_sampling_var),
            ("随机裁剪", "随机裁剪 0.5%-1.5% 后 lanczos 缩放回原分辨率（分辨率不变，画质影响小）", self.crop_var)
        ]
        
        for name, desc, var in funcs:
            func_item_frame = tk.Frame(func_container, bg='#f0f0f0')
            func_item_frame.pack(fill=tk.X, pady=2)
            
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
                tk.Label(mask_frame, text="透明度:", font=('Arial', 9), bg='#f0f0f0').pack(side=tk.LEFT)
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
            adv_container, text="音频基础处理：音量微调 + 重采样 + 轻微频谱/相位扰动（不改变音调与速度）",
            variable=self.audio_process_var, bg='#f0f0f0', activebackground='#f0f0f0', anchor=tk.W,
            font=('Arial', 9), justify=tk.LEFT
        ).pack(fill=tk.X)
        
        # 处理轮数（多轮叠加，逐轮独立随机化，累计改变幅度）
        rounds_frame = tk.Frame(adv_container, bg='#f0f0f0')
        rounds_frame.pack(fill=tk.X, pady=(4, 0))
        tk.Label(rounds_frame, text="处理轮数：", font=('Arial', 9), bg='#f0f0f0', anchor=tk.W).pack(side=tk.LEFT)
        tk.Spinbox(rounds_frame, from_=1, to=3, textvariable=self.rounds_value, width=4,
                   font=('Arial', 9)).pack(side=tk.LEFT)
        tk.Label(rounds_frame, text="（1-3，轮数越多改动越大、耗时越长）", font=('Arial', 9),
                 fg='#7f8c8d', bg='#f0f0f0', anchor=tk.W).pack(side=tk.LEFT, padx=(6, 0))
        
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
        
        self.log_text = tk.Text(log_container, height=2, font=('Consolas', 9), bg='#ffffff', fg='#2c3e50')
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
让视频帧率节奏在源帧率 ±0.5% 内轻微波动（约每 2-3 秒少/多 1 帧），帧内容全部原样保留、不做插值重建，画质几乎无损，肉眼基本察觉不到变化。

RGB偏移：
让视频 RGB 颜色通道按设置偏移，达到换色目的。通过对RGB通道进行轻微的空间偏移来产生视觉差异。

水平镜像：
让视频进行左右镜像翻转，改变视频的视觉内容但保持内容完整性。

修改MD5值：
通过重新编码视频并添加随机元数据，规避平台重复检测。确保输出文件的MD5值与原文件不同。

蒙版倒置：
降低画面透明度并叠加到黑底（透明度值 0-0.5，0.03 表示 3% 透明），产生整体色调偏移。

随机裁剪：
随机裁掉画面 0.5%-1.5% 的边框后用 lanczos 缩放回原分辨率（分辨率保持不变），轻微改变构图与像素分布（对感知哈希影响较大）。比例收窄且用高质量缩放，避免画面被明显"推近"或放大变糊。

视频抽针：
每隔指定帧数抽掉 1 帧（如间隔 5 即每 5 帧抽掉 1 帧），随即用 minterpolate 插值把被抽掉的帧补回。输出与原片时长、帧率完全一致，播放流畅不卡顿，画面仅轻微柔化（快速运动时略有重影）。间隔越小变化越明显（如 2-3 变化较强、5 以上较轻微）。

参数随机化：
为每个文件独立在安全区间随机取值（CRF/GOP/B帧/RGB偏移/蒙版值/裁剪比例/抽针间隔/音频参数等），避免批量输出彼此相似。

处理轮数：
对同一文件串联执行多轮处理（1-3 轮），每轮重新独立随机化参数，累计放大与原片的差异。

音频基础处理：
音量微调（volume）、重采样（aresample），并加入时变增益、轻微频谱整形与声道相位微移以扰动音频指纹；不改变音调与播放速度。
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
                    self.crop_var.get(), self.audio_process_var.get()]):
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
            rounds_value = int(self.rounds_value.get())
        except (tk.TclError, ValueError):
            messagebox.showerror("错误", "“蒙版透明度”“抽针间隔”“处理轮数”必须是有效数字")
            return
        if self.mask_invert_var.get() and not (0 < mask_value <= 0.5):
            messagebox.showerror("错误", "蒙版透明度需大于 0 且不超过 0.5")
            return
        if self.frame_sampling_var.get() and sampling_value < 2:
            messagebox.showerror("错误", "抽针间隔必须是大于等于 2 的整数")
            return
        if not (1 <= rounds_value <= 3):
            messagebox.showerror("错误", "处理轮数必须是 1 到 3 之间的整数")
            return
        self.mask_invert_value.set(mask_value)
        self.frame_sampling_value.set(sampling_value)
        self.rounds_value.set(rounds_value)

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

    def _build_params(self, source_fps=0.0, width=0, height=0, channels=0):
        """生成单个文件的处理参数（随机化开启时每个文件独立取值）"""
        r = self.randomize_var.get()

        def pick(lo, hi, fixed):
            return random.uniform(lo, hi) if r else fixed

        # RGB 通道偏移量
        if r:
            rgb_offsets = tuple(random.choice([-3, -2, -1, 1, 2, 3]) for _ in range(6))
        else:
            rgb_offsets = (2, -1, 1, 1, -2, 2)

        # 蒙版透明度：用户设定值附近轻微浮动，控制在 (0, 0.5]
        mask_base = min(0.5, max(0.0001, float(self.mask_invert_value.get())))
        if r:
            mask = round(min(0.5, random.uniform(mask_base * 0.6, mask_base * 1.4)), 4)
        else:
            mask = round(mask_base, 4)

        # 抽针间隔：无论是否随机都必须 >= 2，否则 mod(n, 0) 会产出 0 帧的空文件
        sampling_base = max(2, int(self.frame_sampling_value.get()))
        if r:
            sampling = random.randint(sampling_base, sampling_base + 3)
        else:
            sampling = sampling_base

        # 时间跳跃以源帧率为基准（避免把 60fps 源砍成 30fps），随机化时加 ±0.5% 微抖动
        # （抖动越小，minterpolate 重建的帧越少，画面越清晰）
        fps_base = source_fps if source_fps > 0 else 30.0
        fps = round(fps_base * (random.uniform(0.995, 1.005) if r else 1.0), 3)

        # 随机裁剪：裁掉 0.5%-1.5% 边框后用 lanczos 缩放回原分辨率（宽高均取偶数以适配 yuv420p）。
        # 比例收窄 + lanczos 缩放，最大限度避免"画面被推近/放大变糊"的观感，分辨率保持不变。
        crop = None
        if self.crop_var.get() and width > 2 and height > 2:
            ratio = random.uniform(0.005, 0.015) if r else 0.01
            crop_w = max(2, int(width * (1 - ratio)) // 2 * 2)
            crop_h = max(2, int(height * (1 - ratio)) // 2 * 2)
            max_x = max(0, width - crop_w)
            max_y = max(0, height - crop_h)
            crop_x = (random.randint(0, max_x) if (r and max_x > 0) else max_x // 2) // 2 * 2
            crop_y = (random.randint(0, max_y) if (r and max_y > 0) else max_y // 2) // 2 * 2
            crop = (crop_w, crop_h, crop_x, crop_y, width // 2 * 2, height // 2 * 2)

        return {
            "crf": int(pick(18, 22, 20)),
            "gop": int(pick(48, 72, 60)),
            "bf": int(pick(1, 3, 2)),
            "fps": fps,
            "rgb_offsets": rgb_offsets,
            "mask": mask,
            "crop": crop,
            "sampling": sampling,
            "audio_vol": round(pick(0.98, 1.02, 1.0), 4),
            "audio_sr": random.choice([44100, 48000]) if r else 48000,
            # 音频指纹扰动参数（均不改变音调与速度）
            "gain_depth": round(pick(0.008, 0.018, 0.0), 4),
            "gain_period": round(pick(5.0, 15.0, 7.0), 2),
            "gain_jitter": round(pick(0.004, 0.012, 0.0), 4),
            "eq_freq": int(pick(400, 6000, 1200)),
            "eq_gain": round(pick(0.4, 1.0, 0.0), 3),
            "phase_ms": round(pick(1.0, 4.0, 0.0), 2),
            "width": width,
            "height": height,
            "channels": channels,
        }

    def _file_md5(self, file_path):
        """计算文件 MD5"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def _probe_media(self, video_path):
        """探测媒体信息：是否含音轨、音轨声道数、源视频帧率、分辨率与总时长"""
        info = {"has_audio": False, "fps": 0.0, "width": 0, "height": 0,
                "channels": 0, "duration": 0.0}
        try:
            cmd = [self.ffprobe_path, '-v', 'error', '-show_streams', '-show_format',
                   '-of', 'json', video_path]
            result = subprocess.run(cmd, capture_output=True, text=True,
                                    encoding='utf-8', errors='replace')
            if result.returncode != 0 or not result.stdout.strip():
                return info

            data = json.loads(result.stdout)
            for stream in data.get("streams", []):
                codec_type = stream.get("codec_type")
                if codec_type == "audio":
                    info["has_audio"] = True
                    if not info["channels"]:
                        try:
                            info["channels"] = int(stream.get("channels") or 0)
                        except (TypeError, ValueError):
                            info["channels"] = 0
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
                    try:
                        info["width"] = int(stream.get("width") or 0)
                        info["height"] = int(stream.get("height") or 0)
                    except (TypeError, ValueError):
                        info["width"] = info["height"] = 0
            # 总时长在 format 段，供进度条直接使用，避免再跑一次 ffprobe
            fmt = data.get("format") or {}
            try:
                info["duration"] = float(fmt.get("duration") or 0)
            except (TypeError, ValueError):
                info["duration"] = 0.0
        except Exception as e:
            print(f"探测媒体信息失败: {e}")
        return info
            
    # 支持内嵌缩略图的容器
    SUPPORTED_THUMB_CONTAINERS = ('.mp4', '.mov', '.m4v', '.mkv')

    def _temp_output_path(self, input_path, index):
        """生成中间轮次的临时输出路径（与源文件同目录，复用同一容器）"""
        p = Path(input_path)
        stamp = self._generate_random_string(8)
        return str(p.parent / f"{p.stem}_tmp{index}_{stamp}{p.suffix}")

    def _process_single(self, input_path, output_path):
        """处理单个视频文件（工作线程，支持多轮串联处理）"""
        rounds = max(1, min(3, int(self.rounds_value.get())))
        suffix = Path(output_path).suffix.lower()

        # 缩略图只从原始文件提取一次，并在最后一轮嵌入
        need_thumb = (
            suffix in self.SUPPORTED_THUMB_CONTAINERS
            and any([self.mirror_var.get(), self.rgb_shift_var.get(),
                     self.time_jump_var.get(), self.md5_change_var.get(),
                     self.mask_invert_var.get(), self.frame_sampling_var.get(),
                     self.crop_var.get(), self.audio_process_var.get()])
        )
        thumb_path = self._extract_thumbnail(input_path) if need_thumb else None
        if need_thumb and thumb_path is None:
            self.log_message("提取缩略图失败，本次不嵌入缩略图")

        temp_files = []
        self.log_message(f"输入文件: {input_path}")
        self.log_message(f"输出文件: {output_path}（共 {rounds} 轮）")

        try:
            current = input_path
            for rnd in range(1, rounds + 1):
                if self.cancel_requested:
                    raise Exception("任务已被取消")
                is_last = (rnd == rounds)
                media = self._probe_media(current)
                params = self._build_params(media["fps"], media["width"],
                                            media["height"], media["channels"])
                audio_desc = f"有({media['channels']}声道)" if media["has_audio"] else "无"
                self.log_message(
                    f"--- 第 {rnd}/{rounds} 轮 | {media['width']}x{media['height']} "
                    f"@ {media['fps']:.3f}fps | 音轨: {audio_desc} ---"
                )
                target = output_path if is_last else self._temp_output_path(input_path, rnd)
                if not is_last:
                    temp_files.append(target)
                self._run_single_ffmpeg(current, target, params, media["has_audio"],
                                        thumb_path if is_last else None,
                                        apply_mirror=(rnd == 1),
                                        duration=media.get("duration", 0.0))
                if not os.path.exists(target) or os.path.getsize(target) == 0:
                    raise Exception(f"第 {rnd} 轮输出文件未生成或为空（参数可能不合法）")
                current = target
        finally:
            # 清理中间轮次临时文件与缩略图
            for tmp in temp_files:
                if os.path.exists(tmp):
                    try:
                        os.remove(tmp)
                    except OSError:
                        pass
            if thumb_path and os.path.exists(thumb_path):
                try:
                    os.remove(thumb_path)
                except OSError:
                    pass

        # MD5 对比
        try:
            src_md5 = self._file_md5(input_path)
            out_md5 = self._file_md5(output_path)
            self.log_message(f"原始MD5: {src_md5}")
            self.log_message(f"新文件MD5: {out_md5}")
            self.log_message("MD5 已变化" if src_md5 != out_md5 else "警告: MD5 未发生变化")
        except Exception as e:
            self.log_message(f"计算MD5失败: {e}")

        self.log_message(f"视频处理成功完成（共 {rounds} 轮）")

    def _build_audio_filter(self, params):
        """构建音频滤镜链：音量微调 + 指纹扰动 + 重采样，全程不改变音调与播放速度"""
        r = self.randomize_var.get()
        vol = params["audio_vol"]
        parts = []
        if r and params["gain_depth"] > 0:
            # 时变增益：慢周期波动 + 逐帧随机抖动，改变波形包络但不改变音调。
            # if(isnan(t),0,t) 防止部分 ffmpeg 版本首帧 t 为 NaN 导致音量被置 0
            parts.append(
                f"volume='{vol}+{params['gain_depth']}*sin(2*PI*if(isnan(t),0,t)/{params['gain_period']})"
                f"+{params['gain_jitter']}*(random(0)-0.5)':eval=frame"
            )
        else:
            parts.append(f"volume={vol}")
        if r and params["eq_gain"] > 0:
            # 轻微频谱整形：改变频谱包络以扰动音频指纹
            parts.append(f"equalizer=f={params['eq_freq']}:t=q:w=1:g={params['eq_gain']}")
        if r and params["phase_ms"] > 0 and params["channels"] >= 2:
            # 立体声相位微移：仅延迟第 0 声道，破坏声道间相位关系
            parts.append(f"adelay=delays={params['phase_ms']}ms:all=0")
        parts.append(f"aresample={params['audio_sr']}")
        return ",".join(parts)

    def _run_single_ffmpeg(self, input_path, output_path, params, has_audio, thumb_path,
                           apply_mirror=True, duration=0.0):
        """组装并执行单次 ffmpeg 命令（含可选缩略图嵌入）"""
        cmd = [self.ffmpeg_path, '-y', '-i', input_path]
        if thumb_path:
            cmd.extend(['-i', thumb_path])

        # 视频滤镜链
        filters = []

        # 随机裁剪缩放放在链路最前，让后续滤镜在最终分辨率上工作；
        # 用 lanczos 缩放回原分辨率，避免放大产生明显模糊
        if params["crop"]:
            cw, ch, cx, cy, sw, sh = params["crop"]
            filters.append(f"crop={cw}:{ch}:{cx}:{cy}")
            filters.append(f"scale={sw}:{sh}:flags=lanczos")
            self.log_message(f"应用随机裁剪缩放 (裁剪 {cw}x{ch} @ {cx},{cy} → lanczos缩放回 {sw}x{sh})")

        # 水平镜像是自逆变换（翻转两次会还原），多轮处理时只在首轮应用
        if self.mirror_var.get() and apply_mirror:
            filters.append("hflip")
            self.log_message("应用水平镜像效果")

        if self.rgb_shift_var.get():
            rh, gh, bh, rv, gv, bv = params["rgb_offsets"]
            filters.append(f"rgbashift=rh={rh}:gh={gh}:bh={bh}:rv={rv}:gv={gv}:bv={bv}")
            self.log_message(f"应用RGB偏移效果 {params['rgb_offsets']}")

        if self.time_jump_var.get():
            # 时间跳跃：用 fps 滤镜把帧率节奏微调到源帧率 ±0.5%（约每 2-3 秒少/多 1 帧），
            # 帧内容全部原样保留、不重建任何帧，画质几乎无损；
            # 早期版本用 minterpolate 运动补偿插值，会重建每一帧导致画面发软
            filters.append(f"fps={params['fps']}")
            self.log_message(
                f"应用时间跳跃效果 (轻微变速波动 → {params['fps']}fps，不插值，保持画质)"
            )

        # 视频抽针：每隔指定帧数抽掉 1 帧（保留其余帧），再通过 minterpolate 把
        # 被抽掉的帧补回（插值），输出与原片时长、帧率完全一致且播放流畅，
        # 不会出现帧间隔忽大忽小的卡顿，也不会把视频变成加速短片。
        # 抽帧位置必须是每个文件一次性取定的常量（不能在 select 表达式里用
        # random(0) 逐帧随机，否则抽帧位置完全随机，画面一卡一卡）。
        if self.frame_sampling_var.get():
            interval = params["sampling"]
            if self.frame_sampling_random_var.get():
                interval += random.randint(0, 5)  # 随机间隔：每个文件独立取一次
            filters.append(f"select='not(eq(mod(n,{interval}),{interval - 1}))'")
            filters.append(f"minterpolate=fps={params['fps']}:mi_mode=blend")
            self.log_message(
                f"应用视频抽针效果 (间隔: {interval}帧，抽帧后补帧回 {params['fps']}fps，"
                f"时长保持不变)"
            )

        # 蒙版倒置：alpha 通道在 yuv420p 输出中会被丢弃，因此改为在 RGB 平面按透明度
        # 缩放颜色（等价于把画面以该透明度叠加到黑底），放在链路末尾避免多次色彩空间往返
        if self.mask_invert_var.get():
            alpha = round(1.0 - params["mask"], 4)
            filters.append("format=gbrp")
            filters.append(f"colorchannelmixer=rr={alpha}:gg={alpha}:bb={alpha}")
            filters.append("format=yuv420p")
            self.log_message(f"应用蒙版倒置效果 (透明度 {params['mask']} → 画面保留 {alpha})")

        # yuv420p 需要偶数宽高：若源分辨率为奇数且未开启裁剪（裁剪已自动规整偶数），
        # 先在链路最前把画面规整为偶数，否则 libx264 会因 "width not divisible by 2" 直接失败
        if (not params.get("crop")
                and (params.get("width", 0) % 2 or params.get("height", 0) % 2)
                and (self.md5_change_var.get() or bool(filters))):
            filters.insert(0, "scale=trunc(iw/2)*2:trunc(ih/2)*2")
            self.log_message("源分辨率为奇数，已自动规整为偶数宽高以适配 yuv420p")

        if filters:
            # 有缩略图输入时，滤镜只能作用于第 0 个视频流，否则会应用到静态图片
            cmd.extend(['-filter:v:0' if thumb_path else '-vf', ','.join(filters)])

        # 音频基础处理：音量微调 + 重采样 + 指纹扰动，均不改变音调与速度
        # （抽针为抽帧+补帧，视频时长不变，音频无需变速）
        audio_on = self.audio_process_var.get() and has_audio
        if audio_on:
            af = self._build_audio_filter(params)
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
                    f'-preset:v{vs}', 'veryfast',
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

        # 抽针后 minterpolate 已输出固定帧率，显式 CFR 确保封装为恒定帧率
        if self.frame_sampling_var.get():
            cmd.extend(['-fps_mode', 'cfr'])

        # mp4/mov/m4v 开启 faststart：把 moov 原子移到文件头，便于平台快速起播
        if Path(output_path).suffix.lower() in ('.mp4', '.mov', '.m4v'):
            cmd.extend(['-movflags', '+faststart'])

        cmd.append(output_path)
        self.log_message(f"执行命令: {' '.join(cmd)}")

        self._run_ffmpeg_with_progress(cmd, input_path, duration)

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
        
    def _run_ffmpeg_with_progress(self, cmd, input_path, duration=0.0):
        """运行 FFmpeg 并监控进度（只记录错误信息，避免进度行刷屏）"""
        # 优先使用探测阶段已取得的时长；拿不到时再单独调用 ffprobe 兜底
        if duration <= 0:
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
        self.crop_var.set(False)
        self.randomize_var.set(True)
        self.audio_process_var.set(False)
        
        # 重置功能参数到默认值
        self.mask_invert_value.set(0.03)
        self.frame_sampling_value.set(5)
        self.frame_sampling_random_var.set(True)
        self.rounds_value.set(1)
        
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