#!/usr/bin/python
from jira.client import JIRA
import sys

###########
## Will delete every annoying automation comment from your ticket(s)
## If you would like for it to happen automatically, please tack on "streamline" to the end
###########
def getEm( streamlined ):
	options = { 'server': 'https://jira.server.com' }

	jira = JIRA( options=options, basic_auth=('username','password') )

	tickets = jira.search_issues( '("Dev Lead"=currentUser() OR assignee = currentUser()) AND ( "Last Resolution Date" > startOfWeek() OR status != Closed)' )

	for ticket in tickets:
		comments = jira.comments( ticket.key )
		for comment in comments:
			if comment.author.name == 'automation':
				answ = 'y' # for streamlining the process
				if streamlined == False:
					answ = raw_input( str(comment.body)[:80] + ' - ' + '\033[93m' + 'DELETE y/n? ' + '\033[0m' )
				if answ == 'y':
					print 'Deleting comment...'
					comment.delete()
					print 'Deleted.'
				else:
					print 'Ok - I will ask later on.'

streamlined = False
if len(sys.argv) > 1:
	if sys.argv[1] == 'streamline':
		streamlined = True

getEm( streamlined )
