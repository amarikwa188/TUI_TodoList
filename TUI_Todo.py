from typer import Typer
from rich import print
from rich.table import Table
from rich.console import Console
from datetime import date
import json

app: Typer = Typer(no_args_is_help=True)    

table: Table = Table(show_lines=True, header_style="on blue")

table.add_column("ID", justify="center", width=3)
table.add_column("TASK", width=30)
table.add_column("STATUS", justify="center", no_wrap=True)
table.add_column("DATE CREATED", justify="center", no_wrap=True)

console: Console = Console()

def save_task(task: str|None, data: list[str]=None) -> None:
    if task:
        data = load_tasks()
        data.append(task)

    with open("tasks.json", "w") as file:
        json.dump(data, file)


def load_tasks() -> list[str]:
    try:
        with open("tasks.json", "r") as file:
            global tasks
            tasks = json.load(file)
    except FileNotFoundError:
        with open("tasks.json", "w") as file:
            json.dump([], file)

    return tasks


@app.command()
def display() -> None:
    "Display a table of all tasks."
    data: list[str] = load_tasks()

    for index, task in enumerate(data, 1):
        info, status, time = task.split("::")
        table.add_row(str(index), info, status, time)

    console.print(table)


@app.command()
def add(task: str, show:bool=True) -> None:
    "Add a task to the manager."
    new_todo: str = f"{task}::incomplete::{date.today()}"
    save_task(new_todo)
    if show: display()


@app.command()
def complete(num: int) -> None:
    data: list[str] = load_tasks()

    for index, task in enumerate(data, 1):
        if index == num:
            info, status, time = task.split('::')
            new_status: str = 'complete'
            new_task: str = '::'.join([info, new_status, time])

            del data[index-1]
            data.insert(index-1, new_task)

    save_task(task=None, data=data)
    display()


@app.command()
def reset(num: int) -> None:
    data: list[str] = load_tasks()

    for index, task in enumerate(data, 1):
        if index == num:
            info, status, time = task.split('::')
            new_status: str = 'incomplete'
            new_task: str = '::'.join([info, new_status, time])

            del data[index-1]
            data.insert(index-1, new_task)

    save_task(task=None, data=data)
    display()


@app.command()
def delete(num: int) -> None:
    data: list[str] =  load_tasks()

    for index, task in enumerate(data, 1):
        if index == num:
            del data[index-1]

    save_task(task=None, data=data)
    display()    


@app.command()
def edit(num: int, edited_task: str) -> None:
    data: list[str] = load_tasks()

    for index, task in enumerate(data, 1):
        if index == num:
            info, status, time = task.split('::')
            new_info: str = edited_task
            new_task: str = '::'.join([new_info, status, time])

            del data[index-1]
            data.insert(index-1, new_task)
    
    save_task(task=None, data=data)
    display()

    
if __name__ == "__main__":
    app()