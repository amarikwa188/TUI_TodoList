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
def add(task: str) -> None:
    task = task.strip()
    if task:
        new_task: str = f"{task}::incomplete::{date.today()}"
        save_task(new_task)
        display()
    else:
        print("\nEnter a valid task")
    
if __name__ == "__main__":
    app()