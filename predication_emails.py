
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import ssl

import imaplib


SMTP_PORT   = 465
SMTP_SERVER = 'smtp.gmail.com'

IMAP_PORT   = 993
IMAP_SERVER = 'imap.gmail.com'
with open('C:\email_info\modj.txt', "r") as f:
    PASSCODE = f.read()

MY_ADDRESS = 'modj1999@gmail.com'

def search_for_replies(connection:imaplib.IMAP4_SSL, subject):
  """Returns all messages that are replies to an email with the given subject.

  Args:
    connection: An imaplib.IMAP4 object.
    subject: The subject of the email to search for replies to.

  Returns:
    A list of message numbers.
  """

  # Create a search command.
  command = 'SUBJECT "%s"' % subject

  # Send the search command to the server.
  response = connection.search(command)

  # Check for errors.
  if response[1] != 'OK':
    raise RuntimeError('Error searching for messages: %s' % response[1])

  # Get the message numbers.
  message_numbers = response[0].split()

  return message_numbers

def fixture_formatted(gameweek_fixtures:list[list[str]])->str:
    formatted_list = []
    for home,away in gameweek_fixtures:
        formatted_list.append(f"{home} Vs. {away}")
    return "\n".join(formatted_list)


def send_fixtures(player_list:list[str],gameweek:int,gameweek_fixtures:list[list[str]]):
    subject = f"Premier League Predictions Game - Gameweek {gameweek} Fixtures"
    body = f"Please return your score results by replying to this email and filling out the spaces in the fixture list:\nGameweek {gameweek} Fixtures:\n{fixture_formatted(gameweek_fixtures)}"
    for name, player_email in player_list:
        msg = MIMEMultipart()
        msg["From"]     = MY_ADDRESS
        msg["To"]       = player_email
        msg["subject"]  = subject
        msg.attach(MIMEText(body,'plain'))
        text = msg.as_string()
        try:
            print("Connecting to Server...")
            with smtplib.SMTP_SSL(SMTP_SERVER,SMTP_PORT,context=ssl.create_default_context()) as smtp:
                smtp.login(MY_ADDRESS,PASSCODE)
                print("Connection Successful!")
                print(f"Sending Email to {player_email}")
                smtp.sendmail(MY_ADDRESS,player_email,text)
                print(f"Email Sent to {player_email}")
        except Exception as e:
            print(e)
    
def read_predictions(gameweek:int):
    connection = imaplib.IMAP4_SSL(IMAP_SERVER)
    connection.login(MY_ADDRESS,PASSCODE)
    try:
        connection.select("INBOX")
        result, data = connection.search(None, 'SUBJECT "Premier League Predictions Game"')
        for num in data[1]:
            subject = connection.fetch(num, "(RFC822)")[1][0][1]
            print(subject)
    finally:
        connection.close()