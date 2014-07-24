#!/usr/bin/python
from jira.client import JIRA
from collections import Counter
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import matplotlib.pyplot as plt

##################################
## Will retrieve the data from 	##
## jira and parse through each	##
## rejection into a collection	##
#################################
def getData():
	options = {
		'server': 'https://jira.server.com'
	}

	jira = JIRA( options=options, basic_auth=('user','pass') )

	issues = jira.search_issues( 'status was Rejected DURING (startOfWeek(-1), startOfWeek())  AND "Team Lead" = myuser' )

	rates = {}
	reasons = {}

	for issue in issues:
		issue = jira.issue( issue.key )
		name = str( issue.fields.customfield_10901.displayName )
		reason = str( issue.fields.customfield_14700 )

		# Add name to rates set
		if name not in rates:
			rates[ name ] = 0
		
		# Add reason name to reasons set
		if reason not in reasons:
			reasons[ reason ] = 0
		
		rates[name] = rates[name]+1
		reasons[reason] = reasons[reason]+1

	mailInfo( rates, reasons )
	return

##################################
## Will create a pie graph and	##
## will email the graph to dev	##
##################################
def mailInfo( rates, reasons ):
	labels = []

	values = []

	colors = [ 'yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'green', 'red', 'blue' ]

	## Lets do rejection rates by name first
	for name, rate in rates.items():
		labels.append( name + ' (' + str( rate ) + ')' )
		values.append( rate )

	
	plt.figure(1)
	plt.subplot(211)
	plt.title( 'Rejection Rates - Last Week' )
	patches, texts, autotext = plt.pie( values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90 )
	plt.axis( 'equal' )
	plt.tight_layout()
	plt.plot()

	## Now lets do rejection reasons
	labels = []
	values = []
	for reason, rate in reasons.items():
		labels.append( reason + ' (' + str( rate ) + ')' )
		values.append( rate )

	plt.subplot(212)
	plt.title( 'Rejection Reasons - Last Week' )
	patches2, texts2, autotext2 = plt.pie( values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90 )
	plt.axis( 'equal' )
	plt.tight_layout()
	plt.plot()

	## Save the graphs	
	plt.savefig( "rejections.png" )
	
	img = open( "rejections.png", 'rb' ).read()

	msg = MIMEMultipart('related')
	msg['Subject'] = 'Rejection Rates'
	msg['From'] = 'you@you.com'
	msg['To'] = 'you@you.com'

	msgAlt = MIMEMultipart('alternative')
	msg.attach(msgAlt)

	text = MIMEText( 'Here is a chart of the rejection rates for last week.<br><br><img src="cid:image1"><br><br>This is an automated message. If you do not wish to receive it, please mute the email.', 'html' )
	msgAlt.attach( text )

	image = MIMEImage( img, name=os.path.basename("rejections.png") )
	image.add_header( 'Content-ID', '<image1>' )
	msg.attach( image )

	s = smtplib.SMTP( 'smtp.server.com' )
	s.ehlo()
	s.starttls()
	s.ehlo()
	s.login( 'user', 'pass' )
	s.sendmail( 'you@you.com', 'you@you.com', msg.as_string() )
	s.quit()
	return

print( "starting" )
getData()
