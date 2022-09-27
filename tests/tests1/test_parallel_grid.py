import os
from pathlib import Path

import pandas as pd


def test_parallel_grid(bash, root_dir):
    with bash(envvars={"ROOT": str(root_dir)}) as s:
        s.run_script(Path(root_dir, "tests", "tests1", "parallel_grid.sh"))
        file = os.listdir(Path(root_dir, "download_images/outputs/metadata/parallel/"))[
            0
        ]

        with open(
            Path(root_dir, "download_images/outputs/metadata/parallel/", file)
        ) as f:
            data = f.read().splitlines()
            assert len(data) >= 3

            data = data[-3:]
            assert "Number of points:" in data[2]


def test_parallel_output(bash, root_dir):
    with bash(envvars={"ROOT": str(root_dir)}) as s:
        s.run_script(Path(root_dir, "tests", "tests1", "parallel_output.sh"))

        # check file has summarised output
        assert s.path_exists(
            Path(root_dir, "download_images/outputs/metadata/test_city_20m_panoids.csv")
        )

        # check output is non-zero
        df = pd.read_csv(
            Path(root_dir, "download_images/outputs/metadata/test_city_20m_panoids.csv")
        )
        assert df.shape[0] != 0
