import rasterio
import numpy as np
import concurrent.futures
import threading
# https://rasterio.groups.io/g/main/topic/best_way_of_doing_concurrent/28593754?p=
# https://rasterio.groups.io/g/main/topic/best_way_of_doing_concurrent/28593754?p=


with rasterio.open('./data/DIST_11001_LandUse.tif', 'r') as src:
    with rasterio.open('./output/output_raster.tif', 'w', **src.profile) as dst:
        windows = [window for ij, window in dst.block_windows()]

        read_lock = threading.Lock()
        write_lock = threading.Lock()

        def process(window):
            with read_lock:
                src_array = src.read(window=window)
            # result = src_array
            src_array[np.where(src_array <= 5)] = 1
            src_array[np.where(src_array > 5)] = 2
            with write_lock:
                dst.write(result, window=window)

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=4
        ) as executor:
            executor.map(process, windows)




# with rasterio.open('./data/DIST_11001_LandUse.tif') as src:    
#     array = src.read()
#     profile = src.profile
#     array[np.where(array <= 5)] = 1
#     array[np.where(array > 5)] = 2
#     with rasterio.open('./output/output_raster.tif', 'w',**profile) as dst:
#         dst.write(array)


wetlands = rasterio.open('./data/DIST_11001_LandUse.tif')
landcover = rasterio.open('./data/DIST_11001_LandUse.tif')
# loss = rasterio.open('./data/DIST_11001_LandUse.tif')
# dst = rasterio.open('./data/DIST_11001_LandUse.tif')
if wetlands.shape == landcover.shape:
    # Do Process
    # dst[np.where(wetlands <= 5)] = 1

# # Do Stuff


wetlands.close()
# r2.close()
# r3.close()



