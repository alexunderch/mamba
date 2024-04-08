from enum import Enum


class Env(str, Enum):
    STARCRAFT = "starcraft"
    POGEMA = "pogema"


RANDOM_SEED = 23
ENV = Env.POGEMA
ENV_NAME = "Hard8x8"
