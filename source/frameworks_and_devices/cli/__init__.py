import subprocess
from pathlib import Path

import requests
import typer

app = typer.Typer()


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
):
    raw_data = download_raw_data(script_name)
    exec_file_path = Path.home() / f".local/bin/{script_name}"
    exec_file_path.touch(
        exist_ok=True,
    )
    exec_file_path.write_text(raw_data)
    exec_file_path.chmod(0o775)


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


@app.command(
    name="pgAdmin",
)
def pgAdmin():
    create_exec_file(
        script_name="pgAdmin",
    )


@app.command()
def upgrade_system():
    create_exec_file(
        script_name="upgrade-system",
    )
