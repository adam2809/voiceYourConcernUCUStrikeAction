email_input_prompt = 'Please input your email:'

MESSAGES = {
	'get_started':[
	    'As students we want to support our lectures during the UCU strike action!',
	    'Learn more at https://www.ucu.org.uk/strikeforuss.',
	],
	'send_email_no':['jak nie mejl to nie'],
	'use_template_yes':[email_input_prompt],
	'use_template_no':['Input the content of your email below. The header and footer will be added automatically.'],
	'confirm_input_content_ok':['The content of your message was set.',email_input_prompt],
	'confirm_input_content_discard':['All changes were discarded. Click a menu button to start over.'],
	'confirm_send_email_ok':['email sent'],
	'confirm_send_email_discard':['email discarded'],
	'get_email':['email registered'],
	'get_content':['content registered'],
}

POSTBACKS = {
	'send_email_yes':{
		'text': 'Would you like to use an email templete recommended by UCU?',
		'buttons' : [
	        {
	            "type":"postback",
	            "title":"Yes",
	            "payload":"use_template/yes"
	        },
	        {
	            "type":"postback",
	            "title":"No",
	            "payload":"use_template/no"
	        },
	    ]
	},
	'get_started':{
		'text': 'Send angry email?',
		'buttons' : [
	        {
	            "type":"postback",
	            "title":"Yes",
	            "payload":"send_email/yes"
	        },
	        {
	            "type":"postback",
	            "title":"No",
	            "payload":"send_email/no"
	        },
	    ]
	},
	'input_content':{
		'text': 'Do you confirm the content of your message?',
		'buttons' : [
	        {
	            "type":"postback",
	            "title":"Yes",
	            "payload":"confirm_input_content/ok"
	        },
	        {
	            "type":"postback",
	            "title":"Discard",
	            "payload":"confirm_input_content/discard"
	        },
	    ]
	},
	'input_email':{
		'text': 'Do you confirm you want to send email?',
		'buttons' : [
	        {
	            "type":"postback",
	            "title":"Yes",
	            "payload":"confirm_send_email/ok"
	        },
	        {
	            "type":"postback",
	            "title":"Discard",
	            "payload":"confirm_send_email/discard"
	        },
	    ]
	}
}
