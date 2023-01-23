import json
import os
import platform
import subprocess
import sys

from talon import Context, Module, actions, app, speech_system

from user.pyvoice_talon.rpc import add_method
from user.pyvoice_talon.sublime_client import send_sublime

mod = Module()

ctx = Context()
vscode_ctx = Context()
vscode_ctx.matches = r"""
app: vscode
"""

# @mod.action
# def send_sublime(c: str, data: dict) -> int:
#     """Sent Dated Sublime"""
#     return send_sublime(c, data)


mod.list("pyvoice_importable")
ctx.lists["user.pyvoice_importable"] = {"last": "last"}

mod.list("pyvoice_subsymbol")
ctx.lists["user.pyvoice_subsymbol"] = {"last": "last"}

mod.list("pyvoice_expression")
ctx.lists["user.pyvoice_expression"] = {"last": "last"}


@add_method()
def enhance_spoken(list_name, data):
    print("Enhancing: ", list_name, len(data), data[0])
    # print("getpass.getuser(): ", getpass.getuser())
    # app.notify(body=str(len(data)) + str(data[0]))  # json.dumps(data))
    ctx.lists[f"user.pyvoice_{list_name}"] = {x["spoken"]: json.dumps(x) for x in data}
    return True


@mod.capture(rule="{user.pyvoice_subsymbol} | {user.pyvoice_importable}")
def pyvoice_importable_all(m) -> str:
    return m[0]


@mod.action
def insert_pyvoice_expression(data: str) -> None:
    """
    Insert LSP Expression with Parentheses
    if needed via keypresses
    """
    actions.insert(json.loads(data)["value"])
    print(data)
    if data[-1] == ")":
        actions.key("left")


@mod.action
def insert_pyvoice_qualified(data: str) -> None:
    """Print importable as qualified name"""
    d = json.loads(data)
    # t = ".".join(*(d["module"] + d["name"]))
    t = ".".join([d["module"], d["name"]])
    actions.insert(f'"{t}"')


@mod.action
def pyvoice_add_import(data: str) -> None:
    """Add import to file"""
    send_sublime(
        "lsp_execute",
        {
            "command_name": "add_import",
            "session_name": "LSP-pyvoice",
            "command_args": ["$file_uri", json.loads(data)],
        },
    )


@vscode_ctx.action("user.pyvoice_add_import")
def pyvoice_add_import(data: str) -> None:
    """Add import to file"""
    print("in here... vscode version")
    actions.user.vscode_with_plugin(
        "pyvoice.lsp_execute",
        "add_import",
        ["$file_uri", json.loads(data)],
    )


@mod.action
def pyvoice_from_import(data: str) -> None:
    """2 step from import"""
    send_sublime(
        "lsp_execute",
        {
            "command_name": "from_import",
            "session_name": "LSP-pyvoice",
            "command_args": [json.loads(data)],
        },
    )


@vscode_ctx.action("user.pyvoice_from_import")
def pyvoice_from_import(data: str) -> None:
    """2 step from import"""
    actions.user.vscode_with_plugin(
        "pyvoice.lsp_execute",
        "from_import",
        [json.loads(data)],
    )


@mod.action
def pyvoice_from_import_fuzzy(data: str, name: str, every: bool) -> None:
    """single step fuzzy import"""
    send_sublime(
        "lsp_execute",
        {
            "command_name": "from_import_fuzzy",
            "session_name": "LSP-pyvoice",
            "command_args": ["$file_uri", json.loads(data), name or "", every],
        },
    )


@vscode_ctx.action("user.pyvoice_from_import_fuzzy")
def pyvoice_from_import_fuzzy(data: str, name: str, every: bool) -> None:
    """single step fuzzy import"""
    actions.user.vscode_with_plugin(
        "pyvoice.lsp_execute",
        "from_import_fuzzy",
        ["$file_uri", json.loads(data), name or "", every],
    )
