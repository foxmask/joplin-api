import os
from pathlib import Path

import pytest
from dotenv import load_dotenv


@pytest.fixture
def get_token() -> str:
    """
    put the token of the Joplin WebClipper config page
    :return:
    """
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(dotenv_path=env_path, override=True, verbose=True)
    joplin_key = os.getenv("JOPLIN_KEY")
    if not joplin_key:
        raise EnvironmentError("no JOPLIN_KEY set in .env file")
    return joplin_key
