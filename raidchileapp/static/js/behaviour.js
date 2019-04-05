$( document ).ready(function(){
	// Guarantee that the datepicker uses the correct dateFormat and minDate.
	$(".datepicker.reservation").datepicker({ dateFormat: 'dd/mm/yy', minDate: 0});

	// Search filter sidebar responsive functions
	$("#filter-toggle").click(function(){
		console.log("Click");
		$("#filters-sidebar").toggleClass("w3-hide-small");
	});


	// Method to remove empty fields from GET forms.
	/*
	$("#search-form").submit(function() {
		$(this).find(":input").filter(function(){ return !this.value; }).attr("disabled", "disabled");
		return true; // Ensure form still submits
	});*/

	// Un-disable form fields when page loads, in case they click back after submission
	//$("#search-form").find(":input").removeAttr("disabled");

});