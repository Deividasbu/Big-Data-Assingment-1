import time 
from skimage import io
import os
from multiprocessing import Pool
from main_code import convert_to_black_and_white, apply_blur, add_noise

def process_image(file_name, output_folder, technique):
    image = io.imread(file_name)
    
    if technique == 'bw':
        start_time = time.time()
        image_bw = convert_to_black_and_white(image)
        elapsed_time = time.time() - start_time
        io.imsave(os.path.join(output_folder, f"{os.path.basename(file_name)}_bw.jpeg"), image_bw)
        
    elif technique == 'blur':
        start_time = time.time()
        image_blur = apply_blur(image)
        elapsed_time = time.time() - start_time
        io.imsave(os.path.join(output_folder, f"{os.path.basename(file_name)}_blur.jpeg"), image_blur)
        
    elif technique == 'noise':
        # For noise, convert the image to black and white first (not measured)
        image_bw = convert_to_black_and_white(image)
        start_time = time.time()
        image_noised = add_noise(image_bw)  # Assume image_bw is required for noise
        elapsed_time = time.time() - start_time
        io.imsave(os.path.join(output_folder, f"{os.path.basename(file_name)}_noised.jpeg"), image_noised)
    
    return elapsed_time



if __name__ == "__main__":
    techniques = ['bw', 'blur', 'noise']

    input_folder = 'C:/Users/User/Desktop/data_set_BD/Images/'
    output_folder = 'C:/Users/User/Desktop/data_set_BD/Processed/'
    os.makedirs(output_folder, exist_ok=True)  # Ensure output folder exists
    file_names = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    # Sequential Execution
    for technique in techniques:
        start_time = time.time()
        for file_name in file_names:
            process_image(file_name, output_folder, technique)
        elapsed_time = time.time() - start_time
        print(f"Total time for {technique} processing (sequential): {elapsed_time} seconds")

    # Parallel Execution
    for technique in techniques:
        start_time = time.time()
        with Pool(processes=4) as pool:
            pool.starmap(process_image, [(file_name, output_folder, technique) for file_name in file_names])
        elapsed_time = time.time() - start_time
        print(f"Total time for {technique} processing (parallel): {elapsed_time} seconds")