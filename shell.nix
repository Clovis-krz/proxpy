let
  # We pin to a specific nixpkgs commit for reproducibility.
  # Last updated: 2024-04-29. Check for new commits at https://status.nixos.org.
  pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/cf8cc1201be8bc71b7cbbbdaf349b22f4f99c7ae.tar.gz") {};
in pkgs.mkShell {
  packages = [ 
    pkgs.python3
    (pkgs.python3.withPackages (python-pkgs: [
      # select Python packages here
      python-pkgs.proxmoxer
      python-pkgs.requests
      python-pkgs.requests_toolbelt
      python-pkgs.paramiko
      python-pkgs.python-dotenv
    ]))
  ];
}