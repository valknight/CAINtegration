let songName = null;
let songUri = null;
let artistName = null;
let albumArt = null;
let config = null;


function getJSON(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function() {
        var status = xhr.status;
        if (status === 200) {
            callback(null, xhr.response);
        } else {
            callback(status, xhr.response);
        }
    };
    xhr.send();
};

function getImg() {
    let img = document.getElementById("song-img");
    return img;
}

function getTextWrapper() {
    let text = document.getElementById("song-wrapper");
    return text;
}

function getNotif() {
    return document.getElementById("notification");
}


function showSong() {
    console.log(config);

    function finish() {
        getTextWrapper().innerHTML = generateSong();
        getNotif().classList.add("slide-in");
        if (config.doHide) {
            setTimeout(hide, config.animationDuration);
        }
    }

    function generateSong() {
        return "<div data=\"" + songName + "\" id=\"song\" class=\"song ellipsis\">" + songName + "</div><div data=\"" + artistName + "\" id=\"artist\" class=\"artist\" class=\"ellipsis\">" + artistName + "</div>"
    }

    getImg().setAttribute("src", albumArt);
    getImg().onload = finish;
}

function hide() {
    getNotif().classList.remove("slide-in");

}

function setup() {
    getJSON('/config.json?nocache=' + (new Date()).getTime(),
        function(err, data) {
            // Config data will always be avaliable now at boot
            // Here is where we want to load in the CSS theme
            config = data;
            document.getElementById("theme").setAttribute('href', '/themes/' + config.theme + '/style.css');
            const script = document.createElement('script');
            script.src = '/themes/' + config.theme + '/style.js';
            document.head.append(script);
            setInterval(loop, 1000);
        }
    )
}

function loop() {
    getJSON('/song.json?nocache=' + (new Date()).getTime(),
        function(err, data) {
            if (data == null) {
                return;
            }
            let artists = [];
            data['item']['artists'].forEach(element => {
                artists.push(element['name']);
            });
            artistName = artists.join(', ');
            songName = data['item']['name'];
            if (data['item']['album']['images'].length >= 2) {
                albumArt = data['item']['album']['images'][2]['url'];
            } else {
                albumArt = "images/default_album.png"
            }
            if (songUri != data['item']['uri']) {
                songUri = data['item']['uri'];
                showSong();
            }
        })
}

var rightJS = {
    init: function() {
        rightJS.Tags = document.querySelectorAll('.rightJS');
        for (var i = 0; i < rightJS.Tags.length; i++) {
            rightJS.Tags[i].style.overflow = 'hidden';
        }
        rightJS.Tags = document.querySelectorAll('.rightJS div');
        for (var i = 0; i < rightJS.Tags.length; i++) {
            rightJS.Tags[i].style.position = 'relative';
            rightJS.Tags[i].style.right = '-' + rightJS.Tags[i].parentElement.offsetWidth + 'px';
        }
        rightJS.loop();
    },
    loop: function() {
        for (var i = 0; i < rightJS.Tags.length; i++) {
            var x = parseFloat(rightJS.Tags[i].style.right);
            x = x + 1;
            var w = rightJS.Tags[i].scrollWidth;
            if (x > w) {
                x = -w;
            }
            if (rightJS.Tags[i].parentElement.parentElement.querySelector(':hover') !== rightJS.Tags[i].parentElement) rightJS.Tags[i].style.right = x + 'px';
        }
        requestAnimationFrame(this.loop.bind(this));
    }
};

window.addEventListener('load', rightJS.init);

setup();