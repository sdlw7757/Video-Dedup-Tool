import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import random
import string
from pathlib import Path
import threading
import re
import sys
import hashlib

class VideoDedupTool:
    def __init__(self, root):
        self.root = root
        self.root.title("视频去重工具 - Video Deduplication Tool")
        # 将窗口大小调整为现在的一倍
        self.root.geometry("1700x1500")
        self.root.resizable(True, True)  # 允许调整窗口大小
        self.root.configure(bg='#f0f0f0')
        
        # 取消默认全屏，让用户可以控制窗口
        # self.root.attributes('-fullscreen', True)
        
        # 设置窗口图标（如果有的话）
        try:
            self.root.iconbitmap(default='icon.ico')
        except:
            pass
        
        # 视频文件路径
        self.video_path = tk.StringVar()
        self.output_path = tk.StringVar()
        
        # MD5值变量
        self.original_md5 = tk.StringVar(value="未选择文件")
        self.new_md5 = tk.StringVar(value="未处理")
        
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
        
        # 创建界面
        self.create_modern_widgets()
        
        # 获取项目根目录
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        
        # FFmpeg路径 (使用项目集成的FFmpeg)
        self.ffmpeg_path = os.path.join(self.project_root, "ffmpeg-8.0", "bin", "ffmpeg.exe")
        self.ffprobe_path = os.path.join(self.project_root, "ffmpeg-8.0", "bin", "ffprobe.exe")
        
        # Python路径 (使用项目集成的Python)
        self.python_path = os.path.join(self.project_root, "python", "python.exe")
        
        self.log_message(f"项目根目录: {self.project_root}")
        self.log_message(f"FFmpeg路径: {self.ffmpeg_path}")
        self.log_message(f"FFprobe路径: {self.ffprobe_path}")
        self.log_message(f"Python路径: {self.python_path}")
        
        # 检查必要组件
        self.check_dependencies()
        
    def check_dependencies(self):
        """检查必要组件是否存在"""
        missing_components = []
        
        if not os.path.exists(self.ffmpeg_path):
            missing_components.append("FFmpeg (ffmpeg.exe)")
            
        if not os.path.exists(self.ffprobe_path):
            missing_components.append("FFprobe (ffprobe.exe)")
            
        if not os.path.exists(self.python_path):
            missing_components.append("Python (python.exe)")
            
        if missing_components:
            missing_list = "\n".join(missing_components)
            error_msg = f"缺少以下必要组件:\n{missing_list}\n\n请确保所有文件都在正确的位置。"
            self.log_message(error_msg)
            messagebox.showerror("错误", error_msg)
            
    def create_modern_widgets(self):
        """创建现代化界面组件"""
        # 主框架
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
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
        
        # 文件选择区域
        file_frame = tk.LabelFrame(left_frame, text="文件选择", font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 输入文件选择
        input_frame = tk.Frame(file_frame, bg='#f0f0f0')
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(input_frame, text="输入文件:", font=('Arial', 10), bg='#f0f0f0').pack(anchor=tk.W)
        input_file_frame = tk.Frame(input_frame, bg='#f0f0f0')
        input_file_frame.pack(fill=tk.X, pady=(5, 0))
        
        tk.Entry(input_file_frame, textvariable=self.video_path, font=('Arial', 9), state='readonly').pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(input_file_frame, text="浏览", command=self.browse_file, bg='#3498db', fg='white', font=('Arial', 9, 'bold'), relief=tk.FLAT, padx=10).pack(side=tk.RIGHT, padx=(5, 0))
        
        # MD5值显示
        md5_frame = tk.Frame(file_frame, bg='#f0f0f0')
        md5_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 原始MD5
        original_md5_frame = tk.Frame(md5_frame, bg='#f0f0f0')
        original_md5_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(original_md5_frame, text="原始MD5:", font=('Arial', 9, 'bold'), bg='#f0f0f0').pack(anchor=tk.W)
        tk.Label(original_md5_frame, textvariable=self.original_md5, font=('Arial', 8), bg='#f0f0f0', fg='#7f8c8d', wraplength=300, justify=tk.LEFT).pack(anchor=tk.W)
        
        # 新MD5
        new_md5_frame = tk.Frame(md5_frame, bg='#f0f0f0')
        new_md5_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        tk.Label(new_md5_frame, text="新MD5:", font=('Arial', 9, 'bold'), bg='#f0f0f0').pack(anchor=tk.W)
        tk.Label(new_md5_frame, textvariable=self.new_md5, font=('Arial', 8), bg='#f0f0f0', fg='#7f8c8d', wraplength=300, justify=tk.LEFT).pack(anchor=tk.W)
        
        # 输出文件选择
        output_frame = tk.Frame(file_frame, bg='#f0f0f0')
        output_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(output_frame, text="输出路径:", font=('Arial', 10), bg='#f0f0f0').pack(anchor=tk.W)
        output_file_frame = tk.Frame(output_frame, bg='#f0f0f0')
        output_file_frame.pack(fill=tk.X, pady=(5, 0))
        
        tk.Entry(output_file_frame, textvariable=self.output_path, font=('Arial', 9), state='readonly').pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(output_file_frame, text="选择", command=self.browse_output, bg='#3498db', fg='white', font=('Arial', 9, 'bold'), relief=tk.FLAT, padx=10).pack(side=tk.RIGHT, padx=(5, 0))
        
        # 功能选择区域
        func_frame = tk.LabelFrame(left_frame, text="去重功能", font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        func_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 功能选项容器
        func_container = tk.Frame(func_frame, bg='#f0f0f0')
        func_container.pack(fill=tk.X, padx=10, pady=10)
        
        # 创建功能选项
        funcs = [
            ("水平镜像", "让视频进行左右镜像翻转", self.mirror_var),
            ("RGB偏移", "让视频RGB颜色通道按设置偏移", self.rgb_shift_var),
            ("时间跳跃", "让视频中的帧进行周期性的变速波动", self.time_jump_var),
            ("修改MD5值", "通过重新编码和添加元数据修改文件MD5值", self.md5_change_var),
            ("蒙版倒置", "倒置视频透明度 (0-1)", self.mask_invert_var),
            ("视频抽针", "每隔指定帧数抽取一帧", self.frame_sampling_var)
        ]
        
        for i, (name, desc, var) in enumerate(funcs):
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
        
        # 处理按钮区域
        button_frame = tk.Frame(left_frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 创建按钮容器以水平排列按钮
        buttons_container = tk.Frame(button_frame, bg='#f0f0f0')
        buttons_container.pack(pady=10)
        
        self.process_btn = tk.Button(
            buttons_container, 
            text="开始处理", 
            command=self.start_processing,
            bg='#27ae60', 
            fg='white', 
            font=('Arial', 12, 'bold'), 
            relief=tk.FLAT, 
            padx=20, 
            pady=10,
            cursor='hand2'
        )
        self.process_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 添加清空按钮
        self.clear_btn = tk.Button(
            buttons_container, 
            text="清空", 
            command=self.clear_all,
            bg='#e74c3c', 
            fg='white', 
            font=('Arial', 12, 'bold'), 
            relief=tk.FLAT, 
            padx=20, 
            pady=10,
            cursor='hand2'
        )
        self.clear_btn.pack(side=tk.LEFT)
        
        # 进度区域
        progress_frame = tk.Frame(left_frame, bg='#f0f0f0')
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 进度条和百分比
        progress_container = tk.Frame(progress_frame, bg='#f0f0f0')
        progress_container.pack(fill=tk.X, pady=5)
        
        self.progress = ttk.Progressbar(progress_container, mode='determinate')
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.progress_label = tk.Label(progress_container, text="0%", font=('Arial', 10, 'bold'), width=5, bg='#f0f0f0')
        self.progress_label.pack(side=tk.RIGHT, padx=(10, 0))
        
        # 状态标签
        self.status_label = tk.Label(
            left_frame, 
            text="请选择视频文件并选择功能", 
            font=('Arial', 10), 
            fg='#7f8c8d', 
            bg='#f0f0f0'
        )
        self.status_label.pack(pady=(0, 15))
        
        # 日志区域
        log_frame = tk.LabelFrame(left_frame, text="处理日志", font=('Arial', 12, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        log_container = tk.Frame(log_frame, bg='#f0f0f0')
        log_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.log_text = tk.Text(log_container, height=8, font=('Consolas', 9), bg='#ffffff', fg='#2c3e50')
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
        info_content = """时间跳跃：
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
通过抽取特定帧来创建视频变化，减少视频内容。
"""
        info_text.insert(tk.END, info_content)
        info_text.config(state='disabled')
        
    def browse_file(self):
        """浏览选择视频文件"""
        file_path = filedialog.askopenfilename(
            title="选择视频文件",
            filetypes=[
                ("视频文件", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm"),
                ("所有文件", "*.*")
            ]
        )
        
        if file_path:
            self.set_video_file(file_path)
            
    def set_video_file(self, file_path):
        """设置视频文件路径"""
        self.video_path.set(file_path)
        self.status_label.config(text=f"已选择文件: {os.path.basename(file_path)}", fg='#27ae60')
        self.log_message(f"已选择文件: {file_path}")
        
        # 计算并显示原始MD5值
        self.calculate_original_md5(file_path)
        
        # 默认输出路径为原文件目录
        if not self.output_path.get():
            input_path = Path(file_path)
            default_output = input_path.parent / f"{input_path.stem}_dedup{input_path.suffix}"
            self.output_path.set(str(default_output))
            
    def calculate_original_md5(self, file_path):
        """计算原始文件的MD5值"""
        def calc_md5():
            try:
                self.original_md5.set("计算中...")
                hash_md5 = hashlib.md5()
                with open(file_path, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)
                md5_value = hash_md5.hexdigest()
                self.original_md5.set(md5_value)
                self.log_message(f"原始文件MD5: {md5_value}")
            except Exception as e:
                self.original_md5.set("计算失败")
                self.log_message(f"计算原始MD5失败: {e}")
                
        # 在新线程中计算MD5，避免阻塞UI
        threading.Thread(target=calc_md5, daemon=True).start()
        
    def update_new_md5(self, file_path):
        """更新新文件的MD5值"""
        def calc_md5():
            try:
                self.new_md5.set("计算中...")
                hash_md5 = hashlib.md5()
                with open(file_path, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_md5.update(chunk)
                md5_value = hash_md5.hexdigest()
                self.new_md5.set(md5_value)
                self.log_message(f"新文件MD5: {md5_value}")
            except Exception as e:
                self.new_md5.set("计算失败")
                self.log_message(f"计算新MD5失败: {e}")
                
        # 在新线程中计算MD5，避免阻塞UI
        threading.Thread(target=calc_md5, daemon=True).start()
        
    def browse_output(self):
        """浏览选择输出路径"""
        if not self.video_path.get():
            messagebox.showerror("错误", "请先选择视频文件")
            return
            
        # 获取原文件的扩展名
        input_path = Path(self.video_path.get())
        file_extension = input_path.suffix
        
        output_path = filedialog.asksaveasfilename(
            title="选择输出文件保存位置",
            defaultextension=file_extension,
            filetypes=[(f"{file_extension} 文件", f"*{file_extension}"), ("所有文件", "*.*")]
        )
        
        if output_path:
            self.output_path.set(output_path)
            self.log_message(f"输出路径设置为: {output_path}")
            
    def start_processing(self):
        """开始处理视频（在新线程中）"""
        # 在新线程中处理视频，避免界面冻结
        processing_thread = threading.Thread(target=self.process_video)
        processing_thread.daemon = True
        processing_thread.start()
            
    def process_video(self):
        """处理视频"""
        if not self.video_path.get():
            self.log_message("错误: 请先选择视频文件")
            self.root.after(0, lambda: messagebox.showerror("错误", "请先选择视频文件"))
            return
            
        if not self.output_path.get():
            self.log_message("错误: 请设置输出路径")
            self.root.after(0, lambda: messagebox.showerror("错误", "请设置输出路径"))
            return
            
        # 修复条件检查，包含所有功能选项
        if not any([self.mirror_var.get(), self.rgb_shift_var.get(), 
                   self.time_jump_var.get(), self.md5_change_var.get(),
                   self.mask_invert_var.get(), self.frame_sampling_var.get()]):
            self.log_message("错误: 请至少选择一个功能")
            self.root.after(0, lambda: messagebox.showerror("错误", "请至少选择一个功能"))
            return
            
        # 检查FFmpeg是否存在
        if not os.path.exists(self.ffmpeg_path):
            self.log_message(f"错误: 未找到FFmpeg: {self.ffmpeg_path}")
            self.root.after(0, lambda: messagebox.showerror("错误", f"未找到FFmpeg: {self.ffmpeg_path}"))
            return
            
        # 检查FFprobe是否存在
        if not os.path.exists(self.ffprobe_path):
            self.log_message(f"警告: 未找到FFprobe: {self.ffprobe_path}")
            
        # 开始处理
        self.log_message("开始处理视频...")
        self.root.after(0, lambda: self.status_label.config(text="正在处理视频...", fg='#e67e22'))
        
        # 更新处理按钮状态
        self.root.after(0, lambda: self.process_btn.config(state='disabled', bg='#95a5a6', text="处理中..."))
        
        try:
            self._process_video_internal()
            self.log_message("处理完成!")
            self.root.after(0, lambda: self.status_label.config(text="处理完成!", fg='#27ae60'))
            self.root.after(0, lambda: messagebox.showinfo("成功", "视频处理完成!"))
            
            # 计算并显示新文件的MD5值
            if os.path.exists(self.output_path.get()):
                self.update_new_md5(self.output_path.get())
        except Exception as e:
            self.log_message(f"处理失败: {str(e)}")
            self.root.after(0, lambda: self.status_label.config(text="处理失败", fg='#e74c3c'))
            self.root.after(0, lambda: messagebox.showerror("错误", f"处理失败: {str(e)}"))
        finally:
            # 修复语法错误：使用函数而不是lambda表达式中的赋值
            def reset_progress():
                self.progress['value'] = 0
                self.progress_label.config(text="0%")
            self.root.after(0, reset_progress)
            
            # 恢复处理按钮状态
            self.root.after(0, lambda: self.process_btn.config(state='normal', bg='#27ae60', text="开始处理"))
            
    def _process_video_internal(self):
        """实际处理视频的内部方法"""
        input_path = self.video_path.get()
        output_path = self.output_path.get()
        
        self.log_message(f"输入文件: {input_path}")
        self.log_message(f"输出文件: {output_path}")
        
        # 构建FFmpeg命令
        cmd = [self.ffmpeg_path, '-y', '-i', input_path]
        
        # 添加视频处理滤镜
        filters = []
        
        # 水平镜像
        if self.mirror_var.get():
            filters.append("hflip")
            self.log_message("应用水平镜像效果")
            
        # RGB偏移
        if self.rgb_shift_var.get():
            # 添加轻微的RGB偏移效果
            filters.append("rgbashift=rh=2:gh=-1:bh=1:rv=1:gv=-2:bv=2")
            self.log_message("应用RGB偏移效果")
            
        # 时间跳跃 (周期性的变速波动，肉眼不可见)
        if self.time_jump_var.get():
            # 使用minterpolate滤镜创建微妙的时间波动效果
            # 这种方法会在保持视频总时长不变的情况下，创建微妙的帧速率变化
            filters.append("minterpolate=fps=30:mi_mode=blend:mc_mode=aobmc:me_mode=bidir:mb_size=16:search_param=32")
            self.log_message("应用时间跳跃效果 (周期性变速波动)")
            
        # 蒙版倒置
        if self.mask_invert_var.get():
            # 获取用户设置的倒置值
            invert_value = self.mask_invert_value.get()
            # 应用透明度倒置效果
            filters.append(f"colorchannelmixer=aa={invert_value}")
            self.log_message(f"应用蒙版倒置效果 (透明度: {invert_value})")
            
        # 视频抽针
        if self.frame_sampling_var.get():
            # 获取用户设置的抽针间隔
            sampling_interval = self.frame_sampling_value.get()
            if self.frame_sampling_random_var.get():
                # 随机抽针间隔
                filters.append(f"select='not(mod(n,{sampling_interval}+floor(random(0)*6)))'")
                self.log_message(f"应用视频抽针效果 (随机间隔: {sampling_interval}-{sampling_interval+5}帧)")
            else:
                # 固定抽针间隔
                filters.append(f"select='not(mod(n,{sampling_interval}))'")
                self.log_message(f"应用视频抽针效果 (固定间隔: {sampling_interval}帧)")
            
        # 如果有视频滤镜，添加到命令中
        if filters:
            filter_str = ','.join(filters)
            cmd.extend(['-vf', filter_str])
            
        # 修改MD5值 (通过重新编码)
        if self.md5_change_var.get() or filters:
            # 添加一些元数据来确保MD5变化
            cmd.extend([
                '-metadata', f"title=Processed_{self._generate_random_string(8)}",
                '-metadata', f"comment=Video processed with dedup tool",
                '-metadata', f"date={self._generate_random_string(10)}",
                '-c:v', 'libx264',  # 重新编码视频
                '-preset', 'ultrafast',  # 快速编码
                '-crf', '23'  # 视频质量
            ])
            self.log_message("重新编码视频并添加元数据")
        else:
            # 如果没有选择任何处理选项，直接复制流
            cmd.extend(['-c', 'copy'])
            self.log_message("直接复制视频流")
            
        # 输出文件
        cmd.append(output_path)
        
        self.log_message(f"执行命令: {' '.join(cmd)}")
        
        # 执行FFmpeg命令并监控进度
        self._run_ffmpeg_with_progress(cmd, input_path)
        
        if not os.path.exists(output_path):
            raise Exception("输出文件未生成")
            
        # 生成并嵌入缩略图（无论是否应用了RGB偏移）
        # 只要进行了视频处理就生成缩略图
        if any([self.mirror_var.get(), self.rgb_shift_var.get(), 
                self.time_jump_var.get(), self.md5_change_var.get(),
                self.mask_invert_var.get(),
                self.frame_sampling_var.get()]):
            self._add_thumbnail_to_video(output_path)
            
        self.log_message("视频处理成功完成")
        
    def _add_thumbnail_to_video(self, video_path):
        """为视频生成并嵌入缩略图"""
        self.log_message("正在为视频生成并嵌入缩略图...")
        
        # 创建临时缩略图文件
        thumbnail_path = video_path + "_thumb.jpg"
        final_output = video_path + "_final.mp4"
        
        try:
            # 提取缩略图
            thumb_cmd = [
                self.ffmpeg_path, '-y', '-ss', '00:00:01', '-i', video_path,
                '-frames:v', '1', '-an', '-vf', 'thumbnail,setsar=1', 
                '-q:v', '2', thumbnail_path
            ]
            
            self.log_message(f"提取缩略图命令: {' '.join(thumb_cmd)}")
            result = subprocess.run(thumb_cmd, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode != 0:
                self.log_message(f"提取缩略图失败: {result.stderr}")
                return
                
            if not os.path.exists(thumbnail_path):
                self.log_message("缩略图文件未生成")
                return
                
            # 将缩略图嵌入到视频中
            # 使用正确的参数来嵌入JPEG图片作为缩略图
            embed_cmd = [
                self.ffmpeg_path, '-y', '-i', video_path, '-i', thumbnail_path,
                '-c', 'copy',  # 复制视频和音频流
                '-map', '0', '-map', '1',  # 映射所有流
                '-c:v:1', 'mjpeg',  # 将第二视频流编码为MJPEG
                '-disposition:v:1', 'attached_pic',  # 设置为附加图片（缩略图）
                final_output
            ]
            
            self.log_message(f"嵌入缩略图命令: {' '.join(embed_cmd)}")
            result = subprocess.run(embed_cmd, capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode != 0:
                self.log_message(f"嵌入缩略图失败: {result.stderr}")
                # 删除临时缩略图文件
                if os.path.exists(thumbnail_path):
                    os.remove(thumbnail_path)
                return
                
            # 替换原文件
            os.replace(final_output, video_path)
            
            # 删除临时缩略图文件
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
                
            self.log_message("缩略图已成功嵌入视频")
        except Exception as e:
            self.log_message(f"处理缩略图时出错: {str(e)}")
            # 清理临时文件
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
            if os.path.exists(final_output):
                os.remove(final_output)
        
    def _run_ffmpeg_with_progress(self, cmd, input_path):
        """运行FFmpeg并监控进度"""
        # 首先获取视频时长
        duration = self._get_video_duration(input_path)
        if duration <= 0:
            # 如果无法获取时长，使用基本模式运行
            self.log_message("无法获取视频时长，使用基本模式处理")
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
            stdout, stderr = process.communicate()
            
            self.log_message(f"FFmpeg输出: {stdout}")
            if stderr:
                self.log_message(f"FFmpeg错误: {stderr}")
            
            if process.returncode != 0:
                raise Exception(f"FFmpeg处理失败: {stderr}")
            return
            
        self.log_message(f"视频时长: {duration:.2f} 秒")
        
        # 使用stderr获取实时进度
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            universal_newlines=True,
            encoding='utf-8',
            bufsize=1
        )
        
        # 实时读取stderr以获取进度
        while True:
            if process.stderr is not None:
                output = process.stderr.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    # 解析进度信息
                    time_match = re.search(r"time=([0-9:.]+)", output)
                    if time_match:
                        time_str = time_match.group(1)
                        current_time = self._time_str_to_seconds(time_str)
                        if current_time >= 0:
                            progress_percent = min(100, int((current_time / duration) * 100))
                            self.root.after(0, lambda p=progress_percent: self._update_progress(p))
                            
                    self.log_message(output.strip())
            else:
                # 如果stderr为None，等待进程结束
                process.wait()
                break
        
        # 等待进程结束
        rc = process.poll()
        if rc != 0:
            # 读取剩余输出
            stdout, stderr = process.communicate()
            if stderr:
                self.log_message(f"FFmpeg错误: {stderr}")
            raise Exception(f"FFmpeg处理失败，返回码: {rc}")
            
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
            
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
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
        
    def _generate_output_path(self, input_path):
        """生成输出文件路径"""
        path_obj = Path(input_path)
        output_name = f"{path_obj.stem}_dedup{path_obj.suffix}"
        return str(path_obj.parent / output_name)
        
    def _generate_random_string(self, length):
        """生成随机字符串"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        
    def log_message(self, message):
        """在日志区域添加消息"""
        self.root.after(0, self._update_log, message)
        
    def _update_log(self, message):
        """更新日志显示"""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)
        
    def clear_all(self):
        """清空所有输入和重置界面到初始状态"""
        # 清空文件路径
        self.video_path.set("")
        self.output_path.set("")
        
        # 重置MD5显示
        self.original_md5.set("未选择文件")
        self.new_md5.set("未处理")
        
        # 重置功能选项到默认值
        self.mirror_var.set(False)
        self.rgb_shift_var.set(False)
        self.time_jump_var.set(True)  # 默认勾选
        self.md5_change_var.set(True)   # 默认勾选
        self.mask_invert_var.set(False)  # 新增功能默认不勾选
        self.frame_sampling_var.set(False)  # 新增功能默认不勾选
        
        # 重置新增功能参数到默认值
        self.mask_invert_value.set(0.03)
        self.frame_sampling_value.set(5)
        self.frame_sampling_random_var.set(True)
        
        # 重置进度条
        self.progress['value'] = 0
        self.progress_label.config(text="0%")
        
        # 重置状态标签
        self.status_label.config(text="请选择视频文件并选择功能", fg='#7f8c8d')
        
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