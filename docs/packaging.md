# Packaging and upstream path

Nemo Action Bar is a Nemo Python UI extension. It is not a Cinnamon Spices
applet or extension, so its natural distribution paths are the project
repository, a distribution package, or an accepted contribution to the Linux
Mint `nemo-extensions` repository.

## Debian package

The root `setup.py` and `debian/` metadata follow the existing Python-package
shape used by `linuxmint/nemo-extensions`: the extension is installed below
`/usr/share/nemo-python/extensions`, while its public icon and default JSON
remain in a separate package data directory.

Build the binary package locally with:

```console
sudo apt install build-essential debhelper dh-python python3-all python3-setuptools
make package
```

The package keeps configuration per user. It does not overwrite an existing
`$XDG_CONFIG_HOME/nemo-action-bar/buttons.json`, and the user-local
`install.sh` remains available for installations without root privileges.

## Linux Mint upstream proposal

The prepared package shape is suitable for a contribution branch in
`linuxmint/nemo-extensions`, whose current build uses a project directory,
Debian metadata, `setup.py` for Python data files, and a `build-order` entry.
Acceptance and inclusion in a Linux Mint package are separate from this
project's GitHub release and are not implied by the presence of this metadata.
