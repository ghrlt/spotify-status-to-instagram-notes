from flask import Flask, request, make_response, redirect
import urllib.parse
import threading
import requests
import logging
import base64
import json
import sys
import os

import env


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class Client:
    def __init__(self):
        self.session_file_path = f"{env.WORKING_DIRECTORY_PATH}/spotify.session"

        self.lastError = None

        self.refreshSession()

    def login(self):
        if self.access_token:
            try:
                self.getUser()
            except Exception as e:
                print(e)
                self.refreshToken()

        else:
            self.authorize()

        print("Spotify | Successfully logged in as", self.getUser()['display_name'])

    def authorize(self):
        self.oauth = OauthServer()
        threadEvent = threading.Event()
        oauthThread = threading.Thread(target=self.oauth.run, args=(threadEvent,), daemon=True)
        oauthThread.start()

        print("Open the following URL in your browser:", "http://"+self.oauth.host+":"+self.oauth.port+"/authorize")

        threadEvent.wait()
        #TODO: Find a proper way to stop the flask server...

        #~ Fix the stdout once the thread is done
        sys.stdout = sys.__stdout__

        #~ Check the OAuth process went well
        if self.oauth.status.get('success') != True:
            raise Exception(f"Something went wrong during the OAuth process. Result: {self.oauth.status}")
        
        #~ Refresh the session
        self.refreshSession()

    def refreshToken(self):
        authHeader = base64.b64encode(f"{env.SPOTIFY_CLIENT_ID}:{env.SPOTIFY_CLIENT_SECRET}".encode('utf-8'))
        
        r = requests.post(
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token
            },
            headers={
                "Authorization": f"Basic {authHeader.decode('utf-8')}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
        if r.status_code != 200:
            raise Exception(f"Unable to refresh the access token. Result: {r.json()}")
        
        data = r.json()
        self.refreshSession(**data)

    def refreshSession(self, **kwargs):
        if kwargs:
            if kwargs.get('access_token'):
                self.access_token = kwargs['access_token']
            if kwargs.get('refresh_token'):
                self.refresh_token = kwargs['refresh_token']
            if kwargs.get('expires_in'):
                self.expires_in = kwargs['expires_in']
            if kwargs.get('scope'):
                self.scope = kwargs['scope']

            with open(self.session_file_path, "w") as f:
                json.dump({
                    "access_token": self.access_token,
                    "refresh_token": self.refresh_token,
                    "expires_in": self.expires_in,
                    "scope": self.scope
                }, f)
        else:
            with open(self.session_file_path, "r") as f:
                settings = json.load(f)
            
            self.refreshSession(**settings)


    def getUser(self):
        r = self.apiRequest("GET", "/me").json()
        return r
    
    def getCurrentPlayback(self):
        r = self.apiRequest("GET", "/me/player").json()
        return r


    def apiRequest(self, method: str, endpoint: str, params: dict={}, data: dict|str=None):
        r = requests.request(
            method,
            f"https://api.spotify.com/v1{endpoint}",
            params=params,
            data=data,
            headers={
                "Authorization": f"Bearer {self.access_token}"
            }
        )
        if r.status_code == 401:
            if self.lastError == 401:
                raise Exception("Invalid access token. Unable to refresh it. Please re-authorize the app (delete spotify.session).")

            self.lastError = 401
            self.refreshToken()
            return self.apiRequest(method, endpoint, params, data)
        
        elif r.status_code == 204:
            r.json = lambda: {}

        self.lastError = None
        return r



class OauthServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.host = 'localhost'
        self.port = '1811'
        self.debug = False #env.isDevelopment()

        self.session_file_path = f"{env.WORKING_DIRECTORY_PATH}/spotify.session"

    def run(self, threadEvent: threading.Event):
        @self.app.route('/authorize')
        def authorize():
            return self.authorize()
        
        @self.app.route('/callback')
        def callback():
            return self.callback()
        
        self.threadEvent = threadEvent

        #~ Prevent Flask from printing in the console
        sys.stdout = open(os.devnull, 'w')

        self.app.run(
            host=self.host,
            port=self.port,
            debug=self.debug
        )

    def authorize(self):
        self.state = os.urandom(16).hex()
        self.scope = env.SPOTIFY_CLIENT_SCOPE

        resp = make_response(
            redirect(
                "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode({
                    "client_id": env.SPOTIFY_CLIENT_ID,
                    "response_type": "code",
                    "redirect_uri": f"{env.SPOTIFY_CLIENT_REDIRECT_URI}/callback",
                    "scope": self.scope,
                    "state": self.state
                })                
            )
        )
        return resp

    def callback(self):
        args = request.args
        code = args.get('code')
        state = args.get('state')

        if state != self.state:
            return self.quit({"error": "state_mismatch"})


        if not code:
            return self.quit({"error": args.get('error')})


        
        authHeader = base64.b64encode(
            f"{env.SPOTIFY_CLIENT_ID}:{env.SPOTIFY_CLIENT_SECRET}".encode('utf-8')
        )
        r = requests.post(
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": f"{env.SPOTIFY_CLIENT_REDIRECT_URI}/callback",
            },
            headers={
                "Authorization": f"Basic {authHeader.decode('utf-8')}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
        if r.status_code != 200:
            return self.quit({"error": r.json(), "status_code": r.status_code})
        
        data = r.json()
        self.access_token = data.get('access_token')
        self.refresh_token = data.get('refresh_token')
        self.expires_in = data.get('expires_in')
        self.scope = data.get('scope')

        with open(self.session_file_path, "w") as f:
            json.dump({
                "access_token": self.access_token,
                "refresh_token": self.refresh_token,
                "expires_in": self.expires_in,
                "scope": self.scope
            }, f)

        return self.quit({"success": True})

    def quit(self, data: dict):
        self.status = data
        self.threadEvent.set()

        return data
