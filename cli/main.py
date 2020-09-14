import python_terraform as tf
import typer


app = typer.Typer()


@app.command()
def new():
    pass


@app.command()
def init():
    pass


@app.command()
def plan(
    init: bool = typer.Option(
        False, help="Should terraform init be run before terraform plan"
    ),
    project_home: str = typer.Option(".", help="The root of the project"),
    no_terraform: bool = typer.Option(False, help="Skip terraform planning"),
):
    """Identify the plan that will be executed on a subsequent apply

    """
    t = tf.Terraform(working_dir=f"{project_home}/infra")
    if not tf_command(t, "plan", init):
        return


@app.command()
def deploy(
    init: bool = typer.Option(
        False, help="Should terraform init be run before terraform apply"
    ),
    project_home: str = typer.Option(".", help="The root of the project"),
    auto: bool = typer.Option(False),
):
    t = tf.Terraform(working_dir=f"{project_home}/infra")
    if not tf_command(t, "apply", init):
        return


def tf_command(t: tf.Terraform, cmd, init_first: bool=False):
    if init:
        typer.echo(f"Running 'terraform init' in {t.working_dir}")
        tf_command(t, "init")
    typer.echo(f"Running 'terraform {cmd}' in {t.working_dir}")
    func = getattr(t, cmd)
    return_code, stdout, stderr = func()
    if return_code != 0:
        typer.echo(f"Terraform failed with return code {return_code}")
        typer.echo(stderr)
        return False
    else:
        typer.echo(stdout)
        return True


if __name__ == "__main__":
    app()
