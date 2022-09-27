mkdir -p $ROOT/download_images/outputs/
mkdir -p $ROOT/download_images/outputs/metadata/
rm -rf $ROOT/download_images/outputs/metadata/parallel/
mkdir -p $ROOT/download_images/outputs/metadata/parallel/

cat $ROOT/tests/tests1/test_input/test_city_20m.csv | parallel --delay 1.5 --joblog /tmp/log --progress --pipe --block 3M --files --tmpdir $ROOT/download_images/outputs/metadata/parallel python3 $ROOT/download_images/functions/parallel_grid.py
