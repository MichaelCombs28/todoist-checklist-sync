# Todoist Checklist Sync

Allows users to create recurring checklists that reset after a task has been
completed by first checking for all recurring tasks associated with a label
called `checklist` and uncompleting all the subtasks after. This will also
reduce your daily goal tasks since it doesn't create new tasks but uncompletes
existing ones.

## Usage

Requires python version 3.7 or higher and git.

```
git clone github.com/MichaelCombs28/todoist-checklist-sync
cd todoist-checklist-sync
pip install -r requirements
```

I recommend using [cron](https://itsfoss.com/cron-job/) and setting this to run
once every 5 - 10 minutes.

<h5 a><strong><code>Example Crontab</code></strong></h5>

```
*/5  * * * * /home/michael/bin/todoist_checklist_sync.py
```

A config file in (currently hardcoded) `~/.local/share/todoist_checklist_sync/config.json`
is required to store the users and their tokens.

<h5 a><strong><code>~/.local/share/todoist_checklist_sync/config.json</code></strong></h5>

```json
{
  "name": "michael",
  "token": "my-todoist-api-token"
}
```

Create a label called `checklist` and create a recurring task. Add subtasks to
that task and complete some of the subtasks, then complete the recurring task.

When the script runs, it should reset the subtasks.

## Limitations

You cannot manually change the date of your recurring task without the subtasks
being reset. I could fix this by checking the completed history since the last
date of the task and finding that task by ID in there. I currently have no
need or requirement to do so unless a request is opened for this feature.
