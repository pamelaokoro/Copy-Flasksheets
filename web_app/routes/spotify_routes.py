
import os
from spotipy import SpotifyOAuth, Spotify

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI", default="http://localhost:5000/auth/spotify/callback")

#Define scopes based on the access you need:
#SCOPE = 'user-library-read'
SCOPE = 'user-library-read playlist-read-private'

sp_oauth = SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=SCOPE, cache_path=f".cache-{CLIENT_ID}")




from flask import Blueprint, session, request, redirect, flash #, jsonify #, url_for, render_template

import functools

def spotify_authenticated_route(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        token_info = session.get('spotify_user')

        if token_info:
            print("SPOTIFY USER:", session["token_info"])

            if sp_oauth.is_token_expired(token_info):
                token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
                session['spotify_user'] = token_info

            return view(**kwargs)

        else:
            print("UNAUTHENTICATED...")
            flash("Unauthenticated. Please login!", "warning")
            return redirect("/login")
    return wrapped_view



spotify_routes = Blueprint("spotify_routes", __name__)

@spotify_routes.route('/auth/spotify/login')
def spotify_login():
    #token_info = session.get('spotify_user')
    ## If the token has expired:
    #if token_info and sp_oauth.is_token_expired(token_info):
    #    # refresh the token:
    #    token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    #    # store the user info in the session:
    #    session['spotify_user'] = token_info
    #    # show the user their playlists:
    #    return redirect("/user/playlists")
    #else:
    #    # send user to spotify and back to the callback
    #    auth_url = sp_oauth.get_authorize_url()
    #    return redirect(auth_url)

    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@spotify_routes.route('/auth/spotify/callback')
def spotify_callback():
    # get the code sent from spotify:
    code = request.args.get('code')
    # use it to authorize the user:
    token_info = sp_oauth.get_access_token(code)
    print("TOKEN:", token_info)
    # store the user info in the session:
    session['spotify_user'] = token_info
    # show the user their playlists:
    return redirect("/user/playlists")


@spotify_routes.route('/auth/spotify/logout')
def spotify_logout():
    session.pop('spotify_user', None)
    return redirect("/login")


#@spotify_authenticated_route
@spotify_routes.route("/user/playlists")
def spotify_user_playlists():
    token_info = session.get('spotify_user')

    access_token = token_info['access_token']
    sp = Spotify(auth=access_token)

    # Fetch the playlists
    results = sp.current_user_playlists(limit=10)  # Limit can be adjusted
    #playlists = [(playlist['name'], playlist['description']) for playlist in results['items']]

    # Display playlist names (simple text output)
    #return '/n'.join([f"{name}" for name, _ in playlists])

    #return results['items']
    playlist_names = [f"{playlist['name']}" for playlist in results['items']]
    return playlist_names

    #return [{
    #    "id": playlist['id'],
    #    "name": playlist['name'],
    #    "description": playlist['description']
    #} for playlist in results['items']]
