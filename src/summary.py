from rich.console import Console
from rich.table import Table
from typing import Any


def summary_print(lst_jsons: list[dict[str, Any]]) -> None:
    console = Console()
    table = Table(title="Summary")

    table.add_column("Prompt", justify="center", style="cyan")
    table.add_column("Name", justify="center", style="green")
    table.add_column("Parameters", justify="center", style="red")

    for json in lst_jsons:
        params = ""
        if json["parameters"]:
            for key, value in json["parameters"].items():
                params += f"{key}: {value}\n"
        table.add_row(json["prompt"], json["name"], params)
        table.add_row("", "", "")

    console.print(table)
