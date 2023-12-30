import os
import imageio

def create_gif_from_images(image_folder, gif_path):
    images = []
    for file_name in sorted(os.listdir(image_folder)):
        if file_name.endswith('.png'):
            file_path = os.path.join(image_folder, file_name)
            images.append(imageio.imread(file_path))
    imageio.mimsave(gif_path, images, duration=500, loop=0)