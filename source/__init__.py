from pathlib import Path

import requests
import typer

cli = typer.Typer()

CURRENT_PATH = Path()
HOME = CURRENT_PATH.home()
PGADMIN_EXEC_PATH = HOME / ".local/bin/pgAdmin"


@cli.callback()
def callback(): ...


@cli.command(
    name="pgAdmin",
)
def pgAdmin():
    try:
        response = requests.get(
            "https://raw.githubusercontent.com/marcocarmonadev/autoinstall-cli/main/scripts/pgAdmin"
        )
        raw_data = response.text
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print("Connection error.")
    else:
        PGADMIN_EXEC_PATH.touch(
            exist_ok=True,
        )
        PGADMIN_EXEC_PATH.write_text(raw_data)
        PGADMIN_EXEC_PATH.chmod(0o775)
        print("Reload your shell.")
