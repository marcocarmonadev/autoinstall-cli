import subprocess
from pathlib import Path

import requests
import typer

cli = typer.Typer()

CURRENT_PATH = Path()
HOME = CURRENT_PATH.home()
PGADMIN_EXEC_PATH = HOME / ".local/bin/pgAdmin"
UPGRADE_SYSTEM_EXEC_PATH = HOME / ".local/bin/upgrade-system"


def run_exec_script(
    script_name: str,
):
    raw_data = download_raw_data(script_name)
    subprocess.run(
        raw_data,
        shell=True,
    )


def create_exec_file(
    script_name: str,
    path: Path,
):
    raw_data = download_raw_data(script_name)
    path.touch(
        exist_ok=True,
    )
    path.write_text(raw_data)
    path.chmod(0o775)


def download_raw_data(
    script_name: str,
):
    try:
        response = requests.get(
            f"https://raw.githubusercontent.com/marcocarmonadev/autoinstall-cli/main/scripts/{script_name}"
        )
        raw_data = response.text
        response.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        match exc.response.status_code:
            case 404:
                print("Script not found!")
            case _:
                print("Exception uncaught!")
        raise typer.Abort()
    else:
        return raw_data


@cli.command(
    name="pgAdmin",
)
def pgAdmin():
    create_exec_file(
        script_name="pgadmin",
        path=PGADMIN_EXEC_PATH,
    )


@cli.command()
def upgrade_system():
    create_exec_file(
        script_name="upgrade-system",
        path=UPGRADE_SYSTEM_EXEC_PATH,
    )


@cli.command()
def poetry():
    run_exec_script(
        script_name="poetry",
    )


@cli.command()
def pyenv():
    run_exec_script(
        script_name="pyenv",
    )


@cli.command()
def all():
    print("Installing pgAdmin ...")
    pgAdmin()
    print("Installing upgrade-system ...")
    upgrade_system()
