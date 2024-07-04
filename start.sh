#!/usr/bin/env bash

# Execute the Python script with any passed arguments
nix-shell $HOME/Code/proxpy/shell.nix --run "python3 $HOME/Code/proxpy/Proxpy.py"
