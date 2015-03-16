$(document).ready(function() {

	$('iframe#browser').load(function() {
        setTimeout('getNext()', 1000);
    });
	
})

function getNext() {
	//var url = $('#my_url').val()
	console.log("getting next for " + url)
	$.get( '/?url='+url, function( data ) {
		var json = jQuery.parseJSON(data);
		console.log("attempting redirect to " + json.url);
		$('iframe#browser').attr('src', json.url);
		//$("input[id=my_url]").val(json.url)
		url = json.url
		/*alert(json)*/
	});
}