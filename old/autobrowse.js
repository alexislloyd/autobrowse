$(document).ready(function() {
	getNextLink('http://en.wikipedia.org/wiki/Special:Random')
});


function callIframe(url, callback) {

    $('iframe#browser').load(function() {
        var url= $(this).contentWindow.location.href;
        console.log("url = "+url)
        //getNextLink(url)
    });
}

function getNextLink(url) {
	$.get( url, function( data ) {
		var html = data;
		console.log(html)
	});
}