## Python3.6

import httplib2
import os
import pandas as pd
import oauth2client
from oauth2client import client, tools
from oauth2client.file import Storage
import base64
from email import encoders

# needed for attachment
import smtplib
import mimetypes
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
# List of all mimetype per extension: http://help.dottoro.com/lapuadlp.php  or http://mime.ritey.com/

from apiclient import errors, discovery  # needed for gmail service

## Local Python Files
from convertBinaryToEmail import binary_to_str
from pdfEditing import SetHeaderFooter
from dataFilesPaths import *
from writeToXlsx import write_to_excel

SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


def get_credentials():
    # If needed create folder for credential
    home_dir = os.path.expanduser('~')  # >> C:\Users\Me
    # >>C:\Users\Me\.credentials   (it's a folder)
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)  # create folder if doesnt exist
    credential_path = os.path.join(
        credential_dir, 'gmail-python-quickstart.json')

    # Store the credential
    store = Storage(credential_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


# Get creds, prepare message and send it
def create_message_and_send(sender, to, subject,  message_text_plain, message_text_html, attached_file=None):
    credentials = get_credentials()

    # Create an httplib2.Http object to handle our HTTP requests, and authorize it using credentials.authorize()
    http = httplib2.Http()

    # http is the authorized httplib2.Http()
    # or: http = credentials.authorize(httplib2.Http())
    http = credentials.authorize(http)

    service = discovery.build('gmail', 'v1', http=http)

    if attached_file:
        # with attachment
        message_with_attachment = create_Message_with_attachment(
            sender, to, subject, message_text_plain, message_text_html, attached_file)
        return send_Message_with_attachement(service, "me", message_with_attachment, message_text_plain, attached_file)
    else:
        # without attachment
        message_without_attachment = create_message_without_attachment(
            sender, to, subject, message_text_html, message_text_plain)
        return send_Message_without_attachement(service, "me", message_without_attachment, message_text_plain)


def create_message_without_attachment(sender, to, subject, message_text_html, message_text_plain):
    print("In Without attachment Function")
    # Create message container
    # needed for both plain & HTML (the MIME type is multipart/alternative)
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = to

    # Create the body of the message (a plain-text and an HTML version)
    message.attach(MIMEText(message_text_plain, 'plain'))
    message.attach(MIMEText(message_text_html, 'html'))

    raw_message_no_attachment = base64.urlsafe_b64encode(message.as_bytes())
    raw_message_no_attachment = raw_message_no_attachment.decode()
    body = {'raw': raw_message_no_attachment}
    return body


def create_Message_with_attachment(sender, to, subject, message_text_plain, message_text_html, attached_file):
    """Create a message for an email.

    message_text: The text of the email message.
    attached_file: The path to the file to be attached.

    Returns:
    An object containing a base64url encoded email object.
    """

    # An email is composed of 3 part :
    # part 1: create the message container using a dictionary { to, from, subject }
    # part 2: attach the message_text with .attach() (could be plain and/or html)
    # part 3(optional): an attachment added with .attach()

    # Part 1
    message = MIMEMultipart()  # when alternative: no attach, but only plain_text
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    # Part 2   (the message_text)
    # The order count: the first (html) will be use for email, the second will be attached (unless you comment it)
    message.attach(MIMEText(message_text_html, 'html'))
    message.attach(MIMEText(message_text_plain, 'plain'))

    # Part 3 (attachement)
    # # to attach a text file you containing "test" you would do:
    # # message.attach(MIMEText("test", 'plain'))
    my_mimetype, encoding = mimetypes.guess_type(attached_file)

    # If the extension is not recognized it will return: (None, None)
    # for unrecognized extension it set my_mimetypes to  'application/octet-stream' (so it won't return None again).
    if my_mimetype is None or encoding is not None:
        my_mimetype = 'application/octet-stream'

    main_type, sub_type = my_mimetype.split(
        '/', 1)  # split only at the first '/'

    # this part is used to tell how the file should be read and stored (r, or rb, etc.)
    if main_type == 'text':
        print("text")
        # 'rb' will send this error: 'bytes' object has no attribute 'encode'
        temp = open(attached_file, 'r')
        attachement = MIMEText(temp.read(), _subtype=sub_type)
        temp.close()

    elif main_type == 'image':
        print("image")
        temp = open(attached_file, 'rb')
        attachement = MIMEImage(temp.read(), _subtype=sub_type)
        temp.close()

    elif main_type == 'audio':
        print("audio")
        temp = open(attached_file, 'rb')
        attachement = MIMEAudio(temp.read(), _subtype=sub_type)
        temp.close()

    elif main_type == 'application' and sub_type == 'pdf':
        temp = open(attached_file, 'rb')
        attachement = MIMEApplication(temp.read(), _subtype=sub_type)
        temp.close()

    else:
        attachement = MIMEBase(main_type, sub_type)
        temp = open(attached_file, 'rb')
        attachement.set_payload(temp.read())
        temp.close()

    encoders.encode_base64(attachement)
    filename = os.path.basename(attached_file)
    # name preview in email
    attachement.add_header('Content-Disposition',
                           'attachment', filename=filename)
    message.attach(attachement)

    # Part 4 encode the message (the message should be in bytes)
    # the message should converted from string to bytes.
    message_as_bytes = message.as_bytes()
    # encode in base64 (printable letters coding)
    message_as_base64 = base64.urlsafe_b64encode(message_as_bytes)
    # need to JSON serializable (no idea what does it means)
    raw = message_as_base64.decode()
    return {'raw': raw}


def send_Message_without_attachement(service, user_id, body, message_text_plain):
    try:
        message_sent = (service.users().messages().send(
            userId=user_id, body=body).execute())
        print("message_sent", message_sent)
        message_id = message_sent['id']
        print('Message sent (without attachment) \n\n Message Id: {0}\n\n Message:\n\n {1}'.format(
            message_id, message_text_plain))
        return True
    except errors.HttpError as error:
        print('An error occurred: {}'.format(error))
        return False


def send_Message_with_attachement(service, user_id, message_with_attachment, message_text_plain, attached_file):
    try:
        message_sent = (service.users().messages().send(
            userId=user_id, body=message_with_attachment).execute())
        message_id = message_sent['id']
        # print(attached_file)
        print('Message sent (with attachment) \n\n Message Id: {0}\n\n Message:\n\n {1}'.format(
            message_id, message_text_plain))
        return True
    except errors.HttpError as error:
        print('An error occurred: {}'.format(error))
        return False


def main():
    ## Read excel file
    xl = pd.read_excel(input_file_path, header=None)
    shape_of_sheet = xl.shape
    ## convert sheet values into list
    xl_list = xl.values.tolist()
    ## Decode email Data from convertBinaryToEmail File
    binary_to_str(xl_list)
    ## Create Dict from list for better data handling
    xl_list_of_dict = []
    for item in xl_list[1:]:
        xl_dict = {}
        xl_dict['Serial ID'] = item[0]
        xl_dict['Course ID'] = item[1]
        xl_dict['User Name'] = item[2]
        xl_dict['email'] = item[3]
        xl_dict['HEX code serial ID'] = item[4]
        xl_dict['HEX code course ID'] = item[5]
        xl_dict['addition D + E'] = item[6]
        xl_dict['Encoded Code'] = item[7]
        xl_dict['Decoded Email'] = item[8]
        xl_list_of_dict.append(xl_dict)

    ## Enter your Email ID from which you want to send Email
    ## If this email is not configured it will redirect to browser to configure
    sender = input("Enter Your email Id : ")

    for val in range(len(xl_list_of_dict)):
        ## receptionist email from sheet
        to = xl_list_of_dict[val]['Decoded Email']
        ## Get encoded code & username to append in subject line
        encoded_code = str(xl_list_of_dict[val]['Encoded Code'])
        username = xl_list_of_dict[val]['User Name'].lower().replace(" ", "_")
        username_with_code = encoded_code + "_" + username
        subject = "Your course material {}".format(username_with_code)

        ## Create Message Body
        message_text_html = 'Hey {},<br/><br/>Good to see the progress, Please find the attachment of your previous session.<br/><br/>Thank you,<br/>John'.format(
            xl_list_of_dict[val]['User Name'])
        message_text_plain = "Hey {},\n\nGood to see the progress, Please find the attachment of your previous session.\n\nThank you,\nJohn".format(
            xl_list_of_dict[val]['User Name'])

        ## Get Pdf, Add Logo & Content
        pdf_status = SetHeaderFooter(input_pdf_file_path, output_pdf_file_path, logo_path)
        if pdf_status:
            attached_file = output_pdf_file_path
            # with attachment
            status = create_message_and_send(
                sender, to, subject, message_text_plain, message_text_html, attached_file)
        else:
            # without attachment
            status = create_message_and_send(
                sender, to, subject, message_text_plain, message_text_html)

        ## If Mail Sent successfully then Add Status in Dict
        if status:
            print("Mail Sent")
            xl_list_of_dict[val]['Status'] = 'SENT'
        else:
            print("Error")
            xl_list_of_dict[val]['Status'] = 'UNSENT'
    # print(xl_list_of_dict)
    ## Write updated data in same excel sheet
    excel_status = write_to_excel(xl_list_of_dict)


if __name__ == '__main__':
    main()
