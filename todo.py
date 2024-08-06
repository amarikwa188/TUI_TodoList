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


def save_data(data: list[str]) -> None:
    with open("tasks.json", "w") as file:
            json.dump(data, file)


def save_task(task: str) -> None:
    data: list[str] = load_data()
    data.append(task)

    save_data(data)


def load_data() -> list[str]:
    try:
        with open("tasks.json", "r") as file:
            data: list[str] = json.load(file)
    except FileNotFoundError:
        with open("tasks.json", "w") as file:
            data: list[str] = []
            json.dump(data, file)

    return data


@app.command()
def display() -> None:
    data: list[str] = load_data()

    for index, task in enumerate(data, 1):
        info, status, time = task.split("::")
        table.add_row(str(index), info, status, time)

    console.print(table)


@app.command()
def add(tasks: list[str]) -> None:
    for index, task in enumerate(tasks):
        task = task.strip()
        if task:
            new_task: str = f"{task}::incomplete::{date.today()}"
            save_task(new_task)
        else:
            print(f"\ntask index {index} is not a valid task\n")
    display()


def update_status(stat: str, nums: list[int]) -> None:
    data: list[str] = load_data()

    for index, task in enumerate(data, 1):
        if index in nums:
            info, _, time = task.split("::")
            new_task: str = '::'.join([info, stat, time])

            del data[index-1]
            data.insert(index-1, new_task)
            save_data(data)


@app.command()
def complete(task_nums: list[int]) -> None:
    update_status('complete', task_nums)
    display()


@app.command()
def progress(task_nums: list[int]) -> None:
    update_status('in progress', task_nums)
    display()


@app.command()
def incomplete(task_nums: list[int]) -> None:
    update_status('incomplete', task_nums)
    display()


@app.command()
def edit(task_num: int, new_info: str) -> None:
    data: list[str] = load_data()

    for index, task in enumerate(data, 1):
        if index == task_num:
            _, status, time = task.split("::")
            new_task: str = '::'.join([new_info, status, time])
            
            del data[index-1]
            data.insert(index-1, new_task)
            save_data(data)
            break

    display()

    
if __name__ == "__main__":
    app()