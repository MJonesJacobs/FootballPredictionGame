
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import ssl
import pandas as pd
import imaplib
from db_link import PredictionData
from web_scrape import GameweekFixtures,FixtureData
SMTP_PORT   = 465
SMTP_SERVER = 'smtp.gmail.com'

IMAP_PORT   = 993
IMAP_SERVER = 'imap.gmail.com'
with open(r"C:\Users\JONESMO1\OneDrive - Jacobs\Documents\email_pass.txt", "r") as f:
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


def send_completed_predictions_email(season:str,gw:int):
    
    fixtures = GameweekFixtures(season,gw)
    players = ["Matt","Simon"]
    predictions = dict()
    for fixture in fixtures.fixtures:
        predictions[fixture]={}
        for player in players:
            predictions[fixture][player] = PredictionData(fixture,player)
           
    #Generate df for HTML Table
    table_df = pd.DataFrame(columns=[f'{players[0]} Prediction',"Fixture",f'{players[1]} Prediction'])
    for i,fixture in enumerate(fixtures.fixtures):
        table_df.loc[i] = [str(predictions[fixture][players[0]]),fixture.fixture_str(),str(predictions[fixture][players[1]])]
    
    subject = f"Premier League Predictions Game {fixture.season} - Gameweek {fixtures.gw} Predictions Complete"   
    recipients = ["modj1999@gmail.com","jonessimon12@sky.com"]
    msg = MIMEMultipart()
    msg["From"]     = MY_ADDRESS
    msg["To"]       = ", ".join(recipients)
    msg["subject"]  = subject
    html = """\
    <html>
    <head></head>
    <body>
        {0}
    </body>
    </html>
    """.format(table_df.to_html(index=False,escape=False))

    
    part1 = MIMEText(html, 'html')
    msg.attach(part1)

    try:
        print("Connecting to Server...")
        with smtplib.SMTP_SSL(SMTP_SERVER,SMTP_PORT,context=ssl.create_default_context()) as smtp:
            smtp.login(MY_ADDRESS,PASSCODE)
            print("Connection Successful!")
            print(f"Sending Email")
            smtp.sendmail(MY_ADDRESS,recipients,msg.as_string())
            print(f"Email Sent")
    except Exception as e:
        print(e)


def send_completed_results_email(season:str,gw:int):
    
    fixtures = GameweekFixtures(season,gw)
    players = ["Matt","Simon"]
    predictions = dict()
    for fixture in fixtures.fixtures:
        predictions[fixture]={}
        for player in players:
            predictions[fixture][player] = PredictionData(fixture,player)
           
    #Generate df for HTML Table
    table_df = pd.DataFrame(columns=[f'{players[0]} Prediction',f'{players[0]} Score',"Result",f'{players[1]} Prediction',f'{players[1]} Score'])
    for i,fixture in enumerate(fixtures.fixtures):
        table_df.loc[i] = [str(predictions[fixture][players[0]]),str(predictions[fixture][players[0]].points),fixture.result_str(),str(predictions[fixture][players[1]]),str(predictions[fixture][players[1]].points)]
    
    subject = f"Premier League Predictions Game {fixture.season} - Gameweek {fixtures.gw} Predictions Complete"   
    recipients = ["modj1999@gmail.com","jonessimon12@sky.com"]
    msg = MIMEMultipart()
    msg["From"]     = MY_ADDRESS
    msg["To"]       = ", ".join(recipients)
    msg["subject"]  = subject
    html = """\
    <html>
    <head></head>
    <body>
        {0}
    </body>
    </html>
    """.format(table_df.to_html(index=False,escape=False))

    
    part1 = MIMEText(html, 'html')
    msg.attach(part1)

    try:
        print("Connecting to Server...")
        with smtplib.SMTP_SSL(SMTP_SERVER,SMTP_PORT,context=ssl.create_default_context()) as smtp:
            smtp.login(MY_ADDRESS,PASSCODE)
            print("Connection Successful!")
            print(f"Sending Email")
            smtp.sendmail(MY_ADDRESS,recipients,msg.as_string())
            print(f"Email Sent")
    except Exception as e:
        print(e)




if __name__ == "__main__":
    

    send_completed_results_email("24/25",3)
