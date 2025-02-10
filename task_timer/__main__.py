import click, csv
from datetime import datetime, timedelta
from pathlib import Path

# Static Global Variables.
filepath = Path(__file__).parent / "log.csv"
cyan = "cyan"
red = "red"
green = "green"

def load_data_from_csv(filepath):
    """Load data from filepath to dictionary."""
    data_dict = {}
    with open(filepath, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            task = row[0]
            timestamps = [datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f") for time in row[1:] if time]
            data_dict[task] = timestamps

    return data_dict

def save_data_to_csv(data_dict, filepath):
    """Save data from dictionary to filepath."""
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for task, timestamps in data_dict.items():
            writer.writerow([task] + timestamps)
    return

def sum_timestamps(timestamps):
    """Add up the total time given a sequence of timestamps formatted: [start, stop...]"""
    delta = sum((timestamps[i + 1] - timestamps[i] for i in range(0, len(timestamps) - 1, 2)), timedelta())
    total_seconds = int(delta.total_seconds())
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    return days, hours, minutes, seconds

def running(timestamps):
    """
    Check to see if a given task is currently being timed 
    by checking the number of entries in the timestamps.
    """
    return len(timestamps) % 2 == 0

@click.group()
def main():
    pass

@main.command()
@click.argument('task')
def start(task):
    """
    [TASKNAME] Starts a task timer for a given task.
    """

    tasks = load_data_from_csv(filepath)

    if task in tasks:

        if running(tasks[task]):
            tasks[task].append(datetime.now())
            
        else:
            click.echo(click.style(f"ERROR:\nTask {task} is already started.", fg=red, bold=True))
            return

    else:
        tasks[task] = [datetime.now()]

    click.echo(click.style(f"SUCCESS:\nTask {task} has been started.", fg=green, bold=True))
    save_data_to_csv(tasks, filepath)
    return

@main.command()
@click.argument('task')
def stop(task):
    """
    [TASKNAME] Stops a task timer for a given task.
    """

    tasks = load_data_from_csv(filepath)

    if task not in tasks or running(tasks[task]):
        click.echo(click.style(f"ERROR:\nTask {task} hasn't been started.", fg=red, bold=True))
        return
            
    else:
        tasks[task].append(datetime.now())


    click.echo(click.style(f"SUCCESS:\nTask {task} has been stopped.", fg=green, bold=True))
    save_data_to_csv(tasks, filepath)
    return


@main.command()
@click.option("--all", is_flag=True, help="Show log of timed tasks.")
@click.argument('task', required=False, default="")
def view(task, all):
    """
    [TASKNAME] Shows a summary of status and total time.
    """
    tasks = load_data_from_csv(filepath)

    if all or task == "":
        for task in tasks:
            days, hours, minutes, seconds = sum_timestamps(tasks[task])
            print(f"Task {task} total time: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds")

    elif task in tasks:
        days, hours, minutes, seconds = sum_timestamps(tasks[task])
        print(f"Task {task} total time: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds")

    else:
        click.echo(click.style(f"ERROR:\nTask {task} hasn't been started.", fg=red, bold=True))
    return

@main.command()
@click.option("--all", is_flag=True, help="Deletes all entries for a task.")
@click.argument('task', required=False, default="")
def delete(task, all):
    """
    [TASKNAME] [ENTRYNO] deletes a tasks entries by index.
    """
    tasks = load_data_from_csv(filepath)

    if all:
        if click.confirm(click.style(f"WARNING:\nThis will delete all entries for {task} are you sure?", fg=red, bold=True), abort=True):
            tasks.pop(task, None) 
            
    else:
        if click.confirm(click.style(f"WARNING:\nThis will delete the previous entry for {task} are you sure?", fg=red, bold=True), abort=True):
            if running(tasks[task]):
                tasks[task] = tasks[task][:-2]
            else:
                tasks[task] = tasks[task][:-1]

    save_data_to_csv(tasks, filepath)

    return

@main.command()
def edit():
    """
    Uses built-in text editor to manually edit timesheet.
    """
    click.edit(filename=filepath)
    return

if __name__ == '__main__':
    main()