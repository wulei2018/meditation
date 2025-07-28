import os
import subprocess
from pathlib import Path
import math
import time
from datetime import datetime

# 定义 FFmpeg 路径
FFMPEG_PATH = r"E:\ffmpeg\bin\ffmpeg.exe"
FFPROBE_PATH = r"E:\ffmpeg\bin\ffprobe.exe"

# 定义时长列表（分钟）
DURATIONS = [3, 5, 10, 15, 20, 30]

# 定义输入和输出目录
INPUT_VIDEO_DIR = 'assets/videos/mp4'
INPUT_AUDIO_DIR = 'assets/videos/mp3'
OUTPUT_BASE_DIR = 'assets/videos'

# 视频压缩设置
VIDEO_SETTINGS = {
    'crf': 23,  # 压缩质量，范围0-51，数字越大压缩率越高，质量越低
    'preset': 'medium',  # 编码速度预设，可选：ultrafast,superfast,veryfast,faster,fast,medium,slow,slower,veryslow
    'maxrate': '2M',  # 最大比特率
    'bufsize': '4M',  # 缓冲大小
    'scale': '-2:720'  # 分辨率，-2表示自动计算以保持纵横比
}

def get_media_info(file_path):
    """获取媒体文件的详细信息"""
    try:
        # 获取时长
        duration_cmd = [
            FFPROBE_PATH, 
            '-v', 'error', 
            '-show_entries', 'format=duration', 
            '-of', 'default=noprint_wrappers=1:nokey=1', 
            file_path
        ]
        duration_result = subprocess.run(duration_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 获取比特率
        bitrate_cmd = [
            FFPROBE_PATH,
            '-v', 'error',
            '-show_entries', 'format=bit_rate',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            file_path
        ]
        bitrate_result = subprocess.run(bitrate_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if duration_result.returncode != 0 or bitrate_result.returncode != 0:
            raise Exception(f"获取媒体信息失败: {duration_result.stderr.decode() or bitrate_result.stderr.decode()}")
        
        return {
            'duration': float(duration_result.stdout.decode()),
            'bitrate': int(bitrate_result.stdout.decode() or 0)
        }
    except Exception as e:
        print(f"错误: 无法获取 {file_path} 的媒体信息: {str(e)}")
        return None

def create_concat_file(media_path, num_loops, temp_file):
    """创建循环连接文件"""
    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            for _ in range(num_loops):
                f.write(f"file '{media_path}'\n")
        return True
    except Exception as e:
        print(f"错误: 创建连接文件失败: {str(e)}")
        return False

def create_looped_media(input_path, duration_needed, temp_prefix, is_video=True):
    """创建循环的媒体文件（视频或音频）"""
    media_info = get_media_info(input_path)
    if media_info is None:
        return None, None

    original_duration = media_info['duration']
    num_loops = math.ceil(duration_needed / original_duration)
    print(f"{'视频' if is_video else '音频'} 信息:")
    print(f"  - 原始时长: {original_duration:.2f}秒")
    print(f"  - 比特率: {media_info['bitrate']/1000:.0f}kbps")
    print(f"  - 循环次数: {num_loops}")
    
    # 创建临时的循环列表文件
    temp_concat_file = f'temp_concat_{temp_prefix}.txt'
    temp_output = f'temp_looped_{temp_prefix}.{"mp4" if is_video else "mp3"}'
    
    try:
        if not create_concat_file(os.path.abspath(input_path), num_loops, temp_concat_file):
            return None, None

        # 连接媒体文件
        concat_cmd = [
            FFMPEG_PATH,
            '-f', 'concat',
            '-safe', '0',
            '-i', temp_concat_file
        ]
        
        if is_video:
            # 对视频进行压缩和处理
            concat_cmd.extend([
                '-c:v', 'libx264',  # 使用 H.264 编码
                '-crf', str(VIDEO_SETTINGS['crf']),  # 压缩质量
                '-preset', VIDEO_SETTINGS['preset'],  # 编码速度
                '-maxrate', VIDEO_SETTINGS['maxrate'],  # 最大比特率
                '-bufsize', VIDEO_SETTINGS['bufsize'],  # 缓冲大小
                '-vf', f'scale={VIDEO_SETTINGS["scale"]}',  # 调整分辨率
                '-profile:v', 'high',  # 使用高规格配置
                '-level', '4.1',  # 兼容性级别
                '-movflags', '+faststart',  # 优化网络播放
                '-y'  # 覆盖已存在的文件
            ])
        else:
            # 音频直接复制
            concat_cmd.extend([
                '-c', 'copy',
                '-y'
            ])
            
        concat_cmd.append(temp_output)
        
        result = subprocess.run(concat_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise Exception(f"FFmpeg 错误: {result.stderr.decode()}")
        
        return temp_output, original_duration
        
    except Exception as e:
        print(f"错误: 创建循环媒体失败: {str(e)}")
        return None, None
        
    finally:
        # 清理临时的连接列表文件
        if os.path.exists(temp_concat_file):
            os.remove(temp_concat_file)

def check_media_compatibility(video_path, audio_path):
    """检查视频和音频的兼容性"""
    video_info = get_media_info(video_path)
    audio_info = get_media_info(audio_path)
    
    if video_info is None or audio_info is None:
        return False
        
    video_duration = video_info['duration']
    audio_duration = audio_info['duration']
    
    # 检查时长差异
    duration_diff = abs(video_duration - audio_duration)
    if duration_diff > 1.0:  # 允许1秒的误差
        print(f"警告: 时长不匹配")
        print(f"  - 视频: {video_duration:.2f}秒")
        print(f"  - 音频: {audio_duration:.2f}秒")
        print(f"  - 差异: {duration_diff:.2f}秒")
    
    return True

def process_video(video_num, total_videos):
    """处理单个视频"""
    video_path = os.path.join(INPUT_VIDEO_DIR, f'{video_num}.mp4')
    audio_path = os.path.join(INPUT_AUDIO_DIR, f'{video_num}.mp3')
    
    print(f"\n[{video_num}/{total_videos}] 处理文件 {video_num}")
    print(f"视频文件: {video_path}")
    print(f"音频文件: {audio_path}")
    
    if not (os.path.exists(video_path) and os.path.exists(audio_path)):
        print(f"跳过 {video_num}: 视频或音频文件不存在")
        return False
    
    if not check_media_compatibility(video_path, audio_path):
        print(f"跳过 {video_num}: 视频和音频不兼容")
        return False
    
    success_count = 0
    # 为每个目标时长处理视频
    for duration in DURATIONS:
        duration_seconds = duration * 60
        
        output_dir = os.path.join(OUTPUT_BASE_DIR, f'{duration}min')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f'{video_num}.mp4')
        
        print(f"\n处理中: {video_num} - {duration}分钟版本")
        process_start_time = time.time()
        
        try:
            # 创建循环视频
            temp_video, video_duration = create_looped_media(
                video_path, 
                duration_seconds, 
                f'video_{video_num}_{duration}',
                is_video=True
            )
            
            if not temp_video:
                print("创建循环视频失败，跳过此时长版本")
                continue
            
            # 创建循环音频
            temp_audio, audio_duration = create_looped_media(
                audio_path, 
                duration_seconds, 
                f'audio_{video_num}_{duration}',
                is_video=False
            )
            
            if not temp_audio:
                print("创建循环音频失败，跳过此时长版本")
                if os.path.exists(temp_video):
                    os.remove(temp_video)
                continue
            
            # 计算实际需要的视频和音频循环次数
            video_loops = math.ceil(duration_seconds / video_duration)
            audio_loops = math.ceil(duration_seconds / audio_duration)
            print(f"循环信息:")
            print(f"  - 目标时长: {duration}分钟 ({duration_seconds}秒)")
            print(f"  - 视频循环: {video_loops}次")
            print(f"  - 音频循环: {audio_loops}次")
            
            # 合并循环后的视频和音频，并裁剪到指定时长
            final_cmd = [
                FFMPEG_PATH,
                '-i', temp_video,
                '-i', temp_audio,
                '-t', str(duration_seconds),
                '-map', '0:v',  # 使用第一个输入（视频）的视频流
                '-map', '1:a',  # 使用第二个输入（音频）的音频流
                '-c:v', 'copy',  # 保持视频编码不变
                '-c:a', 'aac',  # 将音频转换为 AAC 格式
                '-b:a', '128k',  # 音频比特率
                '-shortest',  # 使用最短的输入流长度
                '-y',  # 覆盖已存在的文件
                output_path
            ]
            result = subprocess.run(final_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            if result.returncode == 0:
                process_time = time.time() - process_start_time
                output_info = get_media_info(output_path)
                original_size = os.path.getsize(video_path) / 1024 / 1024
                output_size = os.path.getsize(output_path) / 1024 / 1024
                compression_ratio = (1 - output_size / (original_size * video_loops)) * 100
                
                print(f"完成 {duration} 分钟版本:")
                print(f"  - 处理用时: {process_time:.1f}秒")
                print(f"  - 输出时长: {output_info['duration']:.2f}秒")
                print(f"  - 输出大小: {output_size:.1f}MB")
                print(f"  - 压缩率: {compression_ratio:.1f}%")
                success_count += 1
            else:
                print(f"错误: 合并视频和音频失败: {result.stderr.decode()}")
            
        except Exception as e:
            print(f"错误: 处理失败: {str(e)}")
            
        finally:
            # 清理临时文件
            for temp_file in [temp_video, temp_audio]:
                if temp_file and os.path.exists(temp_file):
                    os.remove(temp_file)
    
    return success_count == len(DURATIONS)

def main():
    """主函数"""
    start_time = time.time()
    print(f"开始处理视频... ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    print(f"将处理 {len(DURATIONS)} 个时长版本: {', '.join(map(str, DURATIONS))} 分钟")
    
    total_videos = 13  # 修改为13个视频
    success_count = 0
    
    # 处理所有视频
    for i in range(1, total_videos + 1):
        if process_video(i, total_videos):
            success_count += 1
    
    total_time = time.time() - start_time
    print(f"\n处理完成! ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    print(f"总用时: {total_time:.1f}秒")
    print(f"成功处理: {success_count}/{total_videos} 个视频")
    print(f"生成的文件位于: {os.path.abspath(OUTPUT_BASE_DIR)}")

if __name__ == "__main__":
    main() 