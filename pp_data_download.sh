# FROM urban-perceptions
mkdir input 
mkdir input/pp_images
cd input/pp_images

# TRAINING IMAGES & METADATA
wget https://www.dropbox.com/s/grzoiwsaeqrmc1l/place-pulse-2.0.zip?dl=0 -O meta.zip
unzip meta.zip

rm meta.zip
