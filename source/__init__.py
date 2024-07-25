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
            "https://gist.githubusercontent.com/marcocarmonadev/313402864136e2be615665636ddc6f10/raw/9f79033c748959bd2bff475e0d136a133675817c/pgAdmin"
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
