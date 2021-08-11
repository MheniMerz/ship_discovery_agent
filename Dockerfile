FROM python:3

WORKDIR /discovery_agent_service

COPY requirements.txt /discovery_agent_service
COPY config/config.ini /discovery_agent_service
COPY ./init.sh
COPY . .

RUN pip3 install -r requirements.txt
RUN mkdir -p /root/.ssh
RUN chmod 0700 /root/.ssh
RUN ssh-keyscan example.com > /root/.ssh/known_hosts

ENV REPEAT_TIMER 30
ENV CONF_FILE .

ENTRYPOINT ["init.sh"]
CMD [ "python3", "main.py" ]
