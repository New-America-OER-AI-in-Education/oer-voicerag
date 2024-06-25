# %%
from pathlib import Path
import json

from dotenv import load_dotenv
load_dotenv(override=True)

from tqdm import tqdm
import pandas as pd
from fdllmret.helpers.encoding import DocsetEncoding
from bs4 import BeautifulSoup

# %%
DATADIR = Path(__file__).resolve().parent / "data"

# %%
csvfile = DATADIR / "lesson-20240618T182814.csv"
# csvfile = DATADIR / "lesson-20240618T182920.csv"

csvdata = pd.read_csv(csvfile)

# %%
### map uuids to filenames
jsondir = DATADIR / "AmericanGovernmentJSON"
# jsondir = DATADIR / "AnatomyPhysiologyJSON"

uuidmap = {}

for jsonfile in jsondir.glob("*.json"):
    with open(jsonfile) as f:
        jsondata = json.load(f)
    uuidmap[jsondata["uuid"]] = jsonfile.stem

print(len(csvdata) == len(uuidmap))

# %%
def get_unit_tasks(unit_id, csvdata, jsondir):
    """Retrieve all tasks content associated with a UNIT_ID"""
    unit_rows = csvdata.query(f"UNIT_ID=={unit_id}")
    unit_uuids = unit_rows["UUID"].to_list()

    # load associated tasks from jsondata
    unit_tasks = {}
    for uuid in unit_uuids:
        jsonfile = jsondir / f"{uuidmap[uuid]}.json"
        if jsonfile.exists():
            with open(jsonfile) as f:
                jsondata = json.load(f)
            unit_tasks[uuid] = jsondata["tasks"]
        else:
            raise OSError(f"{jsonfile.as_posix()} doesn't exist")
    return unit_tasks

unit_id = 8460
unit_tasks = get_unit_tasks(unit_id, csvdata, jsondir)

print(json.dumps(unit_tasks, indent=4))

# %%
### for each unit, pack all of the tasks decoded html into a single string
all_units = csvdata["UNIT_ID"].unique()

tasktext = {}
for unit_id in tqdm(all_units):
    unit_tasks = get_unit_tasks(unit_id, csvdata, jsondir)
    tasktext[unit_id] = unit_tasks
    
# %%
myiter = iter(tasktext.items())