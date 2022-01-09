import time
import json
import os
import sys
from typing import Tuple
import click
import spotify
import requests
import multiprocessing

from config import PORT
from web import start_server
from config import get_spotify_config, get_version

queued_alerts = []
# Main code
uri = None


def generate_spotify_code(uri):
    spotify_code_url = "https://scannables.scdn.co/uri/plain/{file_format}/{bg_color}/{color}/1280/{uri}"
    BG_COLOR, COLOR = get_spotify_config()
    formattedSvg = spotify_code_url.format(
        bg_color=BG_COLOR, color=COLOR, uri=uri, file_format="svg")
    formattedPng = spotify_code_url.format(
        bg_color=BG_COLOR, color=COLOR, uri=uri, file_format="png")
    rSvg = requests.get(formattedSvg)
    with open('web/spotify_code.svg', 'w') as f:
        f.write(rSvg.text)
    rPng = requests.get(formattedPng, stream=True)
    with open('web/spotify_code.png', 'wb') as f:
        rPng.raw.decode_content = True
        for chunk in rPng:
            f.write(chunk)
    return rSvg.text


def download_album_art(playback):
    top_image = playback['item']['album']['images'][0]['url']
    r = requests.get(top_image, stream=True)
    with open('web/album_art.png', 'wb') as f:
        r.raw.decode_content = True
        for chunk in r:
            f.write(chunk)

def main_loop(sp: spotify.CAIntegrationSpotifyApiWrapper):
    global uri
    try:
        while True:
            try:
                playback = sp.playback
                if type(playback) == dict:
                    if playback['is_playing']:
                        if playback['item']['uri'] != uri:
                            uri = playback['item']['uri']
                            # write track names for those using OBS
                            with open('web/track.txt', 'w') as f:
                                f.write(playback['item']['name'])
                            # write artist names for those using OBS
                            artists = []
                            for artist in playback['item']['artists']:
                                artists.append(artist['name'])
                            with open('web/artist.txt', 'w') as f:
                                f.write(', '.join(artists))
                            # download album art
                            download_album_art(playback)
                            # Get Spotify code
                            code = generate_spotify_code(
                                playback['item']['uri'])
                            playback['scannable_code_svg'] = code
                            with open("web/song.json", "w") as f:
                                f.write(json.dumps(playback))
                else:
                    with open("web/song.json", "w") as f:
                        f.write(json.dumps(playback))
            except ConnectionError:
                pass
            except Exception as e:
                print("An unknown error occurred!")
                print(e)
            time.sleep(1)
    except KeyboardInterrupt:
        pass

def mute():
    sys.stdout = open(os.devnull, 'w')    

def main():
    """
    Main function
    """
    try:
        click.echo(click.style("CustomAudioIntegration", fg='cyan', bold=True) +
            " | " + 
            click.style("github.com/valknight", fg='white', bold=True) +
            " | " +
            click.style("twitch.tv/VKniLive", fg='magenta', bold=True))
        click.echo(click.style("Version: {}".format(get_version()), dim=True))
        click.echo(click.style("Logging into Spotify...", dim=True))
        sp = spotify.CAIntegrationSpotifyApiWrapper()
        click.echo(click.style('Connected to server - checking versions...', dim=True))
        version_status = sp.versionStatus
        if version_status['need_to_update']:
            click.echo(click.style('Latest server version is {} - you are running {}', fg='red').format(version_status['latest'], version_status['client']))
            time.sleep(5)
        else:
            click.echo(click.style('Latest server version is {} - you do not need to update.'.format(version_status['latest']), dim=True))
        click.echo(click.style("Hiya {}!\n".format(
            sp.user_info['display_name']), fg='green', bold=True))
        p = multiprocessing.Process(target=main_loop, args=(sp,))
        p.start()
        q = multiprocessing.Process(target=start_server)
        q.start()
        time.sleep(0.6)
        print("\nYour web source for OBS is: http://127.0.0.1:{}".format(PORT))
        click.echo(click.style("Press CTRL-C to quit.", fg='black', bg='white'))
        p.join()    
    except KeyboardInterrupt:
        print("Shutting down!")
        files = [
            "song.json",
            "album_art.png",
            "spotify_code.png",
            "spotify_code.svg",
            "artist.txt",
            "track.txt",
            "config.json"
        ]
        for f in files:
            try:
                os.remove("web/{}".format(f))
                click.echo("cleaned up {}".format(f))
            except FileNotFoundError:
                click.echo("no need to cleanup {} - already deleted".format(f))
        click.echo("All done! Thanks for using CustomAudioIntegration")
        click.echo("o7 - val")
        click.pause("Press any key to quit.")
        sys.exit(0)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
