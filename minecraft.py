#! python3

# ruff: noqa

from typing import Never, TypeAlias

import hashlib
import os
import pathlib
import logging
import random
import time
from datetime import datetime, timedelta
import urllib.request as request
import tomllib as toml


MissingJars: TypeAlias = dict[str, list[str]]
TIME_ONLY = "%H:%M:S"


def log(message):
    """Logging utility"""
    logging.debug(message)
    print(message)


def download_jars(config: dict, key: str, missing: list[str] = []) -> Never | None:
    """
    :param config Parsed TOML config dictionary
    :param key    Key holding downloadable jar info (dict of dicts)
    """
    for basename, info in config[key].items():
        path = f"./{key}/{basename}.jar"

        if len(missing) > 0 and basename not in missing:
            log(f"File {path} doesn't need to be downloaded, skipping")
            continue

        log(f"Downloading data for {basename}")
        start = datetime.now()
        with (
            # request.urlopen(info["url"]) as jar_data,
            open(path, "wb") as jar_file
        ):
            finish = datetime.now()
            # data = jar_data.read()
            data = bytes()
            log(
                f"Successfully downloaded data for {basename}, "
                f"took {(finish - start).total_seconds()} seconds"
            )
            data_hash = hashlib.sha256(data).hexdigest()
            if data_hash.strip() != info["hash"].strip():
                log(f"Downloaded data's hash for '{basename}' is invalid, skipping")
                continue
            jar_file.write(data)
        wait_time = random.randint(5, 15)
        now = datetime.now()
        next = now + timedelta(minutes=wait_time)
        log(
            f"Waiting {wait_time} minutes before downloading next file. "
            f"Now: {now.strftime(TIME_ONLY)}, Download start: {next.strftime(TIME_ONLY)}"
        )
        time.sleep(wait_time * 60)


def check_jars(config: dict, keys: list[str]) -> MissingJars:
    """Check files and hashes validity.
    :param  config Parsed TOML config
    :param  keys   Keys to check for downloadable jar info
    :return List of key-value pair tuples that point to jars that must be redownloaded
    """
    must_redownload = {k: [] for k in keys}
    for dir in keys:
        jars = list(pathlib.Path(dir).glob("*.jar"))
        config_keys = [jar.stem for jar in jars]
        for key, path in zip(config_keys, jars):
            if not os.path.exists(path):
                log(f"File {path} doesn't exists. Flagging for download")
                must_redownload[dir].append(key)
                continue

            with path.open("rb") as file:
                data = file.read()
                if len(data) == 0:
                    log(f"File {path} exists but has no data. Flagging for download")
                    must_redownload[dir].append(key)
                    continue

                local_file_hash = hashlib.sha256(data).hexdigest()
                expected_hash = config[key]["hash"]
                if local_file_hash != expected_hash:
                    log(f"File {path} has an invalid hash. Flagging for download")
                    must_redownload[dir].append(key)
                    continue

            log(f"File {path} is valid")

    return must_redownload


def prepare() -> None:
    logging.basicConfig(
        filename="./minecraft.log",
        encoding="utf-8",
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s:%(funcName)s %(message)s",
    )

    with open("./minecraft.toml", "rb") as config_file:
        config = toml.load(config_file)

    jar_dirs = ["bin", "plugins"]
    for dirname in jar_dirs:
        os.makedirs(dirname, exist_ok=True)
    to_download = check_jars(config, jar_dirs)
    print(to_download)
    for dirname in jar_dirs:
        download_jars(config, dirname, to_download[dirname])


if __name__ == "__main__":
    prepare()
