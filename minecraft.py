#! python3

# ruff: noqa

from typing import Never

import hashlib
import os
import logging
import random
import time
from datetime import datetime, timedelta
import urllib.request as request
import tomllib as toml


TIME_ONLY = "%H:%M:S"


def log(message):
    """Logging utility"""
    logging.debug(message)
    print(message)


def download_jars(config: dict, key: str) -> Never | None:
    """
    :param config Parsed TOML config dictionary
    :param key    Key holding downloadable jar info (dict of dicts)
    """
    for basename, info in config[key].items():
        path = f"./{key}/{basename}.jar"
        log(f"Downloading data for {basename}")
        start = datetime.now()
        with request.urlopen(info["url"]) as jar_data, open(path, "wb") as jar_file:
            finish = datetime.now()
            data = jar_data.read()
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
    for dirname in jar_dirs:
        download_jars(config, dirname)


if __name__ == "__main__":
    prepare()
