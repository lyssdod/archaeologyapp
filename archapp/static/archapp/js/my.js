(function(jQuery) {
    $(document).ready(function($) {
        $(function(){
            var uploader = new qq.FileUploader({
                action: $('my'),
                element: $('#file-uploader')[0],
                multiple: true,
                onComplete: function(id, fileName, responseJSON) {
                    if(responseJSON.success) {
                        alert("success!");
                    } else {
                        alert("upload failed!");
                    }
                },
                onAllComplete: function(uploads) {
                    // uploads is an array of maps
                    // the maps look like this: {file: FileObject, response: JSONServerResponse}
                    alert("All complete!");
                },
                params: {
                    'csrf_token': '{{ csrf_token }}',
                    'csrf_name': 'csrfmiddlewaretoken',
                    'csrf_xname': 'X-CSRFToken',
                },
            });
            });
	});
})();
