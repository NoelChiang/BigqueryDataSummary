#### Script file to create charts' html, deploy to firebase hosting, then send mail to notify

#!/bin/bash

# Get input parameter for firebase token, mail list for sending notification
while getopts s:r:t:p: option
do 
case ${option} in 
s) mailingargs="${mailingargs}-${option} ${OPTARG} ";;
r) mailingargs="${mailingargs}-${option} ${OPTARG} ";;
t) token="${OPTARG}";;
p) mailingargs="${mailingargs}-${option} ${OPTARG} ";;
esac
done

# Declare project path
webPageDir=hosting

# Set PATH explicitly
export PATH=/usr/local/opt/ruby/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

# Run Untitled.ipynb to update chart and output to html
jupyter nbconvert --ExecutePreprocessor.timeout=1200 --to html --execute Events_Dashboard.ipynb

FILE=error.log
if [ ! -f "$FILE" ]; then
    # If error.log doesn't exist
    # Rename html file and move to hosting folder
    mv Events_Dashboard.html $webPageDir/public/events.html

    # Change folder to hosting project and deploy
    cd $webPageDir
    firebase deploy --token $token
    cd ..
fi

# Send mail to inform users
python3 send_mail.py $mailingargs
rm $FILE
