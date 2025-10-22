from server import clubs

def test_show_summary_valid_email(client):
    """Connexion avec email valide"""
    email = clubs[0]['email']
    response = client.post('/showSummary', data={'email': email})
    assert response.status_code == 200
    assert b'competitions' in response.data

def test_show_summary_invalid_email(client):
    """Connexion avec email invalide"""
    response = client.post('/showSummary', data={'email': 'fake@email.com'})
    assert response.status_code == 400
    assert b'Email not found' in response.data
