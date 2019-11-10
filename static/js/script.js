var form_data = new FormData();

jQuery.each(jQuery('#file')[0].files, function(i, file) {
    data.append('file-'+i, file);
});

$("#classify-form").ajaxForm({
	type: 'POST',
	url: '/classify',
	data: form_data,
	contentType: false,
	cache: false,
	processData: false,
	success: function(data) {
// what you want to do with the prediction returned
	}
})