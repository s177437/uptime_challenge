# sshd
#
# VERSION               0.0.2

FROM ubuntu:14.04
MAINTAINER Stian Strom Anderssen <s177437@stud.hioa.no>

ENV TERM xterm
RUN apt-get update && apt-get install -y python-pip git git-core httperf libwww-perl
RUN pip install pika==0.9.8
RUN pip install httplib2
RUN pip install beautifulsoup

##Add commands to modify the image to be able to clone the github repo

ADD ./startup.sh /opt/startup.sh

CMD ["/bin/bash", "/opt/startup.sh"]

