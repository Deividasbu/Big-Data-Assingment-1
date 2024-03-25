import os
import multiprocessing
from skimage import io, color, filters
import numpy as np
from skimage.exposure import rescale_intensity
from skimage.filters import threshold_otsu

def find_optimal_threshold(image):
    # Find a threshold that divides the image into two parts as equally as possible
    hist, bin_edges = np.histogram(image, bins=256, range=(0,1))
    cumulative_hist = np.cumsum(hist)
    total_pixels = image.size
    # Find the threshold where the number of pixels on each side is as equal as possible
    optimal_threshold_index = np.abs(cumulative_hist - (total_pixels / 2)).argmin()
    optimal_threshold = bin_edges[optimal_threshold_index]
    return optimal_threshold

def convert_to_black_and_white(image):
    # Convert to grayscale
    im_gray = color.rgb2gray(image)
    # Find optimal threshold
    threshold = find_optimal_threshold(im_gray)
    # Convert to black and white
    im_bw = im_gray > threshold
    im_bw_uint8 = (im_bw * 255).astype(np.uint8)
    return im_bw_uint8


def apply_blur(image, sigma=3):
    # Apply Gaussian blur
    im_blur = filters.gaussian(image, sigma=sigma)
    im_blur_uint8 = (im_blur * 255).astype(np.uint8)
    return im_blur_uint8

def add_noise(image_bw, fraction=0.1):
    # Identify black pixels
    black_indices = np.where(image_bw == 0)
    num_noise_pixels = int(len(black_indices[0]) * fraction)
    if num_noise_pixels == 0:
        return image_bw
    # Select random indices to add noise
    noise_indices = np.random.choice(len(black_indices[0]), num_noise_pixels, replace=False)
    # Add noise
    for idx in noise_indices:
        x, y = black_indices[0][idx], black_indices[1][idx]
        image_bw[x, y] = 255  # Changing black pixels to white as example noise
    return image_bw

def process_image(file_name, output_folder):
    # Read image
    image = io.imread(file_name)
    # Convert to black and white
    image_bw = convert_to_black_and_white(image)
    # Apply blur
    image_blur = apply_blur(image)
    # Add noise to the black and white image
    image_noised = add_noise(image)
    # Save images
    base_name = os.path.splitext(os.path.basename(file_name))[0]
    io.imsave(os.path.join(output_folder, f"{base_name}_bw.jpeg"), image_bw)
    io.imsave(os.path.join(output_folder, f"{base_name}_blur.jpeg"), image_blur)
    io.imsave(os.path.join(output_folder, f"{base_name}_noised.jpeg"), image_noised)

# Example usage
if __name__ == "__main__":
    input_folder = 'C:/Users/User/Desktop/data_set_BD/Sample/'
    output_folder = 'C:/Users/User/Desktop/data_set_BD/Processed/'
    os.makedirs(output_folder, exist_ok=True)

    file_names = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    with multiprocessing.Pool(processes=4) as pool:
        pool.starmap(process_image, [(file_name, output_folder) for file_name in file_names])
