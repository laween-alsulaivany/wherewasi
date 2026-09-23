import json
from datetime import datetime
from pathlib import Path

import click
from click_default_group import DefaultGroup
from rich import box
from rich.console import Console
from rich.panel import Panel


@click.group(cls=DefaultGroup, default="launch", default_if_no_args=True)
def cli():
    """A tool to help you remember where you left off"""
    pass


console = Console()


@cli.command("launch")
def launch():
    fileExists()
    existing_state = _checkState()
    if existing_state == "read":
        _newNote()
    else:
        _showNote()
        _changeState()


def _checkState():
    "Check if previous note exists or not"
    with open("log.json", "r", encoding="utf-8") as file:
        log_file = json.load(file)
        state = log_file[-1]["state"]
    return state


def _newNote():
    console.print("Start Typing... ", style="dim")

    with open("log.json", "r", encoding="utf-8") as file:
        log_file = json.load(file)

        note_id = 1 + int(log_file[-1]["id"])
        timestamp = str(datetime.now())[:16]  # Concatenate to Format: YYYY-MM-DD HH:MM
        content = console.input()
        state = "unread"

        new_entry = {
            "id": note_id,
            "timestamp": timestamp,
            "content": content,
            "state": state,
        }
        if new_entry["content"] != "":
            log_file.append(new_entry)

    with open("log.json", "w") as file:
        json.dump(log_file, file, indent=4)


def _showNote(n=0):
    with open("log.json", "r", encoding="utf-8") as file:
        log_file = list(reversed(json.load(file)))

    if len(log_file) <= 1:
        return

    my_panel = Panel(
        f"{log_file[n]['content']}",
        style="on #1f2937",
        subtitle=f"{log_file[n]['timestamp']}",
        subtitle_align="right",
        safe_box=True,
        box=box.ROUNDED,
        expand=False,
        padding=(1, 1),
        highlight=True,
        border_style="bright_magenta",
    )
    console.print(my_panel)


def _changeState():
    "changes the state of the most recent note to read"
    with open("log.json", "r", encoding="utf-8") as file:
        log_file = json.load(file)

        log_file[-1]["state"] = "read"

    with open("log.json", "w") as file:
        json.dump(log_file, file, indent=4)


def _showLogs(limit=3):
    with open("log.json", "r", encoding="utf-8") as file:
        log_file = list(reversed(json.load(file)))
    if limit > len(log_file) - 1:
        limit = len(log_file) - 1
    for i in range(limit - 1, -1, -1):
        my_panel = Panel(
            f"{log_file[i]['content']}",
            style="on #1f2937",
            title=f"Note: {log_file[i]['id']}",
            title_align="left",
            subtitle=f"{log_file[i]['timestamp']}",
            subtitle_align="right",
            safe_box=True,
            box=box.ROUNDED,
            expand=False,
            padding=(1, 1),
            highlight=True,
            border_style="bright_magenta",
        )
        console.print(my_panel)
        print()


# Helper methods
def fileExists(file_name="log.json"):
    current_directory = str(Path.cwd())
    file_path = Path(current_directory + "\\" + file_name)
    if file_path.exists():
        with open(file_name, "r", encoding="utf-8") as file:
            try:
                content = json.load(file)
            except json.JSONDecodeError:
                content = []
            if len(content) < 1:
                content.append(
                    {"id": 0, "timestamp": 0, "content": "", "state": "read"}
                )
        with open(file_name, "w") as file:
            json.dump(content, file, indent=4)
        return
    else:
        createFile(file_name)


def createFile(file_name):
    with open(file_name, "w") as file:
        new_entry = [
            {
                "id": 0,
                "timestamp": 0,
                "content": "",
                "state": "read",
            },
        ]
        json.dump(new_entry, file, indent=4)


# CLI command aliases
@cli.command("write")
def newNote():
    """Write a new note"""
    _newNote()


@cli.command("show")
def showNote():
    """Show the most recent note"""
    _showNote()


@cli.command("log")
def showLogs(limit=3):
    "shows the X (default = 3) most recent notes"
    _showLogs(limit)


if __name__ == "__main__":
    # fileExists()
    launch()
