

import pytest

import wcf


@pytest.fixture
def conn():
    conn = wcf.API()
    return conn


def test_loaded_credentials(conn):
    assert conn.credentials is not None
    assert 'Username' in conn.credentials
    assert 'Password' in conn.credentials


def test_connect_to_database(conn):
    conn.connect()
    assert conn.token is not None
