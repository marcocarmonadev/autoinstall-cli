from pathlib import Path

import requests
import typer

cli = typer.Typer()

CURRENT_PATH = Path()
HOME = CURRENT_PATH.home()
PGADMIN_EXEC_PATH = HOME / ".local/bin/pgAdmin"
UPGRADE_SYSTEM_EXEC_PATH = HOME / ".local/bin/upgrade-system"


def download_raw_data(
    script_name: str,
):
    try:
        response = requests.get(
            f"https://raw.githubusercontent.com/marcocarmonadev/autoinstall-cli/main/scripts/{script_name}"
        )
        raw_data = response.text
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print("Connection error.")
        raise typer.Abort()
    else:
        return raw_data


@cli.command(
    name="pgAdmin",
)
def pgAdmin():
    raw_data = download_raw_data(
        script_name="pgAdmin",
    )
    PGADMIN_EXEC_PATH.touch(
        exist_ok=True,
    )
    PGADMIN_EXEC_PATH.write_text(raw_data)
    PGADMIN_EXEC_PATH.chmod(0o775)
    print("Reload your shell.")


@cli.command()
def upgrade_system():
    raw_data = download_raw_data(
        script_name="upgrade-system",
    )
    UPGRADE_SYSTEM_EXEC_PATH.touch(
        exist_ok=True,
    )
    UPGRADE_SYSTEM_EXEC_PATH.write_text(raw_data)
    UPGRADE_SYSTEM_EXEC_PATH.chmod(0o775)
    print("Reload your shell.")
