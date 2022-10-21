import speech_recognition as sr
import pyttsx3 as pt
import smtplib
import ssl
from email.message import EmailMessage
import imaplib
import email

listener=sr.Recognizer()
engine=pt.init()
newVoiceRate = 150
engine.setProperty('rate',newVoiceRate)
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
sender='assistant.bot12@gmail.com'
password='zraurjgohwmmxukm'
imap =imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(sender,password)
error_count = 0
cmd=''

#-------------------------------SPEECH----------------------------------------------------
def talk(talk):
    print(talk)
    engine.say(talk)
    engine.runAndWait()

#--------------------------TYPING BY KEYBOARD---------------------------------------------
def get_input():
    global error_count
    error_count=0
    talk('Type below')
    value=input()
    return value

#-------------------------------MICROPHONE------------------------------------------------
def get_info():
    try:
        with sr.Microphone() as source:
            talk('listening...')
            listener.adjust_for_ambient_noise(source)
            voice=listener.listen(source,10,10)
            info=listener.recognize_google(voice)
            return info.lower()
    except:
        talk("I can't reach it.")
        return None

#-----------------------------SENDING EMAILS----------------------------------------------
def Sending_Emails():
    talk("Whom do you wanna send?")
    receiver_resp=get_conformation()
    receiver = receiver_resp.lower()
    talk("Subject of the email.")
    subject_resp=get_conformation()
    subject = subject_resp.capitalize()
    talk("What mail do you wanna send.")
    body_resp=get_conformation().capitalize()
    body = body_resp

    em = EmailMessage()
    em['From'] = sender
    em['To'] = receiver
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender, password)
            smtp.sendmail(sender, receiver, em.as_string())
        talk('Email sent successfully!')
    except:
        talk("Something went wrong")

#-----------------------------READING EMAILS----------------------------------------------
def Read_Emails():
    imap.select("Inbox")
    _, msgnums = imap.search(None, "UNSEEN")
    for msgnum in msgnums[0].split():
        _, data = imap.fetch(msgnum, "(RFC822)")
        _, b = data[0]
        message = email.message_from_bytes(b)
        talk(f"You recevied this mail from : {message.get('From')}")
        talk(f"This recevied mail at : {message.get('Date')}")
        talk(f"Subject is : {message.get('Subject')}")
        talk("Body of mail :")
        for part in message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                k = (body.decode())
                talk(k)

    imap.close()

#-----------------------------GETTING CONFIRMATION----------------------------------------
def get_conformation():
    global error_count
    global cmd
    if error_count<2:
        global command
    command = get_info()
    if error_count<2 and command!=None:
        talk(command)
        talk("Is it right?")
        result=get_info()
        if "yes" in result:
            talk("OK")
            cmd=command
        else:
            error_count+=1
            talk("Try again!")
            command=get_conformation()
            cmd=command
    elif error_count<2 and command==None:
        talk("Please, give some response")
        error_count += 1
        command = get_conformation()
        cmd = command

    else:
        talk("You can also use keyboard.")
        command=get_input()
        cmd=command
    return cmd

talk("Welcome to Voice Based Email Assistant.")
talk("Select the options : ")
talk('''1. Send Email
2. Read Emails''')
confirm=get_conformation()
if '1' in confirm or 'send email' in confirm or 'first one' in confirm:
    Sending_Emails()
elif '2' in confirm or 'read emails' in confirm or 'second one' in confirm:
    Read_Emails()
else:
    talk("Sorry, Select correct one")