import os, glob
import math
import pandas as pd
import time
import numpy as np
from multiprocessing import Pool
import argparse


def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='input file name, excel or csv')
    parser.add_argument('--output', type=str, help='output file name, excel or csv')
    parser.add_argument('--within_radius', type=str, help='unit in km')
    parser.print_help()

    return parser.parse_args()

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

def site_within(group, site_latlong, radius):
    other_sites = latlong_df['site_latlong'].loc[latlong_df['group'] != group].tolist()
    sites = site_latlong[0]
    latlong = site_latlong[1]
    distance = [haversine_dist(latlong, x[1]) for x in other_sites]
    # distance_within = [x for x in distance if x< 2.0]
    site_km = list(zip([x[0] for x in other_sites], distance))
    site_km = [x for x in site_km if x[1]< radius]
    site_km = sorted(site_km, key=lambda tup: tup[1])
    return site_km

if __name__ == "__main__":

    args = init_args()

    start_time = time.time()
    latlong_df = pd.read_excel(args.input, header=1, index_col=0)
    latlong_df['site_latlong'] = list(zip(latlong_df['site'],list(zip(latlong_df['lat'],latlong_df['long']))))
    latlong_df['radius_limit'] = float(args.within_radius)
    latlong_df['nearest'] = latlong_df.apply(lambda x: site_within(x['group'], x['site_latlong'], x['radius_limit']), axis=1)
    latlong_df.to_excel(args.output)
    
    print("--- Processed in {} seconds ---".format((time.time() - start_time)))