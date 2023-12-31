import os
import imageio

def create_gifs_from_folders(input_dir):
    animation_dir = os.path.join(input_dir, "animated")
    os.makedirs(animation_dir, exist_ok=True)

    for folder_name in os.listdir(input_dir):
        folder_path = os.path.join(input_dir, folder_name)
        
        if os.path.isdir(folder_path):
            image_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.png')])

            if image_files:
                images = []
                for filename in image_files:
                    file_path = os.path.join(folder_path, filename)
                    images.append(imageio.imread(file_path))

                gif_path = os.path.join(animation_dir, f'{folder_name}.gif')
                imageio.mimsave(gif_path, images, duration=100, loop=0) # duration in seconds