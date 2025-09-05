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

#
#This is a bad way to do this, in the future will be revised
# ( ** get the list of installed packages )
#
def verify_if_package_are_installed(package):
    command = ["apt", "list"]
    command.append(package)
    
    result = subprocess.run(command, capture_output=True)
    print(result.stdout)
    if result.stdout == "error: no matching snaps installed":
        print("not installed")  
    print(result.stderr)
    print(result.stdout)

def list_native_installed_packages():
    result = subprocess.run(["apt", "list", "--installed"], capture_output=True)
    splited = result.split('\n')
    print(splited)

def list_flatpak_installed_packages():
    output = subprocess.run(["flatpak", "list", "--columns", "name"], capture_output=True).stdout
    splited = output.splitlines()
    print(splited)
    for item in splited:
        print(item)