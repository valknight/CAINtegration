# CustomAudioIntegration

> A Spotify music widget for use in livestreaming

## What *is* CustomAudioIntegration?

CAIntegration is a tool for streamers to quickly add a widget to their streams showing what they're listening to on Spotify - with features such support for showing [Spotify Codes](https://www.spotifycodes.com/) on stream, music "alerts" which only show when you change songs, and complete customisation via CSS themeing.

## How do I get started?

### From Source

#### Requirements

- Python 3.9 or higher

#### Steps
1. Download / clone this repository to your computer
2. Install the requirements with `pip install -r requirements.txt` or similar
3. Copy `config.example.json` to `config.json`, and modify as you see fit

* You may also wish to modify the config.json inside the web folder - this controls the theme in use, and if we hide or not *

4. Run `python main.py`
5. Follow the prompts to login to spotify
6. If you are on Linux or Mac, open a command prompt in the "web" folder and run `python3 -m http.server [port]` where port is the port you want to access your overlay on.
7. Add the overlay to OBS, or use the text files and images present in `web/` as a local overlay in OBS

## Best tips

While it's easier to make a local overlay using reading text files and reloading of images, OBS does not reload all of this at the same time, which may look odd when tracks change. As such, if you want to reload all data at once, I recommend using the web overlay, and use a custom CSS theme if you need it. 

Another strategy is to use a basic theme and wrap it inside an element within OBS. For example, if you wanted Spotify codes, you could use the basic theme and then just use an image source in OBS to load a Spotify Code on top.

## Differences between this and the non-public version

All that is removed for the public release is some themes developed by me that some streamers would prefer to keep private. An example of this is my personal streaming theme, or my friend andromacy's theme using this software. Apart from that, the actual codebase is identical!

## Privacy

When you use this app, you connect to a server I host using Heroku that will act as a middle service between your computer and the Spotify API. This is done for two reasons:

1. Avoid users having to setup their own Spotify applications and client secrets
2. Assist in future plans to develop an entirely hosted version of this application

This web server does **not** log your playback history. The data stored includes:

### Linking code requests

This includes the creation and validation of linking codes, and monitoring of incorrect attempts. This data is attributed to an IP address, to help identify potential attackers. 

This is logged to a standard log file.
### IP addresses

As per above, I log IP addresses to help with monitoring abuse and potential attackers. This data will not be sold.

### Spotify IDs

We use Spotify IDs to ensure one Spotify account does not have multiple linking codes active.

When a new successful link is made, the Spotify ID associated is logged. This is stored alongside the IP address, and the linking code used. This again is to monitor abuse - for example, one IP address linking to many different Spotify IDs. No other information from your Spotify account is logged.

## What we don't store

Once a link is made, any tokens from my database. Tokens are then stored on your computer, and are sent as encoded base 64 during requests. 

Our scopes only allow me to see your playback data and your user info (which is used to show your name & other info when linking and when launching the application). Again, I do not log or store this playback or user info.

In the future, if I were to move to an entirely hosted version of this application, we may store tokens on the server side. However, until that point the current model works find for CustomAudioIntegration.

## Thanks

Big thanks to the libraries:
- click
- requests

And, on our server side:
- flask
- gunicorn

## Future

Planned is a hosted version of this app, which you can just head to a website to use. This will be way off in the future though, as I got other things to be doing!