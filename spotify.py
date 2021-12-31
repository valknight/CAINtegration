import requests
import base64
import webbrowser
import json
import click
import time
from config import debug

cacheVersion = 1
class CAIntegrationSpotifyApiWrapper():
    def __init__(self) -> None:
        if debug:
            self.base_url = "http://localhost:5000"
        else:
            self.base_url = "https://spotifyherokutest.herokuapp.com"
        auth_dict = self.readCache()
        if auth_dict is None:
            self.spotify_auth = self.pairToApi()
            self.writeCache()
        else:    
            self.spotify_auth = auth_dict
    
    @property
    def spotifyHeaderb64(self):
        return base64.b64encode(json.dumps(self.spotify_auth).encode('utf-8')).decode("utf-8")
    
    @property
    def headers(self):
        return {
            "spotify": self.spotifyHeaderb64
        }
    
    @property
    def user_info(self):
        return self.makeRequestToApi("/user/info")
    
    @property
    def playback(self):
        return self.makeRequestToApi("/user/playback")
    
    def makeRequestToApi(self, endpoint):
        url = self.base_url + endpoint
        r = requests.get(url, headers=self.headers)
        r = r.json()
        if r.get('auth'):
            if r['auth']['access_token'] != self.spotify_auth['access_token']:
                self.spotify_auth['access_token'] = r['auth']['access_token']
                self.writeCache()
            return r['data']
        return r

    def readCache(self):
        try:
            with open('.cache', 'r') as f:
                j = json.loads(f.read())
        except FileNotFoundError:
            return None
        if j.get('cacheVersion', 0) == cacheVersion:
            del j['cacheVersion']
            return j
        return None
    
    def writeCache(self):
        with open('.cache', 'w') as f:
            j = self.spotify_auth
            j['cacheVersion'] = cacheVersion
            f.write(json.dumps(j))

    def pairToApi(self):
        url = self.base_url + "/authenticate"
        click.echo("Your browser should open - if it doesn't, please go to {}".format(url))
        webbrowser.open(url)
        click.echo("Log into Spotify on this page, then enter the code displayed on the screen below")
        click.echo("The code should be " + click.style("8 characters long", fg='green', bold=True) + " with a dash in the middle")
        while True:
            code = click.prompt("Code: ")
            url = self.base_url + "/validate/{}".format(code)
            r = requests.get(url)
            if r.json().get('auth'):
                return r.json().get('auth')
            else:
                click.echo(click.style(r.json().get('error'), fg='red', bold=True) + " - please try again")

def main():
    s = CAIntegrationSpotifyApiWrapper()
    print("Logged in as {}".format(s.user_info['display_name']))
    while True:
        print("Currently listening to: {}".format(s.playback.get('item', {}).get('name', 'Nothing')))
        time.sleep(5)

if __name__ == "__main__":
    main()