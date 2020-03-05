import rasterio
import numpy as np
import concurrent.futures
import threading
# https://rasterio.groups.io/g/main/topic/best_way_of_doing_concurrent/28593754?p=
# https://rasterio.groups.io/g/main/topic/best_way_of_doing_concurrent/28593754?p=


with rasterio.open('./data2/Virginia_1m_LU.tif', 'r') as src:
    with rasterio.open('./output/output_raster.tif', 'w', **src.profile) as dst:
        windows = [window for ij, window in dst.block_windows()]

        read_lock = threading.Lock()
        write_lock = threading.Lock()

        def process(window):
            with read_lock:
                src_array = src.read(window=window)
            result = src_array
            with write_lock:
                dst.write(result, window=window)

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=4
        ) as executor:
            executor.map(process, windows)



# with rasterio.open('./data2/Virginia_1m_LU.tif') as src:    
#     # array = src.read()
#     for ji, window in src.block_windows(1):
#         r = src.read(1, window=window)
#         dst.write(result_block, window=window)
    # profile = src.profile
    # array[np.where(array <= 5)] = 1
    # array[np.where(array >= 5)] = 2
    # with rasterio.open('./output/output_raster.tif', 'w',**profile) as dst:
    #     dst.write(array)