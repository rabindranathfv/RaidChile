$( document ).ready(function(){
	// Slideshow functions
	var $slides = $(".slideshow-slide")
	var $thumbnails = $(".slide-thumbnail")

	$slides.filter(".hidden").removeClass("hidden").hide();

	$(".slide-thumbnail").click(function(){
		var viewIndex = $thumbnails.index( this );

		// Hiding all slides and giving opacity effect to all thumbnails
		$slides.hide();
		$thumbnails.removeClass("w3-opacity-off")

		// Showing intended slide and removing opacity effect to its thumbnail
		$($slides[viewIndex]).show();
		$(this).addClass("w3-opacity-off")
	});
});
