import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


# ------------------------
# Fonctions pour charger les données
# ------------------------
def loadClubs():
    with open('clubs.json') as c:
        return json.load(c)['clubs']
    



def loadCompetitions():
    with open('competitions.json') as comps:
        return json.load(comps)['competitions']

# ------------------------
# Initialisation de l'application
# ------------------------
app = Flask(__name__)
app.secret_key = 'something_special'

clubs = loadClubs()
competitions = loadCompetitions()

# ------------------------
# Routes
# ------------------------

@app.route('/')
def dashboard():
    """
    Page d'accueil : tableau public des clubs
    """
    return render_template('dashboard.html', clubs=clubs)

@app.route('/index')
def index():
    """
    Page de retour ou générique
    """
    return render_template('index.html', clubs=clubs)

@app.route('/showSummary', methods=['POST'])
def showSummary():
    """
    Affiche le résumé après connexion d'un club
    """
    email = request.form.get('email')
    club = next((c for c in clubs if c['email'] == email), None)  # recherche sécurisée

    if not club:
        # On reste sur la page index et on affiche le message
        return render_template('index.html', clubs=clubs, error_message="Email not found.")

    # Ajouter un flag pour indiquer si la compétition est passée
    for comp in competitions:
        comp_date = datetime.strptime(comp['date'], "%Y-%m-%d %H:%M:%S")
        comp['is_past'] = comp_date < datetime.now()

    return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs)

@app.route('/book/<competition>/<club>')
def book(competition, club):
    """
    Page de réservation d'une compétition pour un club
    """
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]

    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong - please try again")
        return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs)

@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    """
    Valide l'achat des places pour une compétition
    """
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    # Vérifications
    if int(club['points']) < placesRequired:
        flash("You don't have enough points to book these places.")
        return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs)

    if int(competition['numberOfPlaces']) < placesRequired:
        flash("Not enough places available in this competition.")
        return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs)

    if placesRequired > 12:
        flash("You cannot book more than 12 places per competition.")
        return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs)

    competition_date = datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S")
    if competition_date < datetime.now():
        flash("You cannot book places for past competitions.")
        return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs)

    # Mise à jour des points et places
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] = int(club['points']) - placesRequired

    flash(f"Booking complete! You booked {placesRequired} place(s).")
    return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs)

@app.route('/logout')
def logout():
    """
    Déconnexion : redirige vers la page dashboard
    """
    return redirect(url_for('dashboard'))


# ------------------------
# Lancement de l'application
# ------------------------
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
