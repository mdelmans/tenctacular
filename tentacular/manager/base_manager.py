from typing import Optional, TypeVar, Generic

from abc import ABC, abstractmethod

class Firmware(ABC):
    @abstractmethod
    def get_name(self);
        return

    @abstractmethod
    def get_source(self):
        return

    # @classmethod
    # @abstractmethod
    # def find(cls, name):
    #     return

class Device(ABC):
    @abstractmethod
    def get_uuid(self):
        return

    @abstractmethod
    def get_config(self):
        return

    @classmethod
    @abstractmethod
    def devices(cls):
        return

    # @classmethod
    # @abstractmethod
    # def find(cls, uuid):
    #     return

    @abstractmethod
    def get_firmware_name(self):
        return

    def __str__(self):
        return f"{self.get_conf()}:{self.get_uuid()}"

D = TypeVar('DeviceType') 

class Manager(ABC, Generic[D], Generic[F]):
    def __init__(self, host, port, database, username, password):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password

    @abstractmethod
    def connect(self):
        """Connect to the database
        Establish a connection to the database.
        """
        return

    @abstractmethod
    def add_device(self, firmware:F)->D:
        """Add device
        Add a new device with a given config.
        Returns a new device object.
        """
        return

    @abstractmethod
    def get_device(self, uuid:str)->Optional[D]:
        return

    @abstractmethod
    def get_firmware(self, name:str)->Optional[F]:
        return


