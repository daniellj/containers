FROM alpine:latest

EXPOSE 2222

RUN apk add --no-cache openssh
COPY /config-files/sshd_config /etc/ssh/
COPY /config-files/start.sh /usr/bin/

# adjust/clean format shell script file
RUN sed -i -e 's/\r$//' /etc/ssh/sshd_config
RUN sed -i -e 's/\r$//' /usr/bin/start.sh

# create a user admin
RUN addgroup admin
RUN adduser -D -H admin -G admin
RUN echo "admin:admin" | chpasswd

RUN mkdir /home/admin
RUN chown root:root /home/admin
RUN chmod 755 /home/admin
RUN mkdir /home/admin/data
RUN chown admin:admin /home/admin/data
RUN chmod 700 /home/admin/data

# Default is to run the OpenSSH server
ENTRYPOINT ["/usr/bin/start.sh"]