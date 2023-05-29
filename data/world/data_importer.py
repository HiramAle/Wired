import os

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
            if attribute == "npcs":
                if pandas.isnull(value):
                    value = []
                else:
                    value = value.splitlines()
            task[str(attribute).lower()] = value

        tasks[row.iloc[0]] = task
    Loader.save_json("tasks.json", tasks)


def export_dialogs():
    npc_dialogs = "../npcs"
    for npc_file in os.listdir(npc_dialogs):
        dialogs = Loader.load_json(f"{npc_dialogs}/{npc_file}").get("dialogs", {})
        print(f"----- {npc_file} -----")
        for dialog in dialogs.values():
            dialog: list[str]
            print("\n".join(dialog))


def import_dialogs():
    data = pandas.read_excel(data_file, sheet_name="Dialogues")
    for index, row in data.iterrows():
        dialog = {}
        npc_id = ""
        for attribute, value in row.items():
            if attribute == data.columns[0]:
                continue
            if attribute == "npc_id":
                npc_id = value
                continue
            if attribute == "text":
                if pandas.isnull(value):
                    value = []
                else:
                    value = value.splitlines()
            if attribute == "mission_requirement":
                if pandas.isnull(value):
                    value = {}
                else:
                    mission, status = value.split(" ")
                    value = {mission: int(status)}
                print(value)
            if attribute == "new_mission":
                if pandas.isnull(value):
                    value = ""
            dialog[attribute] = value
        # print(npc_id, dialog)
        filename = f"../npcs/{npc_id.title()}.json"
        npc_json = Loader.load_json(filename)
        npc_json["dialogs"][str(row.iloc[0])] = dialog
        Loader.save_json(filename, npc_json)


if __name__ == '__main__':
    import_tasks()
    import_dialogs()
