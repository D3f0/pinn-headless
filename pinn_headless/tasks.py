from typing import Union
from invoke import task, Context, Task, call, Collection
import os
import paramiko
import rich
import re
from dataclasses import dataclass, field
from functools import cached_property

@dataclass
class Partition:
    """Partition definition, corresponds to the output of blkid"""
    device: str
    LABEL: str = field(default_factory=str)
    SEC_TYPE: str = field(default_factory=str, repr=False)
    TYPE: str = field(default_factory=str)
    PARTUUID: str = field(default_factory=str, repr=False)
    # PTUUID: str = field(default_factory=str, repr=False)
    # PTTYPE: str = field(default_factory=str, repr=False)
    UUID: str = field(default_factory=str)


    @classmethod
    def from_blkid_output(cls, output: Union[str, bytes]) -> "list[Partition]":
        retval = []
        if isinstance(output, bytes):
            output = output.decode("utf-8")

        partitions: list[str] = output.splitlines()
        for blkid_partition_line in partitions:
            partition_def = {}
            device, attributes = blkid_partition_line.split(":", maxsplit=1)
            partition_def["device"] = device
            attribute_pairs = attributes.split(" ")
            for pair in attribute_pairs:
                if not pair:
                    continue
                name, value = pair.split("=")
                value = value.strip('"')
                partition_def[name] = value
            try:
                p = Partition(**partition_def)
            except TypeError: # Skip partitions that are not relevant
                continue
            retval.append(p)
        return retval

    @cached_property
    def device_name(self):
        return self.device.split("/")[-1]


def get_connection(ctx):
    """Adds a connection to the Invoke context to be used by other commands"""
    host = os.environ.get("HOST")
    user = os.environ.get("RPI_USER")
    password = os.environ.get("RPI_PASSWORD")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(
        hostname=host,
        username=user,
        password=password,
        allow_agent=False,
        look_for_keys=False,
    )
    ctx.config["ssh_client"] = client


@task(pre=[call(Task(get_connection))])
def list_partitions(ctx):

    client = ctx.config['ssh_client']
    stdin, stdout, stderr = client.exec_command("/sbin/blkid")
    partitions = Partition.from_blkid_output(stdout.read())

    breakpoint()


@task(pre=[call(Task(get_connection))])
def launch_filebrowser(ctx):
    """Runs the popular filebrowser standalone in the RPi board"""


# ns = Collection()