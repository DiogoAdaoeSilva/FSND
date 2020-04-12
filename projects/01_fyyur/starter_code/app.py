  #----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
from datetime import datetime

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app,db)

# TODO: connect to a local postgresql database - [DONE]

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.Text)
    genres = db.Column(db.PickleType, nullable=False)
    shows = db.relationship('Show', backref='venue', lazy=True)


    def __repr__(self):
      return f'<Venue ID: {self.id}, city: {self.city}, name: {self.name}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate - [DONE]
    # TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration. - [DONE]

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.PickleType, nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.Text)
    website = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist', lazy=True)

    def __repr__(self):
      return f'<Artist {self.id} {self.name}>'

class Show(db.Model):
  __tablename__ = 'show'

  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
  start_time = db.Column(db.DateTime)

  def __repr__(self):
    return f'<Show {self.id} {self.venue_id} {self.artist_id}>'
 

#----------------------------------------------------------------------------#
# My helper functions
#----------------------------------------------------------------------------#


def count_upcoming_shows(id):
  return Show.query.filter_by(venue_id=id).filter(Show.start_time >  datetime.now()).count()


def count_past_shows(id):
  return Show.query.filter_by(venue_id=id).filter(Show.start_time <  datetime.now()).count()

def upcoming_shows(id):
  upcoming_shows = [] 
  shows = db.session.query(Show, Artist).join(Show,Show.artist_id==Artist.id).filter(Show.venue_id==id, Show.start_time > datetime.now()).all()
  for show in shows:
    upcoming_shows.append({"artist_id": show[1].id, "artist_name": show[1].name, \
                          "artist_image_link": show[1].image_link, "start_time": (show[0].start_time).strftime("%Y-%m-%dT%H:%M:%S")})
  return upcoming_shows

def past_shows(id):
  past_shows = [] 
  shows = db.session.query(Show, Artist).join(Show,Show.artist_id==Artist.id).filter(Show.venue_id==id, Show.start_time < datetime.now()).all()
  for show in shows:
    past_shows.append({"artist_id": show[1].id, "artist_name": show[1].name, \
                          "artist_image_link": show[1].image_link, "start_time": (show[0].start_time).strftime("%Y-%m-%dT%H:%M:%S")})
  return past_shows

def past_shows_artist(id):
  past_shows = [] 
  shows = db.session.query(Show, Venue).join(Show,Show.venue_id==Venue.id).filter(Show.artist_id==id, Show.start_time < datetime.now()).all()
  for show in shows:
    past_shows.append({"venue_id": show[1].id, "venue_name": show[1].name, \
                          "venue_image_link": show[1].image_link, "start_time": (show[0].start_time).strftime("%Y-%m-%dT%H:%M:%S")})
  return past_shows



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues - [DONE]
#  ----------------------------------------------------------------


