import rasterio
import numpy as np

with rasterio.open('../data/DC_LandUse/DIST_11001_LandUse.tif') as src:
    array = src.read()
    # profile = src.profile()

    array[np.where(array < 5)] = 1
    array[np.where(array > 5)] = 2

with rasterio.open('../data/output/DIST_11001_LandUse_output.tif', 'w') as output:
    output.write(array)


