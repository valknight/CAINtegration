// This script is loaded when basic.css is loaded as your theme
// Put whatever modifications you might need in code here!

window.code = undefined;

function customThemeSongChange() {
    console.log("Hi from custom theme song change!");
    if (window.code == undefined) {

        var notification = document.getElementById("notification");
        var code = document.createElement("img");
        var container = document.createElement("div");
        container.id = "spotify_code_container";
        code.id = "spotify_code";
        container.appendChild(code);
        notification.appendChild(container);
        window.code = code;
    }
    window.code.src = "spotify_code.svg?r=" + Date.now().toString();
    console.log('finished custom theme setup!');
}

function customThemeSetup() {
}

window.customThemeSongChange = customThemeSongChange;
customThemeSetup();