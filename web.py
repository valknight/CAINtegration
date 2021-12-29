import subprocess

from config import PORT, PLATFORM
def start_server():
    if PLATFORM == "WINDOWS":
        ws = subprocess.Popen("miniweb.exe -r web -p {}".format(PORT), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    return False
