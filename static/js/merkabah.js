var merkabah = {};
merkabah.utils = {};


merkabah.render_form_dialog = function(url, form_id, form_content, dialog_title) {
	
	var dialog = $('<div id="modal_for_form_' + form_id + '" class="modal hide fade modal_wide" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">');
	var form = $('<form class="fill-up" id="' + form_id + '" method="POST" action="' + url + '">');
	dialog.append(form);

	var header = $('<div class="modal-header">');

	var close = $('<button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>');
	header.append(close);

	var modal_title = $('<h3 id="myModalLabel">' + dialog_title + '</h3>');
	header.append(modal_title);

	form.append(header);

	var modal_body = $('<div class="modal-body"> '  + form_content + ' </div>');

	// TODO: Pass these via the ajax data args
	//modal_body.append($('<input type="hidden" name="action" value="display_form"/>'));
	//modal_body.append($('<input type="hidden" name="form_id" value="' + form_id + '"/>'));

	form.append(modal_body);

	var modal_footer = $('<div class="modal-footer">');

	modal_footer.append($('<button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>'));
	modal_footer.append($('<button class="btn btn-primary">Submit</button>'));

	form.append(modal_footer);

	//var dialog = $('<div class="modal-body"> '  + form_content + ' </div> <div class="modal-footer"> <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button> <button class="btn btn-primary">Submit</button> </div>  </form> </div>');
	$('body').append(dialog);
	
	// need to require these things
	// ckeditor
	
	//$('.ckeditor', dialog).ckeditor()
	return dialog.modal();
}


merkabah.utils.parse_query_params = function(query_string){
	/* Thank you Andy E - http://stackoverflow.com/questions/901115/how-can-i-get-query-string-values */
	var urlParams = {};
    var match,
        pl     = /\+/g,  // Regex for replacing addition symbol with a space
        search = /([^&=]+)=?([^&]*)/g,
        decode = function (s) { return decodeURIComponent(s.replace(pl, " ")); },
        query  = window.location.search.substring(1);

    while (match = search.exec(query_string))
       urlParams[decode(match[1])] = decode(match[2]);

	return urlParams;
};

/* Handlers */
$.fn.redirect_handler = function(data){
	/*
	Handler to redirect
	*/

	window.location = data.url;
}

$.fn.alert_handler = function(data){
	/*
	Handler to redirect
	*/

	alert(data.message);
}

$.fn.error_handler = function(data){
	/*
	Handler to redirect
	*/

	data.title = 'An error occurred.'
	$.fn['dialog_handler'].apply(this, [data]);
}

$.fn.dialog_handler = function(data){
	/*
	Handler to redirect
	*/

	//$('body').append('what?');
	var dialog = $('#myModal');
	$('.modal-body', dialog).html('').append(data.content);
	$('#myModalLabel', dialog).html('').append(data.title);
	$(dialog).modal('toggle');
}

$.fn.close_form_dialog_handler = function(data) {
	/*
	Close The Dialog
	*/

	console.log(data);

	var form_id = data.form_id;
	var dialog = $('#modal_for_form_' + form_id + '');

	$(dialog).modal('hide');
	
}

$.fn.form_handler = function(data){
	/* Handler for form responses */
	var form_id, dialog_title, rendered_form;

	form_id = data.form_id

	if (!form_id) {
		alert('Please provide a form_id');
	}

	dialog_title = data.title
	rendered_form = data.form
	url = data.target_url
	action = data.target_action

	//$.fn['dialog_handler'].apply(this, [data]);

	window.dialog = merkabah.render_form_dialog(url, form_id, rendered_form, dialog_title)
	dialog.show('show');

	var submit_data = {'form_id': form_id, 'action' : action};
	var ajax_settings = merkabah.get_ajax_form_settings(submit_data, 'get');
	
	$('#' + form_id).ajaxForm(ajax_settings);
}

$.fn.add_grid_row_handler = function(data) {
    //var node_id = data.grid_id;
    var row = $(data.content);
    $('#grid').prepend(row);
    row.hide();
    row.toggle('highlight');
}
$.fn.dynamic_content_handler = function(data) {
	var node_id = data.node_id

	if (!node_id) {
		alert('Node id ' + node_id + ' given, but doesn\'t exist in dom.')
	}

	var target_node = $('#' + node_id);
	if (!target_node.size()) {
		console.log('Received a dynamic content response type with target id of "' + node_id + '" but failed to find the node in the existing dom.');
	}

	target_node.html($(data.content));
	merkabah.apply_bindings(target_node);
}

