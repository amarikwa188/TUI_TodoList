from typer import Typer
from rich import print
from rich.table import Table
from rich.console import Console
from datetime import date
import json

app: Typer = Typer()    

tasks: list[str] = []

table: Table = Table(padding=(1))

table.add_column("ID", justify="center", width=3)
table.add_column("Task", width=30)
table.add_column("Status", justify="center", no_wrap=True)
table.add_column("Date Created", justify="center", no_wrap=True)

console: Console = Console()

def save_task(task: str) -> None:
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
    data: list[str] = load_tasks()

    for index, task in enumerate(data, 1):
        info, status, time = task.split("::")
        table.add_row(str(index), info, status, time)

    console.print(table)


@app.command()
def add(task: str) -> None:
    new_todo: str = f"{task}::incomplete::{date.today()}"
    tasks.append(new_todo)
    save_task(new_todo)
    display()


if __name__ == "__main__":
    app()