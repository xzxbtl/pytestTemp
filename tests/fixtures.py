import pytest
import pytest_asyncio
from random import randint
from httpx import AsyncClient


# ПОЗИТИВНЫЕ ТЕСТЫ
@pytest.fixture(scope='session')
def get_random_numbers_to_request():
    data = {
        "x": randint(1, 100),
        "y": randint(1, 100),
    }
    return data


@pytest.fixture(scope="session")
def api_base_url(running_app):
    host, port = running_app
    return f"http://{host}:{port}/api/"


# ПОЛУЧЕНИЕ КЛИЕНТА
@pytest_asyncio.fixture(scope="session")
async def api_client():
    async with AsyncClient() as client:
        yield client
        await client.aclose()


@pytest.fixture(scope='session')
def get_negative_numbers():
    data = {
        "x": -10,
        "y": -10,
    }
    return data


# НЕГАТИВНЫЕ ТЕСТЫ
@pytest.fixture(scope='session')
def get_incorrect_keys():
    data = {
        "x": randint(1, 100)
    }
    return data


@pytest.fixture(scope='session')
def get_largest_numbers():
    data = {
        "x": 10 ** 18,
        "y": 10,
    }
    return data


@pytest.fixture(scope='session')
def get_zero_to_division():
    data = {
        "x": randint(1, 100),
        "y": 0,
    }
    return data
