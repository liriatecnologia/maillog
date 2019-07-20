#!/usr/bin/env python3

"""
Python script that enables to send short e-mail messages from the system
terminal or from other Python programs using an external SMTP e-mail account.
For information on how to install, see the README file.

Author: Renato Candido <renato@liria.com.br>
Copyright 2014 Liria Tecnologia <http://www.liria.com.br>

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

2019-07-20
Migration to Python 3.

2015-02-14
Correction to work with special characters.

2014-04-04
Fixed to display the "from" field correctly.

2014-03-27
Added support for attaching files in e-mail.

2013-06-13
Fixed to work with multiline messages.

2013-04-29
Added support for SMTP using SSL and multiple recipients.

2013-04-22
Initial commit.
"""

import sys
import os
from smtplib import SMTP, SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from textwrap import dedent

# External SMTP account configuration
SENDER_NAME = "Maillog e-mail"
SENDER_EMAIL = "sender@provider.com"
SMTP_SERVER = "mail.provider.com"
SMTP_PORT = "587"
SMTP_LOGIN = "sender@provider.com"
SMTP_PASSWORD = "smtp_password"
USE_SSL = False
# End of configuration


def send_mail(destinations, subject, message, files=[], sender_name=SENDER_NAME,
              sender_email=SENDER_EMAIL, smtp_server=SMTP_SERVER,
              smtp_port=SMTP_PORT, smtp_login=SMTP_LOGIN,
              smtp_password=SMTP_PASSWORD, use_ssl=USE_SSL):
    """
    Sends an e-mail to the destinations provided, with the subject, message and
    attached files provided. Optionally, the external SMTP account configuration
    can be set up through arguments on the function call.
    """

    if type(destinations) is str:
        destinations = destinations.split(';')
        for n, destination in enumerate(destinations):
            destinations[n] = destination.strip()

    if type(files) is str:
        files = files.split(';')
        for n, file in enumerate(files):
            files[n] = file.strip()

    email = MIMEMultipart()
    email['From'] = sender_name + " <" + sender_email + ">"
    email['To'] = COMMASPACE.join(destinations)
    email['Date'] = formatdate(localtime=True)
    email['Subject'] = subject
    email.attach(MIMEText(message, 'plain', 'utf-8'))

    for f in files:
        part = MIMEBase('application', "octet-stream")
        try:
            part.set_payload(open(f, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment; filename="%s"' % os.path.basename(f))
            email.attach(part)
        except:
            print("File " + f + " not found")
            sys.exit(1)

    try:
        if use_ssl:
            smtpObj = SMTP_SSL(smtp_server, smtp_port)
        else:
            smtpObj = SMTP(smtp_server, smtp_port)
        smtpObj.login(smtp_login, smtp_password)
        smtpObj.sendmail(sender_email, destinations, email.as_string())
        if __name__ == '__main__':
            print("Successfully sent email")
    except:
        print("Error: unable to send email")
        sys.exit(1)


def main():
    """
    Main function. Checks the arguments passed to the script and calls
    send_mail() function. This function expects the script to be run as
    maillog.py "<destination email addresses>" "<subject>" "<message>"
    """
    if (len(sys.argv) < 4 or len(sys.argv) > 5 or sys.argv[1] == '-h'
            or sys.argv[1] == '--help'):
        print(dedent(f'''\
        Usage {__file__} "<destination email addresses>" "<subject>" "<message>" "[<files>]
        Example:
        { __file__} "bob@gmail.com ann@gmail.com" "Maillog test" "If you received this, it worked!"
        
        In case of a single recipient, the first argument might not need quotes 
        (in case of no spaces, in general. For example:
        {__file__} bob@gmail.com "Maillog test" "If you received this, it worked!"

        Optionally, files can be attached to the e-mail. For example:
        {__file__} "bob@gmail.com; ann@gmail.com" "Maillog test" "If you received this, it worked!" "./dir1/file1; ./dir2/file2"
        '''))
    else:
        destinations = sys.argv[1]
        subject = sys.argv[2]
        message = sys.argv[3]
        if len(sys.argv) == 5:
            files = sys.argv[4]
            send_mail(destinations, subject, message, files)
        else:
            send_mail(destinations, subject, message)


if __name__ == '__main__':
    main()
