# CustomAudioIntegration

> A Spotify music widget for use in livestreaming

## What *is* CustomAudioIntegration?

CAIntegration is a tool for streamers to quickly add a widget to their streams showing what they're listening to on Spotify - with features such support for showing [Spotify Codes](https://www.spotifycodes.com/) on stream, music "alerts" which only show when you change songs, and complete customisation via CSS themeing.

## How do I get started?

### From Source

#### Requirements

- Python 3.9 or higher
- A Spotify developer CLIENT_ID and CLIENT_SECRET - you can get these from [developer.spotify.com/dashboard/](https://developer.spotify.com/dashboard/)

#### Steps
1. Download / clone this repository to your computer
2. Install the requirements with `pip install -r requirements.txt` or similar
3. Copy `config.example.json` to `config.json`, and fill in the CLIENT_ID and CLIENT_SECRET 
4. Run `python main.py`
5. Follow the prompts to login to spotify
6. If you are on Linux or Mac, open a command prompt in the "web" folder and run `python3 -m http.server [port]` where port is the port you want to access your overlay on.
7. Add the overlay to OBS, or use the text files and images present in `web/` as a local overlay in OBS

## Best tips

While it's easier to make a local overlay using reading text files and reloading of images, OBS does not reload all of this at the same time, which may look odd when tracks change. As such, if you want to reload all data at once, I recommend using the web overlay, and use a custom CSS theme if you need it. 

Another strategy is to use a basic theme and wrap it inside an element within OBS. For example, if you wanted Spotify codes, you could use the basic theme and then just use an image source in OBS to load a Spotify Code on top.

## Differences between this and the non-public version

All that is removed for the public release is some themes developed by me that some streamers would prefer to keep private. An example of this is my personal streaming theme, or my friend andromacy's theme using this software. Apart from that, the actual codebase is identical!

## Future

Planned is a hosted version of this app, which you can just head to a website to use. This will be way off in the future though, as I got other things to be doing!