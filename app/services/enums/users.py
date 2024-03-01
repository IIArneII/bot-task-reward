from enum import Enum


class Role(str, Enum):
    member = 'member'
    admin = 'admin'
