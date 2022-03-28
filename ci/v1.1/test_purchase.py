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
    music_id = '9e1f57a0-ae0d-11ec-b909-0242ac120002'
    user_id = '9e1f57a0-ae0d-11ec-b909-0242ac125742'
    purchase_amt = 25
    update_purchase_amt = 30
    return (music_id, user_id, purchase_amt, update_purchase_amt)


def test_get_purchase(pserv, purchase_tx):
    trc, p_id = pserv.create(purchase_tx[0], purchase_tx[1], purchase_tx[2])
    assert trc == 200
    trc, music_id, user_id, timestamp, purchase_amount = pserv.read(p_id)
    assert (trc == 200 and music_id == purchase_tx[0] 
        and user_id = purchase_tx[1] and purchase_amount == purchase_tx[2])
    pserv.delete(p_id)
    # No status to check

def test_delete_purchase(mserv, song, pserv: purchase.Purchase, purchase_tx):
    trc, p_id = pserv.create(purchase_tx[0], purchase_tx[1], purchase_tx[2])
    assert trc == 200
    trc, music_id, user_id, timestamp, purchase_amount = pserv.read(p_id)
    assert (trc == 200 and music_id == purchase_tx[0] 
        and user_id = purchase_tx[1] and purchase_amount == purchase_tx[2])
    trc = pserv.delete(p_id)
    assert trc == 200

def test_update_purchase(pserv, purchase_tx):
    trc, p_id = pserv.create(purchase_tx[0], purchase_tx[1], purchase_tx[2])
    assert trc == 200
    trc1, music_id1, user_id1, timestamp1, purchase_amount1 = pserv.read(p_id)
    assert (trc1 == 200 and music_id1 == purchase_tx[0] 
        and user_id1 = purchase_tx[1] and purchase_amount1 == purchase_tx[2])
    trc, p_id = pserv.update(p_id,purchase_tx[3])
    
    trc2, music_id2, user_id2, timestamp2, purchase_amount2 = pserv.read(p_id)
    assert (trc2 == 200 and music_id2 == purchase_tx[0] 
        and user_id2 = purchase_tx[1] and purchase_amount2 == purchase_tx[3])
    pserv.delete(p_id)

def get_purchase_by_user(pserv, purchase_tx):
    trc1, p_id1 = pserv.create(purchase_tx[0], purchase_tx[1], purchase_tx[2])
    assert trc1 == 200
    trc2, p_id2 = pserv.create('123-456-789', purchase_tx[1], purchase_tx[3])
    assert trc2 == 200

    trc, u_purchases = pserv.get_purchase_by_user(purchase_tx[1])

    assert (trc == 200 and u_purchases['count'] == 2 
        and u_purchases['purchases'][0]['music_id'] == purchase_tx[0] 
        and u_purchases['purchases'][1]['music_id'] == '123-456-789')
