import os
from time import time
import xarray as xr
import rioxarray
from .cog_func import cog_create_from_tif
from .s3_func import s3_push_delete_local

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

def xr_write_geotiff_from_ds(DS, primary_name, out_prefix_path):
    
    print(DS)
    print(primary_name)
    print(out_prefix_path)

    a = primary_name.split('/')
    just_tif = a[-2] + '/' + a[-1]

    output = out_prefix_path + just_tif
    bucket = 'dev-et-data'
    print(f'OUTPUT=={output}')
    DS.rio.to_raster('a.tif')
    cog_create_from_tif('a.tif', 'b_cog.tif')
    local_file='b_cog.tif'
    s3_push_delete_local(local_file, bucket, output)
    os.remove('a.tif')
