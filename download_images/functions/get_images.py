import fileinput
import time
from io import BytesIO
from pathlib import Path

import requests
import utils
from PIL import Image

root_dir = Path(__file__).parent.parent
save_path = Path("outputs/downloaded/")
save_path = Path(root_dir, save_path)

# letters = {'0': 'a', '90': 'b', '180': 'c', '270': 'd'}
###################################
# Get Image from Google Street View
###################################


def download_image(url, angle):
    # global letters
    response = requests.get(url)
    im = Image.open(BytesIO(response.content))
    filename = "%s_%s" % (img_id.strip("\n"), angle)
    im.save(Path(save_path, filename + ".png"), "png")
    return print(filename + " saved to drive.")


def panoid_url(panoid, heading):
    image_url = "https://maps.googleapis.com/maps/api/streetview?"
    size = "=640x640&"
    params = "&fov=120&heading="
    paramsII = "&pitch=0&key="
    my_url = (
        image_url + "size" + size + "pano=" + panoid + params + heading + paramsII + key
    )
    return my_url


#############
# PROGRAMME
#############
start_time = time.time()

# GET API KEY one by one
key = utils.get_api(Path(Path(__file__).parent.parent, "source/api_keys/api_keys.csv"))

print(key)
counter = 0
for line in fileinput.input():
    att = line.split(",")
    panoid = str(att[2])
    img_id = str(att[9])
    azi = str(att[7])
    if len(azi) != 0:
        # try:
        letters = {
            str(int(float(att[7]) + 90)): "b",
            str(int(float(att[7]) + 270)): "d",
        }  # get building facing images
        # letters = {str(int(float(att[8]) + 0)): 'a',
        # str(int(float(att[8]) + 180)): 'c'
        # } #get down the road images
        for azi in letters:
            heading = azi
            url = panoid_url(panoid, heading)
            # print (url)
            download_image(url, letters[azi])
            counter += 1
            # except:
            print("panoid not printed: " + panoid + " " + img_id + key)
    else:
        continue
end_time = time.time()
print(
    "file is finished after  --- %s seconds --- and %s images"
    % (time.time() - start_time, counter)
)
