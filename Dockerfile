# Dockerfile, Image, Container
FROM python:3.11-bookworm
RUN apt-get update && apt-get install -y network-manager
RUN mkdir /adwel
WORKDIR /adwel

COPY init/ /init/
ADD core/ /core/
ADD scraper/ /scraper/
COPY requirements.txt ./

# ARG src="Posthoorn.nmconnection"
# ARG target="/etc/NetworkManager/system-connections/Posthoorn VPN.nmconnection"
# COPY ${src} ${target}
# RUN chmod -R 600 '/etc/NetworkManager/system-connections/Posthoorn VPN.nmconnection'
# RUN chown -R root:root '/etc/NetworkManager/system-connections/Posthoorn VPN.nmconnection'
# RUN nmcli con up '/etc/NetworkManager/system-connections/Posthoorn VPN.nmconnection'
# RUN nmcli con up 'Posthoorn VPN'

RUN pip install --no-cache-dir -r requirements.txt


ENV PATH="/usr/sbin:${PATH}"
# Define an environment variable for the outside folder path (you can customize this)
ENV MOUNT_POINT /outside

CMD [ "python", "/scraper/scraper.py" ]

# docker build --no-cache -t adwel .
# docker run -v C:/Users/Jules/Code/mnt:/outside adwel