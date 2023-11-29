### Code files for the talk at FOSS4G ASIA 2023 in Seoul, South Korea


![image](https://github.com/amanbagrecha/Foss4gAsia2023/assets/76432265/db2de1b9-32a9-43b9-8adb-56f3efb8ad8b)
https://talks.osgeo.org/foss4g-asia-2023/talk/LKWZRR/


### Environment (linux)

```
# create a virtual environment
python3 -m venv .venv

# activate the environement
source .venv/bin/activate

# install all the libraries
pip install -r reqirements.txt
```

### How to use the code

1. Run the [dataset_creation.py](https://github.com/amanbagrecha/Foss4gAsia2023/blob/main/dataset_creation.py) file after downloading the data from https://registry.opendata.aws/c2smsfloods/.
2. Run the [flood_mapping_cloud_native_foss4g23.ipynb](https://github.com/amanbagrecha/Foss4gAsia2023/blob/main/flood_mapping_cloud_native_foss4g23.ipynb) file to train and perform inference on the model.

