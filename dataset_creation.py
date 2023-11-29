"""Dataset Creation"""
# users need to have planetary computer API installed along with `adlfs` package installed
"""
Prerequisite: Download the labelled dataset from https://registry.opendata.aws/c2smsfloods/
              Find the chips folder inside the downloaded data and `cd` into that

We are downloading 4-band satellite data for the labelled flood imagery to our local machine

"""
import glob
import re
import shutil
import stackstac
import numpy as np
import pystac_client
import planetary_computer
import rioxarray as rxr
from pathlib import Path

S1_label_paths = sorted(glob.glob("chips/*/s1/*/LabelWater.tif"))
S1_img_paths = [[path.replace("LabelWater.tif", "VV.tif"), path.replace("LabelWater.tif", "VH.tif")] for path in S1_label_paths]

Path('images').mkdir(exist_ok=True)
Path('labels').mkdir(exist_ok=True)

def extract_date(filename):
    # Regular expression to match the date pattern
    match = re.search(r'S1[A,B]_IW_GRDH_1SDV_(\d{8})', filename)
    if match:
        # Extract and format the date
        date_str = match.group(1)
        
        formatted_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
        return formatted_date
    else:
        return "Date not found"

# Example usage
date = extract_date(S1_label_paths[0])
print("Extracted Date:", date)



catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace,
)


for idx,iw in enumerate(S1_label_paths):

        my_arr = rxr.open_rasterio(iw)
        reprj_iw = my_arr.rio.reproject('epsg:4326')
        epsg = my_arr.rio.crs
        bbox = reprj_iw.rio.bounds()
        bounds = my_arr.rio.bounds()
        date = extract_date(iw)
        # print(date)
        search = catalog.search(
            collections=["sentinel-1-rtc"], bbox=bbox, datetime=date
        )
        items = search.item_collection()
        if len(items) == 0:
            print(f"skipping {idx}, iw")
            continue
        print(f"Found {len(items)} items")
        item = items[0]

        search = catalog.search(collections=["nasadem"], bbox=bbox)
        items = search.item_collection()
        items.items.append(item)
        ds = stackstac.stack(items, bounds=bounds, epsg=int(epsg.to_authority()[1]) , resolution=10).mean(dim='time')
        ds = ds.to_dataset(dim='band')
        ds['vv_vh'] = ds.vv / ds.vh
        ds[['vv', 'vh', 'vv_vh', 'elevation']].rio.set_crs(epsg).rio.to_raster(f'images/{idx}.tif', dtype=np.float32)
        shutil.copyfile(iw, f"labels/{idx}.tif")
