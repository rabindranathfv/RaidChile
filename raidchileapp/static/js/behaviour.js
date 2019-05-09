$( document ).ready(function(){

	// Guarantee that the datepicker uses the correct dateFormat and minDate.
	$(".datepicker.reservation").datepicker({ dateFormat: 'dd/mm/yy', minDate: 0});

	// Search filter sidebar responsive functions
	$("#filter-toggle").click(function(){
		$("#filters-sidebar").toggleClass("w3-hide-small");
	});

	$("#navbar-toggle").click(function(){
		$("#mobile-navbar").toggleClass("w3-hide");
		$(".back-combo-btn").toggleClass("w3-hide");
	});

	// Back to the top button function
	$("button.top-btns").click(function(){
		$("html, body").animate({ scrollTop: 0 }, "slow");
	});

	// Rating Stars Colouring and value setting when clicking them
	$("#rating_input span.fa-star").click(function(){
		$(this).addClass('checked');
		$(this).prevAll(".fa-star").addClass('checked');
		$(this).nextAll(".fa-star").removeClass('checked');
		var val = parseInt($(this).find(".value-span").text())
		$("#rating_input .number-rating").text(val);
		$("#id_rating").val(val);
		// make the form errors hide and submit button available
		$(this).closest("form").find("p.none_rating_error").hide();
		$(this).closest("form").find("#submit-review").prop( "disabled", false );
	});

	// Validation of the review form rating being set.
	$('form#review_add_form').submit(function() {
		var rating_value = parseInt( $(this).find("#rating_input .number-rating").text());
		// Validate that the rating value is between 1 and 5
		if (rating_value < 1 || rating_value > 5){
			// Display warning and disable post button
			$(this).find("p.none_rating_error").show();
			$(this).find("#submit-review").prop( "disabled", true );
			return false;
		}else{
			return true;
		}
	});

	// Making the languague choices drowpdown interactive and look right.
	$('#language-switch').click(function(){
		$(this).toggleClass('extended-switch');
		$('#language-choices').toggle()
	});
	// Make the language choices close up when clicking anywhere else while it's open.
	$(document).click(function(event) {
		//if you click on anything except the choices itself or the "open modal" link, close the modal
		if (!$(event.target).closest(".language-container, #language-switch").length) {
			$("#language-switch").removeClass("extended-switch");
			$("#language-choices").hide();
		}
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