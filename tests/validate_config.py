#!/usr/bin/env python3
"""Minimal validation smoke test for the shipped configuration."""

import copy
import json
import os
import warnings
from pathlib import Path

import nemo_action_bar
from gi.repository import Gtk


ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "buttons.json").read_text(encoding="utf-8"))
validated = nemo_action_bar.validate_config(CONFIG)
assert validated == nemo_action_bar.validate_config(
    copy.deepcopy(nemo_action_bar.DEFAULT_CONFIG)
)

assert [
    entry.get("id") for entry in validated["buttons"] if entry["type"] == "button"
] == [
    "new-folder",
    "cut",
    "copy",
    "paste",
    "duplicate",
    "rename",
    "undo",
    "redo",
    "properties",
    "select-all",
    "show-hidden",
    "copy-path",
    "open-terminal",
    "open-admin",
    "favorite",
    "archive-create",
    "archive-extract",
    "trash",
]
assert next(
    entry for entry in validated["buttons"] if entry.get("id") == "rename"
)["action"] == "rename"
assert {
    entry["id"]: entry["label"]
    for entry in validated["buttons"]
    if entry["type"] == "button"
} == {
    "new-folder": "New Folder",
    "cut": "Cut",
    "copy": "Copy",
    "paste": "Paste",
    "duplicate": "Duplicate",
    "rename": "Rename",
    "undo": "Undo",
    "redo": "Redo",
    "properties": "Properties",
    "select-all": "Select All",
    "show-hidden": "Toggle Hidden Files",
    "copy-path": "Copy Paths",
    "open-terminal": "Open in Terminal",
    "open-admin": "Open as Administrator",
    "favorite": "Toggle Favorite",
    "archive-create": "Create Archive",
    "archive-extract": "Extract Here",
    "trash": "Move to Trash",
}
for hidden_id in (
    "open-admin",
    "favorite",
    "archive-create",
    "archive-extract",
):
    hidden = next(
        entry for entry in validated["buttons"] if entry.get("id") == hidden_id
    )
    assert hidden["enabled"] is False

# Nemo has multiple GtkActions named Copy. File actions must win over an
# unrelated text/clipboard action even when that proxy is discovered first.
with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    clipboard_group = Gtk.ActionGroup(name="ClipboardActions")
    clipboard_copy = Gtk.Action(
        name="Copy", label="Copy", tooltip=None, stock_id=None
    )
    clipboard_group.add_action(clipboard_copy)
    file_group = Gtk.ActionGroup(name="DirViewActions")
    file_copy = Gtk.Action(name="Copy", label="Copy", tooltip=None, stock_id=None)
    file_group.add_action(file_copy)
assert nemo_action_bar._prefer_action_groups(
    [clipboard_copy, file_copy], nemo_action_bar.NEMO_FILE_ACTION_GROUPS
) == [file_copy]
assert nemo_action_bar._prefer_action_groups(
    [clipboard_copy], nemo_action_bar.NEMO_FILE_ACTION_GROUPS
) == [clipboard_copy]

with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    activated = []
    file_copy.set_sensitive(False)
    file_copy.connect("activate", lambda _action: activated.append(True))
    nemo_action_bar._activate_with_current_selection(file_copy)
    assert activated == [True]
    assert not file_copy.get_sensitive()
assert nemo_action_bar.FORCE_LAZY_ACTIONS == {"undo", "redo"}

# The installer and runtime must agree when a user selects an XDG config root.
original_xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
original_override = os.environ.get("NEMO_ACTION_BAR_CONFIG")
try:
    os.environ["XDG_CONFIG_HOME"] = "/tmp/nemo-action-bar-test-config"
    os.environ.pop("NEMO_ACTION_BAR_CONFIG", None)
    assert nemo_action_bar._config_path() == Path(
        "/tmp/nemo-action-bar-test-config/nemo-action-bar/buttons.json"
    )
    os.environ["NEMO_ACTION_BAR_CONFIG"] = "/tmp/nemo-action-bar-custom.json"
    assert nemo_action_bar._config_path() == Path(
        "/tmp/nemo-action-bar-custom.json"
    )
finally:
    if original_xdg_config_home is None:
        os.environ.pop("XDG_CONFIG_HOME", None)
    else:
        os.environ["XDG_CONFIG_HOME"] = original_xdg_config_home
    if original_override is None:
        os.environ.pop("NEMO_ACTION_BAR_CONFIG", None)
    else:
        os.environ["NEMO_ACTION_BAR_CONFIG"] = original_override

# Nemo's desktop is a virtual location, while browsing the user's Desktop
# directory in a regular window remains a normal file:// location.
assert nemo_action_bar._is_nemo_desktop_location("x-nemo-desktop:")
assert nemo_action_bar._is_nemo_desktop_location("X-NEMO-DESKTOP:///")
assert not nemo_action_bar._is_nemo_desktop_location(
    "file:///home/example/Desktop"
)
assert not nemo_action_bar._is_nemo_desktop_location("file:///tmp")

# Copy Paths falls back to the current folder when the active view has no
# selection, while selected files and folders retain newline-separated paths.
assert nemo_action_bar._uri_to_path_text("file:///home/example/Documents") == (
    "/home/example/Documents"
)
assert nemo_action_bar._uri_to_path_text("file:///tmp/My%20Folder") == (
    "/tmp/My Folder"
)
assert nemo_action_bar._uris_to_path_text(
    ["file:///tmp/one.txt", "file:///tmp/two.txt"]
) == "/tmp/one.txt\n/tmp/two.txt"
assert nemo_action_bar._uris_to_path_text(["file:///tmp/selected-folder"]) == (
    "/tmp/selected-folder"
)
assert nemo_action_bar._uri_to_path_text("x-nemo-desktop:") is None
assert nemo_action_bar._uri_to_path_text("") is None
assert nemo_action_bar._uris_to_path_text([]) is None

# Existing shortcut-only user configurations remain valid.
legacy = copy.deepcopy(CONFIG)
legacy["buttons"] = [
    {
        "id": "legacy-copy",
        "label": "Copy",
        "icon": "edit-copy-symbolic",
        "shortcut": "<Control>c",
    }
]
assert nemo_action_bar.validate_config(legacy)["buttons"][0]["action"] is None

invalid = copy.deepcopy(legacy)
invalid["buttons"][0].pop("shortcut")
try:
    nemo_action_bar.validate_config(invalid)
except ValueError:
    pass
else:
    raise AssertionError("button without action or shortcut was accepted")

invalid = copy.deepcopy(legacy)
invalid["buttons"][0]["action"] = "run-arbitrary-command"
try:
    nemo_action_bar.validate_config(invalid)
except ValueError:
    pass
else:
    raise AssertionError("unsupported action was accepted")
