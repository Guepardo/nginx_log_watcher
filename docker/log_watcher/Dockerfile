FROM nginx:latest

RUN apt-get update && apt-get install python python-pip -y
RUN pip install requests

EXPOSE 4000

ENTRYPOINT ["/entrypoint.sh"]
