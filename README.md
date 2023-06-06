# Proxpy

Script to switch between 2 Proxmox VMs in python

 
> **Requirements:**
> Moonlight-qt installed and computers already paired.
> Tailscale is installed and configured with moonlight ip adresses and tailscale computer names are same same as moonlight and proxmox VM.

Install Dependecies :
```
pip3 install proxmoxer requests requests_toolbelt openssh_wrapper paramiko python-dotenv
```

```
cp .env.example .env
```
Edit .env file and add values to: HOST, NODE, USER, PASSWORD and MOONLIGHTRUN.

Create proxpy alias in ~/.bash_aliases :
```
alias proxpy='python3 /<ABSOLUTE PATH TO FOLDER>/Proxpy/Proxpy.py'
```

Run script :
```
proxpy
```

> **Warning**
> The name of the computer that appears in moonlight has to be the same as the name of the VM in proxmox

> **Warning**
> For Windows PC, make sure to enable autologin (ping doesnt work while locked)