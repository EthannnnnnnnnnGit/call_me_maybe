from rich.console import Console
from rich.table import Table


def summary_print(lst_jsons: list[dict]) -> None:
    console = Console()
    table = Table(title="Summary")

    table.add_column("Prompt", justify="center", style="cyan")
    table.add_column("Name", justify="center", style="green")
    table.add_column("Parameters", justify="center", style="red")

    for json in lst_jsons:
        table.add_row(json["prompt"], json["name"], str(json["parameters"]))
        table.add_row("", "", "")

    console.print(table)
