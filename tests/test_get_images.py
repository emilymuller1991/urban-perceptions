import os
from pathlib import Path


def test_get_images(bash, root_dir):
    with bash(envvars={"ROOT": str(root_dir)}) as s:
        s.run_script(Path(root_dir, "tests", "get_images.sh"))
        files = os.listdir(Path(root_dir, "download_images/outputs/downloaded/"))

        assert len(files) == 4
        assert ".png" in files[0]
