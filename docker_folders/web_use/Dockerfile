# sshd
#
# VERSION               0.0.2

FROM ubuntu:14.04
MAINTAINER Stian Strom Anderssen <s177437@stud.hioa.no>

RUN apt-get update && apt-get install -y python-pip git git-core httperf libwww-perl
RUN pip install pika==0.9.8

##Add commands to modify the image to be able to clone the github repo


ADD ./startup.sh /opt/startup.sh

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
CMD ["/bin/bash", "/opt/startup.sh"]

