FROM python:3

WORKDIR /discovery_agent_service

COPY requirements.txt /discovery_agent_service
COPY config/config.ini /discovery_agent_service
COPY . .

RUN pip3 install -r requirements.txt
RUN sourcce init.sh
RUN mkdir -p /root/.ssh
RUN chmod 0700 /root/.ssh
RUN ssh-keyscan example.com > /root/.ssh/known_hosts

ENV REPEAT_TIMER 30
ENV CONF_FILE .

CMD [ "python", "./main.py" ]
