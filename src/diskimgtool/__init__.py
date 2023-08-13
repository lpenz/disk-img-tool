#!/usr/bin/env python3
# Copyright (C) 2023 Leandro Lisboa Penz <lpenz@lpenz.org>
# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.


import logging
import os
import re
import subprocess
import tempfile
from contextlib import contextmanager
from time import sleep


def log():
    if not hasattr(log, "logger"):
        log.logger = logging.getLogger(os.path.basename("diskimgtool"))
    return log.logger


def run(cmd, check=True, capture=False):
    log().info(f'+ {" ".join(cmd)}')
    return subprocess.run(cmd, check=check)


def run_capture(cmd, check=True, capture=False):
    log().info(f'+ {" ".join(cmd)}')
    return subprocess.check_output(cmd, encoding="ascii")


@contextmanager
def chdir(path):
    log().info(f"+ cd {path}")
    cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        log().info("+ cd -")
        os.chdir(cwd)


@contextmanager
def loopback_setup(image):
    data = run_capture(["kpartx", "-a", "-v", image])
    for line in data.split("\n"):
        if line:
            log().info(f"  {line}")
    try:
        m = re.search(r"add map (loop[0-9]+)p.*", data)
        if not m:
            raise Exception("regex didnt match")
        loop = f"/dev/mapper/{m.group(1)}"
        yield loop
    finally:
        run(["kpartx", "-d", image], check=False)
        run(["sync"])


@contextmanager
def mount(src, dst, t="auto", bind=False, args=None):
    if bind:
        t = "none"
    c = ["mount", "-t", t]
    if bind:
        c.extend(["-o", "bind"])
    if args:
        c.extend(args)
    c.extend([src, dst])
    run(c)
    try:
        yield
    finally:
        for i in range(5):
            r = run(["umount", dst], check=False)
            if r.returncode == 0:
                return
            run(["lsof", dst], check=False)
            sleep(1)
        run(["umount", "-l", dst])


@contextmanager
def root_mounts(rootdir):
    with mount("dev", f"{rootdir}/dev", t="devtmpfs"):
        with mount("devpts", f"{rootdir}/dev/pts", t="devpts"):
            with mount("tmpfs", f"{rootdir}/dev/shm", t="tmpfs"):
                with mount("proc", f"{rootdir}/proc", t="proc"):
                    with mount("sysfs", f"{rootdir}/sys", t="sysfs"):
                        with mount("tmpfs", f"{rootdir}/run", t="tmpfs"):
                            dirs = [f"{rootdir}/run/lock", f"{rootdir}/run/shm"]
                            run(["mkdir", "-p"] + dirs)
                            yield


def chroot(rootdir, cmd):
    cmd = ["chroot", rootdir] + cmd
    return run(cmd)


@contextmanager
def image_fully_mounted(image):
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as rootdir:
        with loopback_setup(image) as loop:
            with mount(f"{loop}p2", rootdir):
                with mount(f"{loop}p1", f"{rootdir}/boot"):
                    yield rootdir
