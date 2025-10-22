from server import clubs, competitions
from datetime import datetime, timedelta

def test_purchase_success(client):
    club = clubs[0]
    competition = competitions[0]

    club['points'] = 15
    competition['numberOfPlaces'] = 20
    competition['date'] = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")

    response = client.post('/purchasePlaces', data={
        'club': club['name'],
        'competition': competition['name'],
        'places': 3
    })
    assert b"Booking complete" in response.data


def test_purchase_not_enough_points(client):
    club = clubs[0]
    competition = competitions[0]
    club['points'] = 2
    competition['numberOfPlaces'] = 10
    competition['date'] = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")

    response = client.post('/purchasePlaces', data={
        'club': club['name'],
        'competition': competition['name'],
        'places': 5
    })
    assert b"enough points" in response.data


def test_purchase_not_enough_places(client):
    club = clubs[0]
    competition = competitions[0]
    club['points'] = 30
    competition['numberOfPlaces'] = 2
    competition['date'] = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")

    response = client.post('/purchasePlaces', data={
        'club': club['name'],
        'competition': competition['name'],
        'places': 5
    })
    assert b"Not enough places" in response.data


def test_purchase_past_competition(client):
    club = clubs[0]
    competition = competitions[0]
    club['points'] = 10
    competition['numberOfPlaces'] = 10
    competition['date'] = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")

    response = client.post('/purchasePlaces', data={
        'club': club['name'],
        'competition': competition['name'],
        'places': 2
    })
    assert b"past competitions" in response.data


def test_purchase_more_than_12(client):
    club = clubs[0]
    competition = competitions[0]
    club['points'] = 40
    competition['numberOfPlaces'] = 50
    competition['date'] = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")

    response = client.post('/purchasePlaces', data={
        'club': club['name'],
        'competition': competition['name'],
        'places': 15
    })
    assert b"more than 12" in response.data

