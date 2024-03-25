# Big-Data-Assignment-1

The submitted project operates as follows: initially, functions for image transformations are defined in the 'main' code:

- `find_optimal_threshold` performs histogram equalization to balance the number of black and white pixels to be as equal as possible.
- `convert_to_black_and_white` applies the aforementioned threshold for setting the pixels to be either black or white.
- `apply_blur` uses a Gaussian kernel with a sigma parameter=3 to allocate the pixels for blurring.
- `add_noise` identifies and counts the number of black pixels, then calculates the 10% fraction of those pixels, and randomly assigns that fraction of the pixels to be transformed to white ones.
- `process_image` applies each of the aforementioned processing techniques and saves the resulting images.

The next part of the code defines the input and output paths that should be edited accordingly. In this example, a smaller subsample of the entire dataset is used for time-convenience.

The `pool.starmap` function uses the defined `process_image` function to apply multiprocessing.

For comparing both approaches, the `evaluation.py` script operates as follows:
- The amount of time spent applying the image transformations sequentially for each technique is calculated.
- Then, the amount of time applying the image transformations with parallel multiprocessing for each technique is calculated.
- Comparing the two durations, it is observed that multiprocessing works faster for each technique, and this advantage increases as the number of images processed increases as well.
