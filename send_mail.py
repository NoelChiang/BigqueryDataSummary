import smtplib, ssl, sys, getopt
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import datetime 
import setting
import os.path as path

receiver = ""
sender = ""
password = ""

# Reset sender/receiver by input arguments
try:
    opts, arg = getopt.getopt(sys.argv[1:], 's:r:p:')
except:
    print('getting sender and receiver failed')
for opt, val in opts:
    if opt == '-s':
        # Sender's email
        sender = val
    elif opt == '-r':
        # Receiver's email (separated by ",")
        receiver = val
    elif opt == '-p':
        # Sender's email password
        password = val

# Gmail ssl port
port = 465  

# Gmail smtp server
smtp_server = "smtp.gmail.com"  

# Create MIME message object
message = MIMEMultipart("alternative")

# Declare receiver list
receiver_list = []

if path.exists('error.log'):
    # If error.log exist, send error log only to me
    message['Subject'] = 'friDay shopping app event summary error'
    with open('error.log', 'r') as log:
        error = MIMEText(log.read())
        message.attach(error)
    receiver_list = ['<# My Email Address #>']
else:
    # If error log not exist, follow normal procedure
    # Add Subject, From, To information
    # Attach html info and attachment info
    today = datetime.datetime.today()
    message["Subject"] = "Events' summary: {0}".format(str(today.year)+'/'+str(today.month)+'/'+str(today.day))
    message["From"] = sender
    message['To'] = receiver

    # Create comment's icon image and html content
    htmlCommentInfoStr = ''
    with open('positive_comment.txt', 'r') as f:
        comments = f.read().split(',')
        htmlContents = ''
        for comment in comments:
            htmlContents += '<h4 style="color:green">{0}</h4>'.format(comment)
        if len(comments) != 0:
            with open('resources/positive.png', 'rb') as image_file:
                image = MIMEImage(image_file.read())
                image.add_header('Content-ID', '<positive-icon>')
            message.attach(image)        
            htmlCommentInfoStr += '<img src="cid:positive-icon" width="75"><br>{0}<br>'.format(htmlContents)
    with open('negative_comment.txt', 'r') as f:
        comments = f.read().split(',')
        htmlContents = ''
        for comment in comments:
            htmlContents += '<h4 style="color:red">{0}</h4>'.format(comment)
        if len(comments) != 0: 
            with open('resources/negative.png', 'rb') as image_file:
                image = MIMEImage(image_file.read())
                image.add_header('Content-ID', '<negative-icon>')
            message.attach(image)      
            htmlCommentInfoStr += '<img src="cid:negative-icon" width="75"><br>{0}<br>'.format(htmlContents)


    # Get attachment info from setting 
    # Set attached image to message object
    htmlAttachInfoStr = ''
    for chart in setting.get_mail_notify_attachments():
        htmlAttachInfoStr += '<img src="cid:{0}" width="800"><br>'.format(chart)
        with open(chart, 'rb') as image_file:
            image = MIMEImage(image_file.read())
            image.add_header('Content-ID', '<{0}>'.format(chart))
        message.attach(image)

    # Set html content
    html = """
    <html>
        <body>
            <p>Hi All</p>
            <p>Please cheack today's summary below</p>
            <p>For more details, click <a href='<# My hosting url #>'>here</a>
            <br>
            {0}
            {1}
        </body>
    </html>
    """.format(htmlCommentInfoStr, htmlAttachInfoStr)
    part = MIMEText(html, "html")
    message.attach(part)

    # Set receiver list
    receiver_list = receiver.split(',')

# Generate SSL connection, login sender gmail and send message
# Message needs to be converted to string format
context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender, password)
    server.sendmail(sender, receiver_list, message.as_string())