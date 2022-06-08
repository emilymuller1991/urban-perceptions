from pathlib import Path

import pandas as pd


def test_parallel_output(bash, root_dir):
    with bash(envvars={"ROOT": str(root_dir)}) as s:
        s.run_script(Path(root_dir, "tests", "parallel_output.sh"))

        # check file has summarised output
        assert s.path_exists(
            Path(root_dir, "download_images/outputs/metadata/test_city_20m_panoids.csv")
        )

        # check output is non-zero
        df = pd.read_csv(
            Path(root_dir, "download_images/outputs/metadata/test_city_20m_panoids.csv")
        )
        assert df.shape[0] != 0
