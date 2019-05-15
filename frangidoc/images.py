import os
import shutil
import logging


def discover(root):
    images = list()

    for root_, dirs, files in os.walk(root):
        relative_root = root_[len(root):]
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                images.append(os.path.join(relative_root, file))

    return images


def copy(source_folder, destination_folder):
    for image in discover(source_folder):
        destination = destination_folder + image

        if not os.path.isdir(os.path.dirname(destination)):
            os.makedirs(os.path.dirname(destination))

        shutil.copy2(
            source_folder + image,
            destination
        )

        logging.info('Copied image : {}'.format(image))
