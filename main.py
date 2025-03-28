import os, sys, json, shutil, platform
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
            r = rq.get(url)
        except Exception:
            input(download_error)
            sys.exit()

        str_data = str(r.content)
        if str_data[2] == "K":
            extension = ".zip"

        elif str_data[2] == "R":
            extension = ".rar"

        elif str_data[2] == "7":
            extension = ".7z"

        mod_path = os.path.join(script_path, f"mod{extension}")

        with open(mod_path, "wb") as f:
            f.write(r.content)
        print("Download complete!")

        print("Extracting..")

        os.chdir(script_path)

        if not os.path.exists("outdir"):
            os.mkdir("outdir")

        try:
            Archive(mod_path).extractall("outdir")
        except Exception:
            input(extract_error)
            sys.exit()

        os.chdir("outdir")

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
        shutil.rmtree("outdir")
        os.remove(mod_path)

        print(f"{Fore.YELLOW}{i + 1} mod installed out of {len(mod_list)}.")


def main():
    init(autoreset=True)
    if platform.system() == "Windows":
        os.system("cls")

    global target_path, script_path

    local = ""

    if platform.system() == "Windows":
        local = os.environ["APPDATA"]

    elif platform.system() == "Linux":
        local = os.path.join(os.environ["HOME"], ".local/share")

    target_path = os.path.join(local, "Sonic3AIR/mods")

    script_path = ""

    if platform.system() == "Windows":
        script_path = "\\".join(os.path.realpath(__file__).split("\\")[0:-1])
    elif platform.system() == "Linux":
        script_path = "/".join(os.path.realpath(__file__).split("/")[0:-1])
    else:
        print(f"{Fore.RED}Error: Operating system not supported.")
        sys.exit()

    help_file = os.path.join(script_path, "help.txt")

    if len(sys.argv) == 1:
        with open(help_file, "r") as f:
            print(f.read())
            sys.exit()

    os.chdir(script_path)
    try:
        os.mkdir("outdir")
    except FileExistsError:
        pass

    if sys.argv[1][0] == "-":

        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            with open(help_file, "r") as f:
                print(f.read())

        if sys.argv[1] == "--file" or "-f":
            try:
                mod_pack = sys.argv[2]
            except IndexError:
                print("No argument was given")
                sys.exit()

            with open(mod_pack, "r") as f:
                url_list = f.readlines()
                for url in enumerate(url_list):
                    i, val = url

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
