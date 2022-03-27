"""
Test the purchase apis.

These tests are invoked by running `pytest` with the
appropriate options and environment variables, as
defined in `conftest.py`.
"""

# Standard libraries

# Installed packages
import pytest

# Local modules
import purchase
import music

@pytest.fixture
def mserv(request, music_url, auth):
    return music.Music(music_url, auth)


@pytest.fixture
def song(request):
    # Recorded 2022
    return ('Dharun Kumar', 'My Family')

@pytest.fixture
def user(request):
    return ('Bangani', 'Hiren', 'hiren_naresh_bangani@sfu.ca')

@pytest.fixture
def pserv(request, purchase_url, auth):
    return purchase.Purchase(purchase_url, auth)


@pytest.fixture
def purchase_tx(request):
    # Purchase amount $50
    music_id = ''
    user_id = ''
    purchase_amt = 25
    return (music_id, user_id, purchase_amt)


def test_get_purchase(pserv, purchase_tx):
    # Original recording, 1952
    orig_artist = 'Big Mama Thornton'
    trc, p_id = pserv.create('', '', purchase_tx[0], purchase_tx[1])
    assert trc == 200
    trc, music_id, user_id, timestamp, purchase_amount = pserv.read(p_id)
    assert (trc == 200 and timestamp == purchase_tx[0] and purchase_amount == purchase_tx[1])
    pserv.delete(p_id)
    # No status to check

def test_delete_purchase(mserv, song, pserv: purchase.Purchase, purchase_tx):
    trc, p_id = pserv.create(purchase_tx[0], purchase_tx[1], purchase_tx[2])
    assert trc == 200
    trc, music_id, user_id, timestamp, purchase_amount = pserv.read(p_id)
    assert (trc == 200 and timestamp == purchase_tx[0] and purchase_amount == purchase_tx[1])
    trc = pserv.delete(p_id)
    assert trc == 200


# @pytest.fixture
# def song_oa(request):
#     # Recorded 1967
#     return ('Aretha Franklin', 'Respect')


# @pytest.fixture
# def m_id_oa(request, pserv, song_oa):
#     trc, m_id = pserv.create(song_oa[0], song_oa[1])
#     assert trc == 200
#     yield m_id
#     # Cleanup called after the test completes
#     pserv.delete(m_id)


# def test_orig_artist_oa(pserv, m_id_oa):
#     # Original recording, 1965
#     orig_artist = 'Otis Redding'
#     trc = pserv.write_orig_artist(m_id_oa, orig_artist)
#     assert trc == 200
#     trc, oa = pserv.read_orig_artist(m_id_oa)
#     assert trc == 200 and oa == orig_artist


# def test_full_cycle(pserv):
#     # `pserv` is an instance of the `Purchase` class

#     # Performance at 2010 Vancouver Winter Olympics
#     song = ('k. d. lang', 'Hallelujah')
#     # Soundtrack of first Shrek film (2001)
#     orig_artist = 'Rufus Wainwright'
#     # Original recording from album "Various Positions" (1984)
#     orig_orig_artist = 'Leonard Cohen'

#     # Create a purchase record and save its id in the variable `m_id`
#     # ... Fill in the test ...
#     trc, m_id = pserv.create(song[0], song[1], orig_artist)
#     assert trc == 200
#     # trc, artist, title, oa = pserv.read(m_id)
#     # assert (trc == 200 and artist == song[0] and title == song[1]
#     #         and oa == orig_artist)

#     trc = pserv.write_orig_artist(m_id, orig_orig_artist)
#     assert trc == 200
#     trc, artist, title, oa = pserv.read(m_id)
#     assert (trc == 200 and artist == song[0] and title == song[1]
#             and oa == orig_orig_artist)

#     # The last statement of the test
#     pserv.delete(m_id)
