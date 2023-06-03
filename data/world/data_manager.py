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
            if attribute == data.columns[0]:
                continue
            if pandas.isnull(value):
                value = ""
            item[str(attribute).lower()] = value
        items[row.iloc[0]] = item

    Loader.save_json("items.json", items)


def import_tasks():
    data = pandas.read_excel(data_file, sheet_name="Tasks")
    tasks = {}
    for index, row in data.iterrows():
        task = {}
        for attribute, value in row.items():
            if attribute in ["npcs", "next_tasks"]:
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
        npc_id = row.iloc[0]
        if pandas.isnull(npc_id):
            continue
        npc_filename = f"../npcs/{npc_id.title()}.json"
        npc_data = Loader.load_json(npc_filename)
        dialog = {}
        for attribute, value in row.items():
            if attribute in "task":
                if pandas.isnull(value):
                    value = ""
            if attribute == "text":
                value = value.strip().splitlines()
            if attribute in ["new_tasks", "requirements", "add_item","consequences"]:
                if pandas.isnull(value):
                    value = []
                else:
                    value = value.splitlines()
            dialog[str(attribute).lower()] = value
        npc_data["dialogues"].append(dialog)
        Loader.save_json(npc_filename, npc_data)


def create_npc_files():
    folder = f"../npcs"

    for file in os.listdir(folder):
        os.remove(f"{folder}/{file}")

    data = pandas.read_excel(data_file, sheet_name="NPCS")
    json_structure = {
        "name": "",
        "dialogues": [],
        "default_zone": "",
        "schedule": {week_day: "" for week_day in range(0, 7)},
        "consequences": []
    }
    for index, row in data.iterrows():
        npc_id = ""
        npc_name = ""
        default_zone = ""
        schedule = {week_day: "" for week_day in range(0, 7)}
        consequences = []
        for attribute, value in row.items():
            if pandas.isnull(value):
                value = ""
            if attribute == "id":
                npc_id = value
            if attribute == "name":
                npc_name = value
            if attribute == "default_zone":
                default_zone = value
            if str(attribute).startswith("day"):
                day = int(str(attribute)[-1])
                schedule[day] = value
            if attribute == "consequences":
                consequences = value.splitlines()
        filename = f"{folder}/{npc_id}.json"
        npc_data = json_structure.copy()
        npc_data["name"] = npc_name
        npc_data["default_zone"] = default_zone
        npc_data["schedule"] = schedule
        npc_data["consequences"] = consequences
        Loader.save_json(filename, npc_data)


if __name__ == '__main__':
    create_npc_files()
    import_dialogs()
    import_tasks()
    import_items()
