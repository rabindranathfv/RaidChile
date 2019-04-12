$( document ).ready(function(){
	// Guarantee that the datepicker uses the correct dateFormat and minDate.
	$(".datepicker.reservation").datepicker({ dateFormat: 'dd/mm/yy', minDate: 0});

	// Search filter sidebar responsive functions
	$("#filter-toggle").click(function(){
		console.log("Click");
		$("#filters-sidebar").toggleClass("w3-hide-small");
	});

	// Back to the top button function
	$("button.top-btns").click(function(){
		$("html, body").animate({ scrollTop: 0 }, "slow");
	});
});