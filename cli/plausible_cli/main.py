import python_terraform as tf
import typer
from plausible_cli.util import TerraformConfig
import basket_case as bc


# import util
import json

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


@app.command()
def compile(
    file: str = typer.Option("config.yaml"), output_tf: str = typer.Option(None)
):
    c = TerraformConfig("0.1.6")
    yaml_config = c.compile(file)
    tf_config = c.generate(yaml_config)
    if output_tf:
        with open(output_tf, "w") as fd:
            fd.write(json.dumps(tf_config, indent=2))


NL = "\n"


@app.command()
def docs():

    c = TerraformConfig("0.1.6")
    doc = c.docs()
    # json_str = json.dumps(c.docs(), indent=2)
    # print(json_str)
    with open("config.md", "w") as fd:
        for d in doc:
            for k, v in d.items():
                _element_to_md(v, 1, fd)


def h(s, n):
    return f"{'#'*n} {s} {2*NL}"


def p(s):
    return f"{s} {2*NL}"


def lb(s, fw=False, colon=True, optional=False):
    q = "`" if fw else ""
    c = ":" if colon else ""
    o = " (Opt)" if optional else ""

    return f"**{q}{s}{q}**{o}{c}"


def li(s):
    return f"* {s}{NL}"


def link(s, u):
    return f"[{s}]({u})"


def maybe_title(v, depth):
    depth = 2

    if "title" in v:
        title = v["title"]
        link = f'<a name="{title}"></a>[#](#{title})'
        if v.get("label", "") == "resource":
            return h(f"{link} **Resource**: `{v['title']}`", 1)
        else:
            return h(f"{link} `{v['title']}` :: {v.get('_type', '')}", 2)
    else:
        return h(f"`no title` {v.get('_type', 'xxx')}", depth)
        # return ""


def maybe_example(v):
    if "example" in v:
        ex = v["example"]
        return f"""
    {ex}
"""
    else:
        return ""


SCALAR_TYPES = ["String", "Enum", "Integer"]


def _element_to_md(v, depth, fd):
    include = not v.get("skip", False)
    if "_type" in v:
        if v["_type"] == "Object":
            # An object has a known set of keys; corresponds to a Map in strictyaml. Front matter is striaghtforward, but the handling of the keys and values depends in large part on the type of the value
            if include:
                fd.write(NL)
                fd.write(maybe_title(v, depth))
                if "text" in v:
                    fd.write(p(v["text"]))
                fd.write(maybe_example(v))
                for a, b in v["keys"].items():
                    optional = b.get("Optional", False)
                    if b.get("_type", "") in SCALAR_TYPES:
                        fd.write(
                            li(
                                f"{lb(a, fw=True, optional=optional)} {b.get('text', '')}"
                            )
                        )
                    elif b.get("_type", "") is "Or":
                        fd.write(
                            li(
                                f"{lb(a, fw=True, optional=optional)} {b['a']['_type']} *or* {b['b']['_type']}"
                            )
                        )

                    elif b.get("_type", "") is not "Any":
                        fd.write(
                            li(
                                f"{link(lb(a, fw=True, colon=False, optional=optional), '#'+a)}"
                            )
                        )
                fd.write(NL)
            for a, b in v["keys"].items():
                if b.get("_type", "") not in SCALAR_TYPES:
                    _element_to_md(b, depth, fd)
        elif v["_type"] == "Map":
            # A Map has arbitrary keys; corresponds to a MapPattern in strictyaml. Values are handled somewhat similarly to Map, although all values must have the same validator so there's no iteration
            fd.write(maybe_title(v, depth))
            fd.write(p(v.get("text", "")))
            fd.write(maybe_example(v))
            fd.write(li(lb("Key") + " "))
            _element_to_md(v["key"], depth, fd)

            optional = v["value"].get("Optional", False)
            if v["value"].get("_type", "") in SCALAR_TYPES:
                fd.write(
                    li(
                        f"{lb('Value', fw=True, optional=optional)} {v['value'].get('text', '')}"
                    )
                )
            elif v["value"].get("_type", "") is "Or":
                fd.write(
                    li(
                        f"{lb('Value', fw=True, optional=optional)} {v['value']['a']['_type']} *or* {v['value']['b']['_type']}"
                    )
                )

            elif v["value"].get("_type", "") is not "Any":
                fd.write(
                    li(
                        f"{link(lb('Value', fw=True, colon=False, optional=optional), '#'+v['key'].get('title',''))}"
                    )
                )
            _element_to_md(v["value"], depth, fd)
            # fd.write(2*NL)
        elif v["_type"] == "List":
            fd.write(maybe_title(v, depth))
            fd.write(p(v.get("text", "")))
            fd.write(maybe_example(v))
            if v["item"]["_type"] in SCALAR_TYPES:
                fd.write("Item: ")
            _element_to_md(v["item"], depth, fd)
            fd.write(NL)
        elif v["_type"] == "FixedList":
            fd.write(maybe_title(v, depth))
            fd.write(p(v.get("text", "")))
            fd.write(maybe_example(v))
            for item in v["items"]:
                _element_to_md(item, depth, fd)
        elif v["_type"] in SCALAR_TYPES:
            fd.write(f"*{v['_type']}* ")
            fd.write(p(v["text"]))
        elif v["_type"] == "Or":
            # fd.write("A ")
            _element_to_md(v["a"], depth, fd)
            # fd.write(2*NL)
            # fd.write("B ")
            _element_to_md(v["b"], depth, fd)
        elif v["_type"] == "Optional":
            fd.write(p(v["text"]))
        elif v["_type"] == "Any":
            if "any_options" in v:
                # Create links to the schemas accepted by the Any wildcard
                for opt in v["any_options"]:
                    fd.write(
                        li(link(lb(opt, fw=True, colon=False) + " =>", f"{opt}.md"))
                    )


def tf_command(t: tf.Terraform, cmd, init_first: bool = False):
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
