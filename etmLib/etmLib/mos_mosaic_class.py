from .log_logger import log_make_logger
from .log_logger import s3_save_log_file
from .s3_func import s3_list_pseudo_subdirs
from .s3_func import return_s3_list
from .xr_mosaic_func import xr_build_mosaic_ds
from .xr_mosaic_func import xr_write_geotiff_from_ds

def _return_list_of_years(subfolders):
    THE_YEAR_LIST = []
    for path in subfolders:
        #print(path)
        the_year = path.split('/')[-2]
        #print(the_year)
        if 'aaalog' not in the_year:
            THE_YEAR_LIST.append(the_year)
    return THE_YEAR_LIST


class Mos_mosaic:

    def __init__(self, bucket, prefix_path, year, out_prefix_path, products):
        print("hello from Mos_mosaic class")
        self.log = log_make_logger('Mos_mosaic')
        self.bucket = bucket
        self.prefix_path = prefix_path
        self.products = products
        self.year = year
        self.out_prefix_path = out_prefix_path
        msg = f'{bucket} {prefix_path} , {products}'
        self.log.info(msg)

    def _return_peers(self, tif_path, subdirs):
        self.log.info(f'{tif_path}, {subdirs}')
        peers = []
        a = tif_path.split('/')
        just_tif = a[-2] + '/' + a[-1]
        for dir in subdirs:
            peer = dir + just_tif
            peers.append(peer)
        
        return(peers)


    def _do_one_year(self, target_year, subfolders):

        target_tifs = []
        sub_sub_sub = subfolders[0] + target_year + '/'
        self.log.info(f'sub is {sub_sub_sub}')
        all_tifs = return_s3_list(self.bucket, sub_sub_sub)
        #print(all_tifs)

        target_product = self.products[0] + '_'
        for (tif,sz) in all_tifs:
            if target_product in tif:
                #print(tif)
                target_tifs.append(tif)

        for tif in target_tifs:
            tif_peers = self._return_peers(tif, subfolders)
            #print(tif_peers)
            product = target_product
            bucket = self.bucket
            ds = xr_build_mosaic_ds(bucket, product, tif_peers)
            primary_name = tif_peers[0]
            xr_write_geotiff_from_ds(ds, primary_name, self.out_prefix_path)

    def run_mosaic(self):
        self.log.info("run_mosaic")
        for prod in self.products:
            self.log.info(f'Mosaic this product: {prod}')

        if not self.prefix_path.endswith('/'):
            prefix_with_slash = self.prefix_path + '/'
        else:
            prefix_with_slash = self.prefix_path
        self.log.info(prefix_with_slash)
        subfolders = s3_list_pseudo_subdirs(self.bucket, prefix_with_slash)
        for folder in subfolders:
            print(folder)
        sub_sub = subfolders[0]
        years_list = s3_list_pseudo_subdirs(self.bucket, sub_sub)
        for year in years_list:
            print(year)

        target_year = self.year
        self.log.info(f'target year is {target_year}')

        if 'all' in target_year:
            self.log.info('DOING ALL THE YEARS')
            years = _return_list_of_years(years_list)
            for year in years:
                print(year)
                target_year=year
                self._do_one_year(target_year,subfolders)
        else:
            self._do_one_year(target_year,subfolders)


        