@app.route('/venues')
def venues():
  data = []
  areas = Venue.query.distinct('city','state').all()
  for area in areas:
    venues = Venue.query.filter(Venue.city == area.city, Venue.state == area.state).all()
    venues_by_area = []
    for v in venues:
      venues_by_area.append({'id': v.id, 'name': v.name, 'num_upcoming_shows': count_upcoming_shows(v.id)})
    record = {
      'city': area.city,
      'state': area.state,
      'venues': venues_by_area
    }
    data.append(record)
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. [DONE]
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term')
  venues = Venue.query.filter(Venue.name.ilike('%' + search_term + '%')).all()
  venues_count = Venue.query.filter(Venue.name.ilike('%' + search_term + '%')).count()
  data = []
  for v in venues:
    data.append({"id": v.id, "name":v.name, "num_upcoming_shows": upcoming_shows(v.id)})
  response={
    "count": venues_count ,
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id [DONE]
  venue = Venue.query.get(venue_id)
  data={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows(venue.id),
    "upcoming_shows": upcoming_shows(venue.id),
    "past_shows_count": count_past_shows(venue.id),
    "upcoming_shows_count": count_upcoming_shows(venue.id),
  }
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue - [DONE]
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    address = request.form.get('address')
    phone = request.form.get('phone')
    genres = request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link')
    website = request.form.get('website')
    if 'seeking_talent' not in request.form:
      seeking_talent = False
      seeking_description = None
    else:
      seeking_talent = True
      seeking_description = request.form.get('seeking_description')
    venue = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres, 
      facebook_link=facebook_link, seeking_talent=seeking_talent)
    db.session.add(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    flash('Venue ' + name + ' was successfully listed!', 'info')
  else:
    flash('An error occurred. Venue ' + name + ' could not be listed.')
  return render_template('pages/home.html')

  # TODO: insert form data as a new Venue record in the db, instead - [DONE]
  # TODO: modify data to be the data object returned from db insertion - [DONE]

  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead. - [DONE]
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  	

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using [DONE]
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error= False
  try:
    Show.query.filter_by(venue_id=venue_id).delete()
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    flash('Venue was deleted!', 'info')
  else:
    flash('An error occurred. Venue could not be deleted.', 'error')

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that [DONE]
  # clicking that button delete it from the db then redirect the user to the homepage
  return jsonify({ 'success': True })

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database [DONE]
  
  artists = Artist.query.all()
  data = []
  for artist in artists:
    data.append({"id": artist.id, "name": artist.name})

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. [DONE]
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term')
  artists = Artist.query.filter(Artist.name.ilike('%' + search_term + '%')).all()
  artists_count = Artist.query.filter(Artist.name.ilike('%' + search_term + '%')).count()
  data = []
  for a in artists:
    data.append({"id": a.id, "name": a.name, "num_upcoming_shows": upcoming_shows(a.id)})
  response={
    "count": artists_count ,
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artists page with the given venue_id
  # TODO: replace with real artists data from the artists table, using artist_id [DONE]
  artist = Artist.query.get(artist_id)
  data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows_artist(artist.id)
    }

  return render_template('pages/show_artist.html', artist=data)

#  Update [DONE]
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  data = Artist.query.get(artist_id)
  artist = {
  "id": data.id,
  "name": data.name,
  "genres": data.genres,
  "city": data.city,
  "state": data.state,
  "phone": data.phone,
  "website": data.website,
  "facebook_link": data.facebook_link,
  "seeking_venue": data.seeking_venue,
  "seeking_description": data.seeking_description,
  "image_link": data.image_link
  }
  form = ArtistForm(obj=data)
  # TODO: populate form with fields from artist with ID <artist_id> [DONE, called when edit button is clicked]
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing [DONE]
  # artist record with ID <artist_id> using the new attributes
  error = False
  try:
    artist = Artist.query.get(artist_id)
    artist.name = request.form.get('name')
    artist.city = request.form.get('city')
    artist.state = request.form.get('state')
    artist.phone = request.form.get('phone')
    artist.genres = request.form.getlist('genres')
    artist.facebook_link = request.form.get('facebook_link')
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    flash('Artist was successfully updated')
  else:
    flash('Artist ' + request.form['name'] + ' did not update!')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  data = Venue.query.get(venue_id)
  venue={
    "id": data.id,
    "name": data.name,
    "genres": data.genres,
    "address": data.address,
    "city": data.city,
    "state": data.state,
    "phone": data.phone,
    "website": data.website,
    "facebook_link": data.facebook_link,
    "seeking_talent": data.seeking_talent,
    "seeking_description": data.seeking_description,
    "image_link": data.image_link
  }
  form = VenueForm(obj=data)
  # TODO: populate form with values from venue with ID <venue_id> [DONE]
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing [DONE]
  # venue record with ID <venue_id> using the new attributes 
  error = False
  try:  
    venue = Venue.query.get(venue_id)
    venue.name = request.form.get('name')
    venue.genres = request.form.getlist('genres')
    venue.address = request.form.get('address')
    venue.city = request.form.get('city')
    venue.state = request.form.get('state')
    venue.phone = request.form.get('phone')
    venue.website = request.form.get('website')
    venue.facebook_link = request.form.get('facebook_link')
    venue.seeking_talent = request.form.get('seeking_talent')
    venue.seeking_description = request.form.get('seeking_description')
    venue.image_link = request.form.get('image_link')
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    flash('Venue was updated!')
  else:
    flash('Venue ' + request.form['name'] + 'was not updated')
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Artist record in the db, instead [DONE]
  # TODO: modify data to be the data object returned from db insertion  [DONE]
  error = False
  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    phone = request.form.get('phone')
    genres = request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link')

    artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, facebook_link=facebook_link)
    db.session.add(artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  # on successful db insert, flash success   
  # TODO: on unsuccessful db insert, flash an error instead. [DONE]
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  if not error:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')#
  else:
    flash('Error: Artist ' + request.form['name'] + ' was not created', 'error' )
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data. [DONE]
  #       num_shows should be aggregated based on number of upcoming shows per venue. [NOT CLEAR WHERE TO IMPLEMENT REQUIREMENT]
  shows = Show.query.all()
  data = []
  for show in shows:
    data.append({
      "venue_id": show.venue.id, 
      "venue_name": show.venue.name, 
      "artist_id": show.artist.id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": (show.start_time).strftime("%Y-%m-%dT%H:%M:%S") 
      })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead [DONE]
  error = False
  try:
    artist_id = request.form.get('artist_id')
    venue_id = request.form.get('venue_id')
    start_time = request.form.get('start_time')
    show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
    db.session.add(show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc.info())
  finally:
    db.session.close()
  if not error:
    flash('Show was successfully listed!')
  else:
    flash('An error occurred. Show could not be listed.')
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead. [DONE]
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
