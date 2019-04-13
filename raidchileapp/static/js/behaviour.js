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

	// Validate that the passengers total number is higher than the minimun
	$('#id_adult_quantity, #id_children_quantity').on('input', function() {
		console.log("Firing validation of min passengers.")
		var min_pax = parseInt( $(this).closest("form").find("div.min_pax").text() );
		var adult_qty = parseInt( $(this).closest("form").find("#id_adult_quantity").val() );
		var children_qty = parseInt( $(this).closest("form").find("#id_children_quantity").val() );

		// Validate that the passengers total number is higher than the minimun
		if (adult_qty + children_qty < min_pax){
			// Display warning and disable reserve button
			$(this).closest("form").find("p.min_pax_error").show();
			$(this).closest("form").find("#submit-reserve, .submit-reserve").prop( "disabled", true );
		}else{
			$(this).closest("form").find("p.min_pax_error").hide();
			$(this).closest("form").find("#submit-reserve, .submit-reserve").prop( "disabled", false );
		}
	});

	// Validate that the passengers total number is higher than the minimun or don't submit the form
	$('#cart_add_form, form.cart_add_form').submit(function() {
		var min_pax = parseInt( $(this).find("div.min_pax").text() );
		var adult_qty = parseInt( $(this).find("#id_adult_quantity").val() );
		var children_qty = parseInt( $(this).find("#id_children_quantity").val() );

		// Validate that the passengers total number is higher than the minimun
		if (adult_qty + children_qty < min_pax){
			// Display warning and disable reserve button
			$(this).find("p.min_pax_error").show();
			$(this).find("#submit-reserve, .submit-reserve").prop( "disabled", true );
			return false;
		}else{
			$(this).find("p.min_pax_error").hide();
			$(this).find("#submit-reserve, .submit-reserve").prop( "disabled", false );
			return true;
		}
	});
});