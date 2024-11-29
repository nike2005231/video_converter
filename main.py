from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import os

video_path = r"C:\Users\Nike\Desktop\Scripts\Python\Video_converter_shors\Vampire.mp4"
output_folder = r"C:\Users\Nike\Desktop\Scripts\Python\Video_converter_shors\Shorts"

os.makedirs(output_folder, exist_ok=True)

clip = VideoFileClip(video_path)

target_height = 1280
target_width = 720

duration = int(clip.duration)
short_duration = 60

num_shorts = duration // short_duration

def resize_and_crop(clip):
    clip_resized = clip.resize(height=target_height)

    if clip_resized.w < target_width:
        padding = (target_width - clip_resized.w) // 2
        clip_resized = clip_resized.margin(left=padding, right=padding, color=(0, 0, 0))
    else:
        clip_resized = clip_resized.crop(x_center=clip_resized.w / 2, width=target_width)

    return clip_resized

def add_text(clip, text, position):
    font = "Roboto"
    text_clip = TextClip(text, fontsize=80, color='black', bg_color='white', font=font)

    x_pos, y_pos = position
    if y_pos == 'top':
        y_pos = 10

    text_clip = text_clip.set_position(position).set_duration(clip.duration)

    video_with_text = CompositeVideoClip([clip, text_clip])
    
    return video_with_text

def process_clip(i, start_time, end_time, output_folder):
    subclip = clip.subclip(start_time, end_time)
    subclip_resized = resize_and_crop(subclip)
    subclip_with_text = add_text(subclip_resized, f"Часть {i+1}", ('center', 'top'))

    output_path = os.path.join(output_folder, f"Часть_{i+1}.mp4")
    subclip_with_text.write_videofile(output_path, codec="libx264", fps=30)

for i in range(num_shorts):
    start_time = i * short_duration
    end_time = min((i + 1) * short_duration, duration)
    process_clip(i, start_time, end_time, output_folder)

if duration % short_duration != 0:
    start_time = num_shorts * short_duration
    end_time = duration
    process_clip(num_shorts, start_time, end_time, output_folder)