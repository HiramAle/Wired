import pandas
import json
from engine.loader import Loader

data_file = "WiredData.xlsx"


def import_items():
    data = pandas.read_excel(data_file, sheet_name="Items")
    items = {}
    for index, row in data.iterrows():
        item = {}
        for attribute, value in row.items():
            if pandas.isnull(value) or attribute == data.columns[0]:
                continue
            item[str(attribute).lower()] = value
        items[row.iloc[0]] = item

    Loader.save_json("items.json", items)


def import_tasks():
    data = pandas.read_excel(data_file, sheet_name="Tasks")
    tasks = {}
    for index, row in data.iterrows():
        task = {}
        for attribute, value in row.items():
            task[str(attribute).lower()] = value
        tasks[row.iloc[0]] = task
    Loader.save_json("tasks.json", tasks)


if __name__ == '__main__':
    import_items()
