import os
from time import time
import rasterio
import xarray as xr
import rioxarray
from .cog_func import cog_create_from_tif
from .s3_func import s3_push_delete_local

def _xr_open_rasterio_retry(s3_file_name):
    cnt=10
    while(cnt>0):
        try:
            da = xr.open_rasterio(s3_file_name)
            return da
        except rasterio.errors.RasterioIOError:
                        print("Unexpected error:", sys.exc_info()[0])
                        print('oops',cnt)
                        print('oops',s3_file_name)
                        cnt = cnt - 1
                        time.sleep(4)


def xr_build_mosaic_ds(bucket ,product, tifs):

    start = time()
    my_da_list =[]
    for tif in tifs:
        da = _xr_open_rasterio_retry(f's3://{bucket}/'+tif)
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
    local_tif = a[-1]
    local_cog = 'COG_' + local_tif

    output = out_prefix_path + just_tif
    bucket = 'dev-et-data'
    print(f'OUTPUT=={output}')
    DS.rio.to_raster(local_tif)
    cog_create_from_tif(local_tif, local_cog)
    s3_push_delete_local(local_cog, bucket, output)
    os.remove(local_tif)
    local_xml = local_cog + '.aux.xml'
    os.remove(local_xml)
