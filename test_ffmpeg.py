import subprocess
import os

FFMPEG_PATH = r"E:\ffmpeg\bin\ffmpeg.exe"

try:
    # 测试 ffmpeg 是否可用
    result = subprocess.run([FFMPEG_PATH, '-version'], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE,
                          text=True)
    
    if result.returncode == 0:
        print("FFmpeg 可用:")
        print(result.stdout)
    else:
        print("FFmpeg 命令返回错误:")
        print(result.stderr)
        
except FileNotFoundError:
    print(f"找不到 FFmpeg，检查的路径: {FFMPEG_PATH}")
except Exception as e:
    print(f"发生错误: {str(e)}")

# 检查文件是否存在
if os.path.exists(FFMPEG_PATH):
    print(f"\nFFmpeg 文件存在于: {FFMPEG_PATH}")
else:
    print(f"\nFFmpeg 文件不存在于: {FFMPEG_PATH}") 