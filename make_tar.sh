# Used to create docker image and tar file
docker build -t app_event_handler .
docker save app_event_handler > app_event_handler.tar