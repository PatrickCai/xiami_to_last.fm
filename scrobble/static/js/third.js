$(document).ready(function(){
	$("button#more").click(function(){
		url = $('p#url').text();
		window.location.href= 'http://www.patrickcai.com/me';

});
		$("button#recommendation").click(function(){
			url = $('p#url').text();
			window.open("http://www.douban.com/recommend/?url=scrobble.chom.me&title=%E8%99%BE%E7%B1%B3%E5%90%8C%E6%AD%A5last.fm", "_blank"); 
	});


});