import os, sys, json, shutil
import requests as rq
from colorama import Fore, init
from pyunpack import Archive


def install_mod(mod_list):
    extract_error = f"{Fore.RED}Error : Archive has not been able to be extracted. " \
                    f"Please verify that the link is correct."

    download_error = f"{Fore.RED}Error : File has not be able to be downloaded. " \
                     f"Please verify your internet connection or verify that the link is correct."

    for x in enumerate(mod_list):
        i, url = x
        extension = ".zip"
        print("Downloading..")

        try:
            r = rq.get(url)  # Download the file from the internet
        except Exception:
            input(download_error)
            sys.exit()

        # Check for the type of the file
        str_data = str(r.content)
        match str_data[2]:
            case "K":
                extension = ".zip"
            case "R":
                extension = ".rar"
            case "7":
                extension = ".7z"

        mod_path = os.path.join(script_path, f"mod{extension}")  # Define the path of the mod archive

        # Copy mod to the computer
        with open(mod_path, "wb") as f:
            f.write(r.content)
        print("Download complete!")

        print("Extracting..")

        os.chdir(script_path)

        if not os.path.exists("Outdir"):
            os.mkdir("Outdir")

        try:
            Archive(mod_path).extractall("Outdir")
        except Exception:
            input(extract_error)
            sys.exit()

        os.chdir("Outdir")

        if os.path.exists("mod.json"):
            with open("mod.json") as j:
                mod_name = json.load(j)["Metadata"]["Name"]

            print(f"Installing {mod_name}")
            os.mkdir(os.path.join(target_path, mod_name))
            try:
                Archive(mod_path).extractall(os.path.join(target_path, mod_name))
            except Exception:
                input(extract_error)
                sys.exit()

        else:
            print("")
            Archive(mod_path).extractall(target_path)

        os.chdir("..")
        shutil.rmtree("Outdir")
        os.remove(mod_path)  # Delete archive

        print(f"{Fore.YELLOW}Mod {i + 1} out of {len(mod_list)} installed")


def main():
    init(autoreset=True)  # Initialize colorama module
    os.system("cls")  # Clear the console to make the colorama module work correctly with the cmd

    global target_path, script_path  # Make certain variables global

    target_path = os.path.join(os.environ["APPDATA"], "Sonic3AIR\\mods")  # Define the mods folder path
    script_path = "\\".join(os.path.abspath(__file__).split("\\")[0:-1])  # Define the main script's path

    help_file = os.path.join(script_path, "help.txt")  # Store the help file into a file

    # Check if no argument was given
    if len(sys.argv) == 1:
        with open(help_file, "r") as f:
            print(f.read())
            sys.exit()

    os.chdir(script_path)
    try:
        os.mkdir("Outdir")
    except FileExistsError:
        pass

    # Check if an option was given
    if sys.argv[1][0] == "-":
        match sys.argv[1]:

            # If "-help" argument given then print help.txt
            case "-help":
                with open(help_file, "r") as f:
                    print(f.read())

            case "-file":
                try:
                    mod_pack = sys.argv[2]
                except IndexError:
                    print("No argument was given")
                    sys.exit()

                # Import content of the file
                with open(mod_pack, "r") as f:
                    url_list = f.readlines()
                    for url in enumerate(url_list):
                        i, val = url

                        # Check if last character is "\n", if true remove it
                        if val[-1] == "\n":
                            new_url = [x for x in val]
                            new_url.pop(-1)
                            url_list[i] = "".join(new_url)

                    install_mod(url_list)
    else:

        url_list = sys.argv
        url_list.pop(0)

        install_mod(url_list)


if __name__ == "__main__":
    main()
