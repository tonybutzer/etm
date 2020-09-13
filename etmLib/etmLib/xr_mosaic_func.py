from time import time
import xarray as xr

def xr_build_mosaic_ds(bucket ,product, tifs):

    start = time()
    my_da_list =[]
    for tif in tifs:
        da = xr.open_rasterio(f's3://{bucket}/'+tif)
        da = da.squeeze().drop(labels='band')
        da.name=product
        my_da_list.append(da)
        tnow = time()
        elapsed = tnow - start
        print(tif, elapsed)

    DS = xr.merge(my_da_list)
    return(DS)
    
