# Changelog

## 2.0.0 — 2026-09-09

- Copy the current Nemo folder path or URI when **Copy Paths** is used with no
  selection.
- Preserve newline-separated copying for selected files and folders.
- Add coverage for current-location, single-selection and multiple-selection
  path handling.

## 1.3.0 — 2026-09-09

- Add Debian packaging metadata and a reproducible `make package` target for
  system-wide Nemo installation and `nemo-extensions` review.
- Honor `XDG_CONFIG_HOME` when locating the live user configuration.
- Discover packaged icons through the standard `XDG_DATA_DIRS` search path.
- Point the public clone and CI links at the canonical `oss-singularity`
  repository.

## 1.2.1 — 2026-09-01

- Add a polished 1280×640 GitHub social-preview card and a reproducible source
  workflow for rendering it.
- Refresh the root README hero with the card, release badge and concise product
  positioning.

## 1.2.0 — 2026-08-24

- Use English for default button labels, validation errors and runtime dialogs.
- Add automated repository checks and refresh the public project presentation.

## 1.1.1 — 2026-08-14

- Do not display the action bar on Nemo's desktop surface; regular file-manager
  windows, including the actual Desktop folder, remain unchanged.

## 1.1.0 — 2026-08-11

- Keep root, favorite and archive actions available but hide them by default.
- Add a real-window README screenshot of the 14-button default layout while
  retaining the complete 18-action examples.
- Fix **Copy paths** incorrectly reporting an empty selection by resolving
  Nemo's current `DirViewActions/Copy` action instead of an unrelated GTK
  clipboard action.
- Traverse Nemo's widget/action tree without dropping submenu branches when
  short-lived Python wrapper IDs are reused.
- Handle Nemo's lazily refreshed action sensitivity while keeping selection
  checks and confirmation dialogs under Nemo's control.

## 1.0.0 — 2026-08-11

- Add a declaratively configured, live-reloading Nemo action bar.
- Provide Cut, Copy, Paste, Rename and Move to Trash defaults.
- Validate all configuration and limit actions to GTK accelerators.
