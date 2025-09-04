import subprocess

def config_flakpak():
    subprocess.run(["flatpak", "remote-add", "--if-not-exists", "flathub", "https://dl.flathub.org/repo/flathub.flatpakrepo"])

def install_packages(apps, source):
    command = ["pkexec"]
    match source:
        case "native":
            command.extend(["apt", "install", "-y"])
        case "flatpak":
            command.extend(["flatpak", "install", "-y"])
        case "snap":
            command.extend(["snap", "install"])
    command.extend(apps)
    print(f"selecting {source} package: {command}")
    install_command(command)

def install_command(command):
    subprocess.run(command)
    #print("Standard Output:")
    #print(result.stdout)

def update_system():
    subprocess.run(["pkexec", "snap", "refresh"])
    subprocess.run(["pkexec", "apt", "update", "-y"])
    subprocess.run(["pkexec", "flatpak", "upgrade", "-y"])

