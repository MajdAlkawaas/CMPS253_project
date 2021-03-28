// Class definition
var KTFormControls = function () {
	// Private functions
	var _initDemo1 = function () {
		FormValidation.formValidation(
			document.getElementById('kt_form_1'),
			{
				fields: {
					name: {
						validators: {
							notEmpty: {
								message: 'Name is required'
							},
						}
					},

					PhoneNumber: {
						validators: {
							notEmpty: {
								message: 'Phone number is required'
							},
						}
					},

					options: {
						validators: {
							choice: {
								min: 1,
								max: 1,
								message: 'Please select 1 option'
							}
						}
					},
				},

				plugins: { //Learn more: https://formvalidation.io/guide/plugins
					trigger: new FormValidation.plugins.Trigger(),
					// Bootstrap Framework Integration
					bootstrap: new FormValidation.plugins.Bootstrap(),
					// Validate fields when clicking the Submit button
					submitButton: new FormValidation.plugins.SubmitButton(),
					// Submit the form when all fields are valid
					defaultSubmit: new FormValidation.plugins.DefaultSubmit(),
				}
			}
		);
	}

	return {
		// public functions
		init: function() {
			_initDemo1();
		}
	};
}();

jQuery(document).ready(function() {
	KTFormControls.init();
});
