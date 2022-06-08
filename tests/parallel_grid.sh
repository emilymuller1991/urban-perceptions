mkdir $ROOT/download_images/outputs/metadata/
mkdir $ROOT/download_images/outputs/metadata/parallel/

cat $ROOT/tests/test_input/test_city_20m.csv | parallel --delay 1.5 --joblog /tmp/log --progress --pipe --block 3M --files --tmpdir $ROOT/download_images/outputs/metadata/parallel python3 $ROOT/download_images/functions/parallel_grid.py