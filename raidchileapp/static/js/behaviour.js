$( document ).ready(function(){
	// Guarantee that the datepicker uses the correct dateFormat and minDate.
	$(".datepicker.reservation").datepicker({ dateFormat: 'dd/mm/yy', minDate: 0});

	// Search filter sidebar responsive functions
	$("#filter-toggle").click(function(){
		console.log("Click");
		$("#filters-sidebar").toggleClass("w3-hide-small");
	});

	// Back to the top button function
	$("#top-btns button").click(function(){
		$("html, body").animate({ scrollTop: 0 }, "slow");
	});

	/*
	var maxHeight = 0;

	console.log("Firing resizing!")
	$("div.w3-col div.w3-card-2, div.w3-half div.w3-card-2").each(function() {
		if ($(this).height() > maxHeight)
		{
			maxHeight = $(this).height();
		}
	});
	//set all specific classes to highest value from previous loop variable
	$("div.w3-col div.w3-card-2, div.w3-half div.w3-card-2").each(function() {
		$(this).css("height", maxHeight);
	});*/

	// Method to remove empty fields from GET forms.
	/*
	$("#search-form").submit(function() {
		$(this).find(":input").filter(function(){ return !this.value; }).attr("disabled", "disabled");
		return true; // Ensure form still submits
	});*/

	// Un-disable form fields when page loads, in case they click back after submission
	//$("#search-form").find(":input").removeAttr("disabled");

});