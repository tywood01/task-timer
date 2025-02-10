# Task Timer

## Description

Command line utility that allows the user to keep track of time and log tasks.

You can do the following:
1. Start timing existing or new tasks.
2. Stop timing existing or new tasks.
3. Print out the total time for all or a given task.
4. Edit your existing timesheet.

## Usage

Commands:
- `delete [TASKNAME]`: Deletes a task's previous entry. You can use the --all flag to completely remove all time entries and the task.
- `view [TASKNAME]`: Shows a summary of status and total time. If left blank, it will show all entries or you can use the `--all` flag.
- `start [TASKNAME]`: Starts a task timer for a given task.
- `stop [TASKNAME]`: Stops a task timer for a given task.
- `edit`: Uses the built-in text editor to manually edit the timesheet.
