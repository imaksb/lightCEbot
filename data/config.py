from dataclasses import dataclass
from environs import Env

@dataclass
class Config:
    
    token: str
    admin_id: int
    
    @classmethod
    def from_env(cls, env):
        return cls(
            token=env.str("BOT_TOKEN"),
            admin_id=env.int("ADMIN_ID")
        )

def load_config():
    env = Env()
    env.read_env()
    return Config.from_env(env)
