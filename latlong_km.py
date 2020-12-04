import os, glob
import math
import pandas as pd
import time
import numpy as np
from multiprocessing import Pool

def haversine_dist(ori, dest):
    lat1, lon1 = ori
    lat2, lon2 = dest
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    dist = radius * c

    return dist

def site_within(group, site_latlong):
    other_sites = latlong_df['site_latlong'].loc[latlong_df['group'] != group].tolist()
    sites = site_latlong[0]
    latlong = site_latlong[1]
    distance = [haversine_dist(latlong, x[1]) for x in other_sites]
    # distance_within = [x for x in distance]# if x< 0.3]
    site_km = list(zip([x[0] for x in other_sites], distance))
    site_km = [x for x in site_km if x[1]< 2.0]
    site_km = sorted(site_km, key=lambda tup: tup[1])
    return site_km

def parallelize_dataframe(df, func, n_cores=4):
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df

def nearest(latlong_df):
    latlong_df['nearest'] = latlong_df.apply(lambda x: site_within(x['group'], x['site_latlong']), axis=1)
    return latlong_df

if __name__ == "__main__":

    start_time = time.time()
    latlong_df = pd.read_excel('input_file/latlong_data.xlsx', header=1, index_col=0)
    latlong_df['site_latlong'] = list(zip(latlong_df['site'],list(zip(latlong_df['lat'],latlong_df['long']))))
    final_df = parallelize_dataframe(latlong_df, nearest)
    final_df.to_excel('output/result.xlsx')
    
    print("--- Processed in {} seconds ---".format((time.time() - start_time)))