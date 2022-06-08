import os
from pathlib import Path


def test_parallel_grid(bash, root_dir):
    with bash(envvars={"ROOT": str(root_dir)}) as s:
        s.run_script(Path(root_dir, "tests", "parallel_grid.sh"))
        file = os.listdir(Path(root_dir, "outputs/metadata/parallel/"))[0]

        with open(Path(root_dir, "outputs/metadata/parallel/", file)) as f:
            data = f.read().splitlines()
            assert len(data) >= 3

            data = data[-3:]
            assert "Number of points:" in data[2]

        # assert s.path_exists('/home/blah/newdir')
        # assert s.file_contents('/home/blah/newdir/test.txt') == 'test text'
