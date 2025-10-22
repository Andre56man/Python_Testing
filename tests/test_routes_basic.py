def test_dashboard_page(client):
    """Page d'accueil accessible"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Club' in response.data or b'clubs' in response.data

def test_index_page(client):
    """Page index accessible"""
    response = client.get('/index')
    assert response.status_code == 200

def test_logout_redirect(client):
    """Déconnexion redirige vers le tableau"""
    response = client.get('/logout')
    assert response.status_code == 302  # redirection
    assert '/' in response.location

def test_welcome_page(client):
    """page de welcome"""
    response = client.get('/welcome')
