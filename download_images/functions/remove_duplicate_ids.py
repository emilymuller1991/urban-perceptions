from pathlib import Path

import pandas as pd

root_dir = Path(__file__).parent.parent
df = pd.read_csv(Path(root_dir, "outputs/psql/test_city_road_sample_panoids.csv"))
N = df.shape[0]
df = df.drop_duplicates(subset="panoid")
M = df.shape[0]
df.to_csv(
    Path(root_dir, "outputs/psql/test_city_road_sample_panoids_unique.csv"), index=False
)

print(
    "Original dataframe had %s panoids as per roads shape file" % str(N),
    "new dataframe has %s unique panoids" % str(M),
)
print("Road coverage is %s percent" % str(float(M / N) * 100))
