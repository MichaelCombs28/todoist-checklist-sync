#!/usr/bin/env python

import logging
import json
import sys
import pathlib
import todoist


logger = logging.getLogger(__name__)


LABEL_NAME = "checklist"

data_dir = pathlib.Path.home() / ".local" / "share" / "todoist_checklist_sync"

data_file = data_dir / "data.json"
config_file = data_dir / "config.json"



if __name__ == '__main__':
    data_dir.mkdir(parents=True, exist_ok=True)
    if not config_file.exists():
        logger.error("Config file %s is required", config_file)
        sys.exit(1)

    with config_file.open("r") as f:
        configs = json.load(f)

    if data_file.exists():
        with data_file.open('r') as f:
            data = json.load(f)
    else:
        data = {}

    for config in configs:
        username = config["name"]
        token = config["token"]
        sync_api = todoist.TodoistAPI(token, cache=str(data_dir / username / ""))
        sync_api.sync()

        accessed = []
        user_data = data.get(username, {})
        labels = sync_api.labels.all(filt=lambda l: l["name"].lower() == LABEL_NAME)
        if len(labels) != 1:
            logger.error("Error while looking for the checklist label ID for user %s, must provide exactly 1 but provided %d", username, len(labels))
            continue

        label_id = labels[0]["id"]
        for task in sync_api.items.all(filt=lambda t: label_id in t["labels"]):
            task_id = str(task["id"])

            if task_id in user_data and task["due"] is not None and task["due"]["is_recurring"]:
                dt = task["due"]["date"]
                if user_data[task_id] != dt:
                    for completed_subtask in sync_api.items_archive.for_parent(task["id"]).items():
                        completed_subtask.uncomplete()

                    user_data[task_id] = dt

                accessed.append(task_id)
            elif task["due"] is not None and task["due"]["is_recurring"]:
                dt = task["due"]["date"]
                user_data[task_id] = dt
                accessed.append(task_id)

        # Cleanup stale data
        for task_id in list(user_data.keys()):
            if task_id not in accessed:
                user_data.pop(task_id)

        sync_api.commit()
        data[username] = user_data

    with data_file.open('w') as f:
        json.dump(data, f)
