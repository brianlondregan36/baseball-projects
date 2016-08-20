
$( document ).ready(function() {
	$backtotop = $('#backtotop');
	$window = $(window);
	wait = false; 
	
	$('.in-story-image img').click(function(){
		var a = '<a href="#close">'
		var img = $(this).prop('outerHTML');
		var htmlString = a + img + '</a>';
		
		$('#openModal').html(htmlString);
	});
	
	$window.on('scroll resize', CheckOutOfView);
});


function CheckOutOfView() 
{
	var window_height = $window.height();
	var window_top_position = $window.scrollTop();
	var window_bottom_position = (window_top_position + window_height);
	
	if(window_bottom_position > 1400 && !wait)
	{
		wait = true; 
		$backtotop.css('visibility', 'visible');
		var t = setTimeout(hide, 2000);
		function hide(){
			$backtotop.css('visibility', 'hidden');
			clearTimeout(t);
			wait = false;
		}
	}
	else if(window_bottom_position < 1400 && !wait)
		$backtotop.css('visibility', 'hidden');
}



