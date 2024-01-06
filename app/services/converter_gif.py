import os
import imageio

def create_gif_from_folder(input_dir, duration):
    image_files = sorted([f for f in os.listdir(input_dir) if f.endswith('.png')])
    gif_frames = []
    for file in image_files:
        full_path = os.path.join(input_dir, file)
        gif_frames.append(imageio.imread(full_path))

    gif_path = os.path.join(input_dir, 'animated.gif')
    imageio.mimsave(gif_path, gif_frames, duration=duration, loop=0)  # duration in seconds
