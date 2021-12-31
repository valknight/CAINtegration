import subprocess
ffplay_path = "C:\\ffmpeg\\bin\\ffplay.exe"

def play_song(name):
    subprocess.check_call("{} -loglevel quiet -nodisp -autoexit {}".format(ffplay_path, name), stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL)