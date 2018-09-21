FROM python:3-alpine

LABEL name CMSeeK
LABEL src "https://github.com/Tuhinshubhra/CMSeeK"
LABEL creato Tuhinshubhra
LABEL dockerfile_maintenance khast3x
LABEL desc "CMS Detection and Exploitation suite - Scan WordPress, Joomla, Drupal and 130 other CMSs."


RUN apk add --no-cache git py3-pip && git clone https://github.com/Tuhinshubhra/CMSeeK

WORKDIR CMSeeK
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "cmseek.py" ]
