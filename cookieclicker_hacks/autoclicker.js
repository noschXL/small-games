var autoclicker = setInterval(function(){
	Game.lastClick -= 1000;
	cookie = document.getElementById('bigCookie');
	cookie.click();
}, 1)