

import pytest

import wcf


@pytest.fixture
def conn():
    conn = wcf.Scraper()
    return conn


def test_name_reformat(conn):
    assert conn._reformat_name('Sweden') == 'SWE'
    assert conn._reformat_name('Czech Republic') == 'CZE'
    assert conn._reformat_name('United States of America') == 'USA'
