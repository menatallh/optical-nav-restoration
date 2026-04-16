import os
import cv2
import numpy as np
from tqdm import tqdm
from glob import glob

def center_crop(img, crop_size):

    h, w = img.shape[:2]
    start_x = (w - crop_size) // 2
    start_y = (h - crop_size) // 2
    return img[start_y:start_y + crop_size, start_x:start_x + crop_size]

def add_flares_to_lit_parts_with_crop(normal_images_path, flare_images_path, output_path, alpha=0.5, brightness_threshold=200, crop_size=512):
    """
    Add flares to the lit parts of normal images, crop the result to 512x512, and save.

    Args:
        normal_images_path (str): Path to folder containing normal images.
        flare_images_path (str): Path to folder containing flare images.
        output_path (str): Path to save blended images.
        alpha (float): Opacity of the flare image. Range: 0 (no flare) to 1 (only flare).
        brightness_threshold (int): Pixel intensity threshold for applying the flare.
        crop_size (int): Desired size of the cropped output images.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    normal_images = glob(os.path.join(normal_images_path, "*.*"))
    flare_images = glob(os.path.join(flare_images_path, "*.*"))

    if not flare_images:
        print("No flare images found.")
        return

    print(f"Found {len(normal_images)} normal images and {len(flare_images)} flare images.")

    for idx, normal_image_path in tqdm(enumerate(normal_images), desc="Processing Images"):
        # Load normal image
        normal_img = cv2.imread(normal_image_path)
        if normal_img is None:
            print(f"Could not load normal image: {normal_image_path}")
            continue

        # Select a random flare image
        flare_image_path = flare_images[idx % len(flare_images)]
        flare_img = cv2.imread(flare_image_path)
        if flare_img is None:
            print(f"Could not load flare image: {flare_image_path}")
            continue

        # Blend the images with the mask
        blended_img = blend_images_with_mask(normal_img, flare_img, alpha, brightness_threshold)

        # Crop the blended image to center
        cropped_img = center_crop(blended_img, crop_size)

        # Save the cropped image
        output_file = os.path.join(output_path, f"cropped_blended_{idx:04d}.png")
        cv2.imwrite(output_file, cropped_img)

        print(f"Saved {output_file} and {plot_filename}")



def blend_images(normal_img, flare_img, alpha=0.5):
    if normal_img.shape != flare_img.shape:
        flare_img = cv2.resize(flare_img, (normal_img.shape[1], normal_img.shape[0]))
    blended = cv2.addWeighted(normal_img, 1 - alpha, flare_img, alpha, 0)
    return blended

def add_flares(normal_images_path, flare_images_path, output_path, alpha=0.5):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    normal_images = glob(os.path.join(normal_images_path, "*.*"))#[:10]
    flare_images = glob(os.path.join(flare_images_path, "*.*"))#[:10]

    if not flare_images:
        print(f"No flare images found in {flare_images_path}.")
        return

    print(f"Processing directory: {normal_images_path}")
    print(f"Found {len(normal_images)} normal images and {len(flare_images)} flare images.")

    for idx, normal_image_path in tqdm(enumerate(normal_images), desc="Processing Images"):
        normal_img = cv2.imread(normal_image_path)
        if normal_img is None:
            print(f"Could not load normal image: {normal_image_path}")
            continue

        normal_img = cv2.resize(normal_img, (512, 512))

        # Optional: Save resized image (remove if not needed)
        resized_output_dir = os.path.join(output_path, "resized_images")
        os.makedirs(resized_output_dir, exist_ok=True)
        resized_image_path = os.path.join(resized_output_dir, f"resize_{idx:04d}.png")
        cv2.imwrite(resized_image_path, normal_img)

        flare_image_path = flare_images[idx % len(flare_images)]
        flare_img = cv2.imread(flare_image_path)
        if flare_img is None:
            print(f"Could not load flare image: {flare_image_path}")
            continue

        blended_img = blend_images(normal_img, flare_img, alpha)

        # Create output file name using original image name
        base_name = os.path.splitext(os.path.basename(normal_image_path))[0]
        output_file = os.path.join(output_path, f"{base_name}_blended.png")
        cv2.imwrite(output_file, blended_img)

def process_all_subdirs(parent_directory, flare_images_path, main_output_path, alpha=0.5):
    for root, dirs, files in os.walk(parent_directory):
        # Skip processing if there are no image files in this directory
        image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not image_files:
            continue

        # Use the relative path to recreate the folder structure in the output directory
        rel_path = os.path.relpath(root, parent_directory)
        output_path = os.path.join(main_output_path, rel_path)

        add_flares(root, flare_images_path, output_path, alpha)


# ==== SET THESE PATHS ====
parent_directory = "/home/menah-hamman/Downloads/speedplusv2"  # Parent directory with multiple subfolders of images
flare_images_path = "/home/menah-hamman/Downloads/Flare7K++/Flare7Kpp/Flare-R/Compound_Flare"  # Path to flare images
main_output_path = "/home/menah-hamman/output_images/"  # Where to store all blended outputs
alpha = 0.5

process_all_subdirs(parent_directory, flare_images_path, main_output_path, alpha)
