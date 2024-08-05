from typer import Typer
from rich import print
from rich.table import Table
from rich.console import Console
from datetime import date

app: Typer = Typer()

class Todo:
    def __init__(self, task: str, status: str) -> None:
        self.id: int = 1
        self.task: str = task
        self.status: str = status
        self.date_created: date = date.today()

    def update_status(self, new_status: str):
        self.status = new_status

    def __repr__(self) -> str:
        return f"{self.id}::{self.task}::{self.status}::{self.date_created}"
    

tasks: list[Todo] = []


@app.command()
def display() -> None:
    table: Table = Table()

    table.add_column("ID", justify="center", width=3)
    table.add_column("Task", width=30)
    table.add_column("Status", justify="center", no_wrap=True)
    table.add_column("Date Created", justify="center", no_wrap=True)

    for task in tasks:
        id, info, status, time = str(task).split("::")
        table.add_row(id, info, status, time)

    console: Console = Console()
    console.print(table)


@app.command()
def add(task: str, status:str='incomplete') -> None:
    status = status.lower()
    if status not in ('complete', 'incomplete', 'in progress'):
        print(f"\n[red]ERROR:[/red] '{status}' is not a valid status. "
              "Defaulting to 'incomplete'.\n")
        status = 'incomplete'

    new_todo: Todo = Todo(task, status)
    tasks.append(new_todo)
    display()

@app.command()
def options():
    print("\ndisplay \n\n"
          "[blue]add {task name} --status {status}[/blue]\n"
          "add the given task name with a status to the list, if a status is"
          "not given, it defaults to 'incomplete'.")


if __name__ == "__main__":
    app()