merkabah.get_ajax_form_settings = function(data, type) {
	if (type){
		type = 'post';
	}

	var csrftoken = getCookie('csrftoken');
	console.log(csrftoken);

	var ajax_settings = {
		'dataType' : 'json',
		'data' : data,
		'async': false,
		'type' : type,
		'csrfmiddlewaretoken' : csrftoken,
		crossDomain: false, // obviates need for sameOrigin test
		beforeSend: function(xhr, settings) {
		        //if (!csrfSafeMethod(settings.type)) {
		            xhr.setRequestHeader("X-CSRFToken", csrftoken);
		        //}
		},

		success: merkabah.ajax_success,
		error: function(data, textStatus, errorThrown) {
			data.title = 'There was an error with this ajax call. See log for details.'
			data.content = data.responseText
			return $.fn.error_handler.apply(this, [data]);
		}			
	};
	return ajax_settings;
}

$.fn.form_error_handler = function(data){

	var form_id = data.form_id;
	var xform = $('#' + form_id);
	if (xform.size() === 0){
		alert('Form with id "' + form_id + '" not found on page.');
	}

	// Clear existing errors on the form
	$('.error .help-inline', xform).html('');
	$('.error', xform).removeClass('error');
	$('.alert', xform).remove();		


	/*
	<div class="input">
		<input type="text" placeholder="Username" class="error">
	    <span class="input-error" data-title="please write a valid username" data-original-title="">
	    	<i class="icon-warning-sign"></i>
		</span>
	</div>
	*/


	//field_control_group.addClass('error');

	var error_list = jQuery.parseJSON(data['form_errors']);

	$.each(error_list, function(field_name, field_errors){
		var field_control_group, field_help_inline;
		
		var input = $('#id_' + field_name)
		input.addClass('error');

		field_control_group = input.parents('.input');
		field_control_group.append('<span class="input-error" data-title="please write a valid username" data-original-title=""><i class="icon-warning-sign"></i></span>');

	});

	alert_notice = $('<div class="alert alert-error"><button type="button" class="close" data-dismiss="alert">&times;</button> <strong>Warning!</strong> There was an error with your form. </div>');

	form_in_dialog = $('#modal_for_form_' + form_id).size() > 0;
	if (form_in_dialog) {
		$('#modal_for_form_' + form_id + ' .modal-body').prepend(alert_notice);
	}
	else {
		xform.prepend(alert_notice);
	}
}
merkabah.run_action = {};
merkabah.run_action.error_message = 'We are experiencing technical difficulties. Please try again momentarily.';


merkabah.ajax_success = function(data, textStatus, jqXHR){
	/*
	Default Merkabah Response List handler
	*/
	
	
	//var action_responses = data.action_responses;

	var action_responses = data.action_response_list;

	//action_responses = action_responses
	
	$.each(action_responses, function(i, action_response) {
		var action_response = jQuery.parseJSON(action_response);
		var response_handler_name = action_response.response_type; // data.response_type;

		if (response_handler_name) {
			response_handler_name = response_handler_name + '_handler';
			
			response_handler = $.fn[response_handler_name];

			if (!(response_handler)) {
				data.title = 'Response Handler Error'
				data.content = 'No response handler <b>' + response_handler_name + '</b> defined in $.fn.'
				return $.fn.error_handler.apply(this, [action_response]);
			}
			else {
				return response_handler.apply(this, [action_response]);
			}
		
		}
		else {
			alert('Action executed, but return did not contain a response_type param. See log.');
		}
	}); // each
}



merkabah.run_action.execute = function(pathname, data) {
	/* */
	response_method = 'get'

	url = pathname
	settings = {
		'dataType' : 'json',
		'data' : data,
		'type' : response_method,
		'csrfmiddlewaretoken' : csrftoken,
		crossDomain: false, // obviates need for sameOrigin test
		beforeSend: function(xhr, settings) {
		        //if (!csrfSafeMethod(settings.type)) {
		            xhr.setRequestHeader("X-CSRFToken", csrftoken);
		        //}
		},
		success: merkabah.ajax_success,
		error: function(data, textStatus, errorThrown) {
			data.title = 'There was an error with this ajax call. See log for details.'
			data.content = data.responseText
			return $.fn.error_handler.apply(this, [data]);
		}			
	};

	$.ajax(url, settings);
}
merkabah.apply_bindings = function(node){

	/* Bind action buttons, links, etc */
	$('.action', node).click(function(e){
		e.preventDefault();
		var btn = this;
		var $btn = $(this);

		var pathname = btn.pathname
		var query_string = btn.search;

		if (query_string.length >= 1 && query_string[0] == '?')
			query_string = query_string.substring(1);

		q_params = merkabah.utils.parse_query_params(query_string);		
		merkabah.run_action.execute(pathname, q_params);

		return false
	});
	
};





function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');






$(function(){
	merkabah.apply_bindings($(document));
});