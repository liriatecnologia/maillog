#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python script that enables to send short e-mail messages from the system
terminal or from other Python programs using an external SMTP e-mail account.
For information on how to install, see the README file.

Author: Renato Candido <renato@liria.com.br>
Copyright 2013 Liria Tecnologia <http://www.liria.com.br>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Changelog:

2013-06-13
Fixed to work with multiline messages.

2013-04-29
Added support for SMTP using SSL and multiple recipients.

2013-04-22
Initial commit.
"""

from textwrap import dedent
import sys
from smtplib import SMTP, SMTP_SSL

# External SMTP account configuration
SENDER_NAME = "Maillog e-mail"
SENDER_EMAIL = "sender@provider.com"
SMTP_SERVER = "mail.provider.com"
SMTP_PORT = "587"
SMTP_LOGIN = "sender@provider.com"
SMTP_PASSWORD = "smtp_password"
USE_SSL = False
# End of configuration

def send_mail(destinations, subject, message, sender_name=SENDER_NAME,
              sender_email=SENDER_EMAIL, smtp_server=SMTP_SERVER,
              smtp_port=SMTP_PORT, smtp_login=SMTP_LOGIN,
              smtp_password=SMTP_PASSWORD, use_ssl=USE_SSL):
    """
    Sends an e-mail to the destinations provided, with the subject and message
    provided. Optionally, the external SMTP account configuration can be set up
    through arguments on the function call.
    """
    destinations_list = destinations.split(';')

    for destination in destinations_list:
        destination = destination.strip()
        email =  dedent("""\
        From: %s <%s>
        To: %s
        Subject: %s
        
        """ % (sender_name, sender_email, destination, subject))

        email = email + message
     
        try:
            if use_ssl:
                smtpObj = SMTP_SSL(smtp_server, smtp_port)
            else:
                smtpObj = SMTP(smtp_server, smtp_port)
            smtpObj.login(smtp_login, smtp_password)
            smtpObj.sendmail(sender_email, destination, email)
            print "Successfully sent email"
        except:
            print "Error: unable to send email"
            sys.exit(1)

def main():
    """
    Main function. Checks the arguments passed to the script and calls
    send_mail() function. This function expects the script to be run as
    maillog.py "<destination email addresses>" "<subject>" "<message>"
    """
    if len(sys.argv) != 4:
        print ("Usage " + __file__ + " \"<destination email addresses>\" "
               + "\"<subject>\"" + " \"<message>\"")
        print ("Example: " + __file__ + " \"bob@gmail.com; ann@gmail.com\" " 
               + "\"Maillog test\"" + " \"If you received this, it worked!\"")
        print ""
        print ("In case of a single recipient, the first argument may not"
               + " need quotes. For example:\n")
        print (__file__ + " bob@gmail.com " 
               + "\"Maillog test\"" + " \"If you received this, it worked!\"")
    else:
        destinations = sys.argv[1]
        subject = sys.argv[2]
        message = sys.argv[3]
        send_mail(destinations, subject, message)

if __name__ == '__main__':
    main()
