#! python3

import hashlib
import os
import time
import sys
import shutil
import tomllib as toml


def make_ansi_delete_code(lines: int):
    up = "\033[A"
    clear_line = "\033[2K"
    return (up + clear_line) * (lines + 1)


def main() -> None:
    with open("./minecraft.toml", "rb") as config_file:
        config = toml.load(config_file)

    jar_dirs = ["bin", "plugins"]
    for dirname in jar_dirs:
        os.makedirs(dirname, exist_ok=True)

    # MAKE PRINTABLE TEXT
    text_map = {}
    for dir in jar_dirs:
        for name, info in config[dir].items():
            path = f"{dir}/{name}.jar"
            text_map[path] = {
                "url": info["url"],
                "hash": info["hash"],
                "valid": False,
            }

    # WAITING FOR VALID FILES
    path_align: int = max(len(key) for key in text_map.keys())
    ansi_delete = make_ansi_delete_code(len(text_map.keys()))

    def check_hashes():
        for path, info in text_map.items():
            if not os.path.isfile(path):
                continue
            with open(path, "rb") as jar:
                local_hash = hashlib.sha256(jar.read()).hexdigest()
                if local_hash == info["hash"]:
                    text_map[path]["valid"] = True

    check_hashes()
    while not all(info["valid"] for info in text_map.values()):
        for path, info in text_map.items():
            status = info["url"] if not info["valid"] else "OK"
            print(f"{path.ljust(path_align)} :: {status}")
        sys.stdout.flush()

        check_hashes()
        time.sleep(5)

        print(ansi_delete)
        sys.stdout.flush()

    # COPYING FILES
    build_dir = "./build"
    shutil.rmtree(build_dir, ignore_errors=True)
    shutil.copytree("./config", build_dir, dirs_exist_ok=True)
    shutil.copytree("./bin", build_dir, dirs_exist_ok=True)
    shutil.copytree("./plugins", f"{build_dir}/plugins", dirs_exist_ok=True)

    # GENERATE START SCRIPT
    java_flags = " ".join(config["java"]["flags"])
    game_flags = " ".join(config["game"]["flags"])
    game_bin = config["game"]["main_jar"]
    script = f"#! /bin/sh\nexec java {java_flags} -jar {game_bin} {game_flags}\n"
    with open(f"{build_dir}/start.sh", "wt") as script_file:
        script_file.write(script)


if __name__ == "__main__":
    main()
