#!/usr/bin/python
from jira.client import JIRA
import unicodedata
import time
import datetime
import math

def getEm():
	options = { 'server': 'https://jira.server.com' }

	jira = JIRA( options=options, basic_auth=('user','pass') )

	tickets = jira.search_issues( 'Participants = currentUser() AND updated > startOfDay() ORDER BY updated DESC' )

	for ticket in tickets:
		comments = jira.comments( ticket.key )
		for comment in comments:
			if comment.author.name == 'username':
				t = comment.created
				t = unicodedata.normalize( 'NFKD', t ).encode( 'UTF-8', 'ignore' )
				t = t.split("T")
				t = t[0]
				now = time.strftime("%Y-%m-%d")
				if t == now:
					minute_len = len( comment.body.split() )
					if minute_len <= 40:
						minutes = "3m"
					else:
						minutes = str( int( round( math.ceil( minute_len/40 )*3 ) ) ) + "m"
					jira.add_worklog( issue=str(ticket.key), timeSpent=minutes )
	
getEm()
