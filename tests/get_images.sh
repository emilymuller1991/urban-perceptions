mkdir -p $ROOT/download_images/outputs/
mkdir -p $ROOT/download_images/outputs/downloaded/

cat $ROOT/tests/test_input/test_city00 | parallel --delay 1.5 --joblog /tmp/log --pipe --block 2M --ungroup python3 $ROOT/download_images/functions/get_images.py