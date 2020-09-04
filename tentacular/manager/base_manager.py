import re

from ampy.pyboard import Pyboard
from ampy.files import Files

from typing import TypeVar, Generic
from abc import ABC, abstractmethod


D = TypeVar('DeviceType')
F = TypeVar('FiirmwareType')


class Firmware(ABC):
    @abstractmethod
    def get_source(self):
        return


class Device(ABC, Generic[F]):
    @abstractmethod
    def get_uid(self):
        return

    @abstractmethod
    def set_firmware(self, firmware: F):
        return

    def __str__(self):
        return f"{self.get_firmware().get_name()}:{self.get_uid()}"


class Manager(ABC, Generic[D, F]):

    def __init__(self, port, baudrate):
        self.board = Pyboard(port, baudrate, rawdelay=1)
        self.board_files = Files(self.board)

    @abstractmethod
    def log_info(self, message: str):
        return

    def flash_device(self, device: D, firmware: F):
        uid = None

        try:
            uid = self.board_files.get('/flash/uid').decode()
        except Exception:
            pass

        if uid is not None:
            ureg = re.match(
                "^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}"
                "-[0-9a-f]{12}$",
                uid
            )
            if ureg:
                uid = ureg[0]
            else:
                uid = None

        if uid is not None and uid != device.get_uid():
            raise Exception("UUID mismatch")

        if uid is None:
            self.board_files.put('/flash/uid', device.get_uid())

        self.log_info("Uploading tentacle library...")
        with open('flash/tentacle.py') as lib_file:
            self.board_files.put('/flash/tentacle.py', lib_file.read())

        self.log_info("Uploading bootloader...")
        with open('flash/boot.py') as boot_file:
            self.board_files.put('/flash/boot.py', boot_file.read())

        self.log_info("Uploading source...")
        source_file = firmware.get_source()
        self.board_files.put('/flash/main.py', source_file)

        device.set_firmware(firmware)
