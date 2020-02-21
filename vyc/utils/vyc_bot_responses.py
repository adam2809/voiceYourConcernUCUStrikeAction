email_input_prompt = 'Please input your email:'

MESSAGES = {
	'get_started':[
	    'As students we want to support our staff during the UCU strike action!',
	    'The best way you can get involved is to come to picket lines.',
	    'If you are unable to there are still ways you can get involved.',
	],
	'send_email_no':['jak nie mejl to nie'],
	'use_template_no':['Input the content of your email below. The header and footer will be added automatically.'],
	'confirm_input_content_discard':['All changes were discarded. Click a menu button to start over.'],
	'confirm_send_email_ok':['The email was sent. Thank you for getting involved!'],
	'discard_flow':['All changes were discarded','If you want to start again click the menu button below.'],
	'get_email':['Email address registered'],
	'get_content':['Email content saved.'],
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
		'text': 'Would you like to send an email to Shearer West (University of Nottingham Vice-Chancellor) voicing your concern over the strike action?',
		'buttons' : [
	        {
	            "type":"postback",
	            "title":"Yes",
	            "payload":"send_email/yes"
	        }
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
	'input_name':{
		'text': 'Do you confirm you want to send the email?',
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
	},
	'input_email':{
		'text': 'Please enter your name.',
		'buttons' : [
	        {
	            "type":"postback",
	            "title":"Cancel",
	            "payload":"cancel_input/none"
	        }
	    ]
	},
	'email_input_prompt':{
		'text': 'Please enter your email.',
		'buttons' : [
	        {
	            "type":"postback",
	            "title":"Cancel",
	            "payload":"cancel_input/none"
	        }
	    ]
	},
	'invalid_email':{
		'text': 'Please enter a valid email address.',
		'buttons' : [
	        {
	            "type":"postback",
	            "title":"Cancel",
	            "payload":"cancel_input/none"
	        }
	    ]
	}
}


UCU_TEMPLATE_CONTENT = '''
I am writing to complain about the impact of the UCU strike action upon my education.
<br/>
I chose this university in large part due to the staff and I believe that they are the university's greatest asset.
<br/>
As things stand this university, my university, has alienated its staff and is failing me and my fellow students.
<br/>
I urge you to increase your efforts to seek a resolution through national negotiations with UCU in order to enable me to get the education that I deserve.
'''

UCU_TEMPLATE_HEADER = 'Dear vice-chancellor<br/><br/>'

UCU_TEMPLATE_FOOTER = '<br/><br/>Yours<br/>%s'

VC_EMAIL_ADDRESS = 'vco-feedback@nottingham.ac.uk'
