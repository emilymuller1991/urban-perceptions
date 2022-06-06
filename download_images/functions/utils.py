from urllib.request import urlopen
import re
import streetview
import numpy as np
from ast import literal_eval
import pandas as pd

#~~~ APIKEY and URL ~~~#
metadata_url = 'https://maps.googleapis.com/maps/api/streetview/metadata?'

def get_api(path):
    # GET API KEY one by one
    keys = pd.read_csv(path)
    key = keys.iloc[0]['API Key']
    keys = keys.drop(keys.index[0])
    keys = keys.drop(columns = ['Unnamed: 0'])
    keys.to_csv(path)
    return key

def dont_convert_line(line):
    # get co-ordinates
    x = np.float64(line.split(',')[0])
    y = np.float64(line.split(',')[1])
    #x, y = convert_lonlat(x, y)
    return x, y

def pano_image_metadata(pano):
    # takes unique pano and outputs: owner, date, location, pano_id and status.
    # parameters
    size = '=600x300&'
    params = '&fov=90&heading=235&pitch=10&key='
    # fetch url
    my_url = metadata_url + 'size' + size + 'pano=' + pano + params + key
    return urlopen(my_url).read().decode("utf-8")

def get_date(url_output):
    # returns year and month of panoids for those which do not have
    searchObj = re.search(r'(.*) "date" (.*?) .*', url_output)
    date = literal_eval(searchObj.group(0).split()[2].split(',')[0])
    year = int(date[:4])
    month = int(date[-2:])
    return year, month

def google_status(url_output):
    # returns copyright ownership
    try:
        searchObj_g = re.search(r'(.)"© (.*?).*', url_output)
        searchObj_s = re.search(r'(.) "status" (.*?).*', url_output)

        owner = searchObj_g.group(0)[4:-2]
        status = searchObj_s.group(0)[-3:-1]
    except:
        owner = 0
        status = 0
    return owner, status

def get_panoids(x, y, all_gps, all_pano):
    # takes 4386 CRS co-ordinates as input 
    # to Google API checks if the scraped image is owned and has OK status
    # by Google and outputs list of panoids

    # obtain list of panoids over years [{'panoid': 'id', 'lat', 'lon', 'year': 2008, 'month': 7},...,{}]

    panoids = streetview.panoids(lat=y, lon=x)
    point = (x,y)
    # adds unique pano_ids to dictionaries
    all_gps[str(point)] = []
    for pano in panoids:
        # don't add to dictionary if it already exists
        if pano['panoid'] in all_pano.keys():
            pass
        else:
            # check if the metadata is complete 
            if 'year' in pano.keys():
                try:
                    # is google and status
                    results = pano_image_metadata(pano['panoid'])
                    owner, status = google_status(results)
                    if owner == "Google" and status == "OK":
                        # add to pano dictionary
                        all_gps[str(point)].append(pano['panoid'])
                        all_pano[pano['panoid']] = {key: pano[key] for key in ['lat', 'lon', 'year', 'month']}
                    else:
                        pass
                except:
                    print ('pano is not added because error somewhere')
                    continue
            else:
            # otherwise send request for year and month
                try:
                    # get owner and google
                    results = pano_image_metadata(pano['panoid'])
                    owner, status = google_status(results)
                    if owner == "Google" and status == "OK":
                        # get year and month
                        year, month = get_date(results)
                        all_gps[str(point)].append(pano['panoid'])
                        all_pano[pano['panoid']] = {key: pano[key] for key in ['lat', 'lon']}
                        all_pano[pano['panoid']]['year'] = year
                        all_pano[pano['panoid']]['month'] = month
                    else:
                        pass
                except:
                    print ('pano is not added because error somewhere')
                    continue
    return