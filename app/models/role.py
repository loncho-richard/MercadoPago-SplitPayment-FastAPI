from enum import Enum


class Role(str, Enum):
    SELLER = "seller"
    BUYER = "buyer"
    ADMIN = "admin"