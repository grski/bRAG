from enum import StrEnum

DEFAULT_NUMBER_OF_WORKERS_ON_LOCAL = 1


class Environments(StrEnum):
    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"
