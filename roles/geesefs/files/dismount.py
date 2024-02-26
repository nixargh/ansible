#!/bin/env python3
"""Do umount of FUSE mountpoint."""

import sys
import argparse
import logging

from subprocess import run, CalledProcessError

NAME = "dismount"
VERSION = "0.1.0"
MOUNTS = "/proc/mounts"

LOG = logging.getLogger(NAME)


def configure_logger(log_level="info"):
    """Configure root logger.

    :type log_level: str
    :param log_level: (Optional) Logging level. Default is INFO.
    """
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))

    formatter = logging.Formatter(
        "%(asctime)s %(process)-8d %(name)-25s "
        "%(levelname)-8s %(message)s")

    std_handler = logging.StreamHandler(sys.stdout)
    std_handler.setFormatter(formatter)
    std_handler.set_name("stdout")
    logger.addHandler(std_handler)

    return logger


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog=NAME,
        description='Dismount usage: ')

    parser.add_argument(
        '-s', '--service',
        metavar='SERVICE',
        required=True,
        help='Service name keeping mount point')
    parser.add_argument(
        '-m', '--mountpoint',
        metavar='DIRECTORY',
        required=True,
        help='Mount point directory')
    parser.add_argument(
        '-L', '--loglevel',
        type=str,
        choices=[
            'debug',
            'info',
            'warning',
            'error',
            'critical'],
        default='info',
        help='Log level (default is "info")')
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=VERSION,
        help='Show version')

    return parser.parse_args()


def _mounted(mountpoint):
    LOG.info("Checking whether mount point is mounted: '%s'.", mountpoint)
    mounts = []
    with open(MOUNTS, "r", encoding="utf8") as mounts_obj:
        mounts = mounts_obj.readlines()

    for mount in mounts:
        if mount.rstrip().split(" ")[1] == mountpoint:
            LOG.warning("Found mounted mount point: '%s'.", mount)
            return True

    LOG.info("Mount point isn't found at '%s'.", MOUNTS)
    return False


def _service(name, action):
    if action not in ["stop", "start"]:
        LOG.error("Unsupported actions: '%s.")
        sys.exit(2)

    LOG.info("Do '%s' on service: '%s'.", action, name)
    if not _shell_run(["systemctl", action, name]):
        LOG.error("Failed to %s service: '%s'.", action, name)
        sys.exit(1)


def _umount(mountpoint):
    LOG.info("Do umount for mount point: '%s'.", mountpoint)
    if not _shell_run(["umount", mountpoint]):
        LOG.error("Failed to umount: '%s'.", mountpoint)
        return False
    return True


def _shell_run(args):
    try:
        run(args, check=True)
    except CalledProcessError as error:
        LOG.error("Error: %s.", error)
        return False
    return True


def main():
    """Entry point."""

    args = parse_args()
    configure_logger(log_level=args.loglevel)

    LOG.info("Starting Dismount (v%s).", VERSION)
    LOG.debug("Command line arguments: %s.", args)

    umount_result = True
    if _mounted(args.mountpoint):
        if not _umount(args.mountpoint):
            _service(args.service, "stop")
            umount_result = _umount(args.mountpoint)
            _service(args.service, "start")

    if umount_result:
        LOG.info("Dismount finished successfully.")
        sys.exit(0)

    LOG.info("Dismount failed.")
    sys.exit(1)


if __name__ == "__main__":
    main()
