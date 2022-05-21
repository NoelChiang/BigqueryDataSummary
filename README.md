# BigqueryDataSummary

### Languages & Tools
Languages: python, shell script  
Tools: Docker, Jupyter notebook, google cloud service bigquery, firebase hosting

### Use case in a local machine
1. Set google service account auth to correct path
2. execute make_tar.sh to create docker image
3. execute below 
```
docker run --rm -v $hosting:/hosting app_event_handler /my_script.sh -s $sender -p $password -r $receiver -t $token
# $sender = 'Mail address of sender'
# $password = 'Password of sender'
# $receiver = 'Mail address of receiver'
# $token = 'Firebase auth token, for deploying html to hosting'
```
4. (optional) Add command in step3 to crontab for scheduling execution
