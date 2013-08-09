(function () {
	'use strict';
	var validateEmail;

	validateEmail = function(event) {
		var address,
			$span;

		address = $(this).val().trim();
		$span = $(this).parent().find('span');

		if (address.match(/\w+.*@\w+(\.\w+)+/)) {
			$span.text('valid');
		} else {
			$span.text('invalid');
		}
	};

	$(document).ready(function() {
		$('#email').keypress(validateEmail);
	});
})();
