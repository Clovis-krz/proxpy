# Proxpy

Script to switch between 2 Proxmox VMs in python

 
> **Requirements:**
> Moonlight-qt installed and computers already paired.
> Tailscale is installed and configured with moonlight ip adresses and tailscale computer names are same same as moonlight and proxmox VM.
## Requirements
1. Moonlight-qt installed
2. A Proxmox server setup
3. A Proxmox VM with GPU passtrough, sunshine and tailscale installed and setup
## Install Dependecies :

### NixOS
Requires direnv installed
```bash
echo "use nix" >> .envrc && direnv allow
```

### Other linux
```bash
pip3 install proxmoxer requests requests_toolbelt openssh_wrapper paramiko python-dotenv
```

## Environment
```bash
cp .env.example .env
```
Edit .env file and add values to: HOST, NODE, USER, PASSWORD and MOONLIGHTRUN.
## Alias
### NixOS
Create `start.sh` file
```sh
#!/usr/bin/env bash
nix-shell $HOME/<PATH TO FOLDER>/proxpy/shell.nix --run "python3 $HOME/<PATH TO FOLDER>/proxpy/Proxpy.py"
```

Add to your `configuration.nix` 
```nixos
programs.bash.shellAliases = {
   proxpy = "sh $HOME/<PATH TO FOLDER>/proxpy/start.sh";
};
```

### Other Linux
Create proxpy alias in ~/.bash_aliases :
```bash
alias proxpy='python3 $HOME/<PATH TO FOLDER>/proxpy/Proxpy.py'
```
## Start Proxpy
Run script :
```bash
proxpy
```

> **Warning**
> The name of the computer that appears in moonlight has to be the same as the name of the VM in proxmox

> **Warning**
> For Windows PC, make sure to enable autologin (ping doesnt work while locked)