# Base OS
FROM python:3.8.6-slim-buster
# Copy static resources to root folder
COPY send_mail.py ./
COPY setting.py ./
COPY Events_Dashboard.ipynb ./
COPY MyModule/ ./MyModule/
COPY resources/ ./resources/
COPY my_script.sh ./
# Copy google service account auth json
COPY GoogleServiceAccountAuth.json ./
# Used for installing firebase.tool, and install chinese font
RUN apt-get update
RUN apt-get install -y \
    sudo \
    curl \
    --no-install-recommends fonts-wqy-zenhei \
    && apt-get clean && fc-cache -fv
# Install python library
RUN pip3 install pandas==1.1.3
RUN pip3 install matplotlib==3.3.2
RUN pip3 install seaborn==0.11.0
RUN pip3 install jupyter 
RUN pip3 install google-cloud-bigquery
RUN pip3 install pyarrow
RUN pip3 install db-dtypes
# Install firebase tool
RUN curl -sL https://firebase.tools | bin/bash
# Get script file permission
RUN chmod +x my_script.sh
# Create charts folder to save output image file
RUN mkdir charts

