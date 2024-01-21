from os import getenv
from dotenv import load_dotenv

load_dotenv()


def get_env(key: str, default="") -> str:
    value = getenv(key)
    if not value and not default:
        raise EnvironmentError(f"Environment variable {key} is not set")
    return value if value else default
