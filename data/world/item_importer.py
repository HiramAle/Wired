import pandas
import json
from engine.loader import Loader

data_file = "WiredData.xlsx"
data = pandas.read_excel(data_file,sheet_name="Items")

items = {}
for index, row in data.iterrows():
    item = {}
    for attribute, value in row.items():
        if pandas.isnull(value) or attribute == data.columns[0]:
            continue
        item[str(attribute).lower()] = repr(value)
    items[row.iloc[0]] = item

Loader.save_json("items.json", items)
