$( document ).ready(function(){
	// Slideshow variables
	var $slides = $(".slideshow-slide")
	var $thumbnails = $(".slide-thumbnail")
	var slideIndex = 1;
	var slidePause = false;
	var slideTimer;

	// Remove the 'hidden' class and set display: None; (To avoid juggling classes)
	$slides.filter(".hidden").removeClass("hidden").hide();

	// If there are more than one slide, start the automatic slideshow (4seg per slide)
	if ($slides.length > 1){
		slideTimer = setInterval(carousel, 4000);
	}

	// Automatic slideshow function
	function carousel(){
		$slides.hide();
		$thumbnails.removeClass("w3-opacity-off");
		if (slideIndex >= $slides.length){
			slideIndex = 0;
		}
		$($slides[slideIndex]).show();
		$($thumbnails[slideIndex]).addClass("w3-opacity-off");
		slideIndex++;
	}

	// Manual selection by the user of a single slide.
	$(".slide-thumbnail").click(function(){
		// Stop time interval
		clearInterval(slideTimer);

		var viewIndex = $thumbnails.index( this );

		// Hiding all slides and giving opacity effect to all thumbnails
		$slides.hide();
		$thumbnails.removeClass("w3-opacity-off");

		// Showing selected slide and removing opacity effect to its thumbnail
		$($slides[viewIndex]).show();
		$(this).addClass("w3-opacity-off");

		// Resume automatic slideshow from next slide.
		slideIndex = viewIndex + 1;
		if ($slides.length > 1){
			slideTimer = setInterval(carousel, 8000);
		}
	});
});