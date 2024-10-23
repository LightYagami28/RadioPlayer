# Debian Based Docker
FROM debian:latest

# Update the package list and upgrade the existing packages
RUN apt update && apt upgrade -y

# Install necessary packages
RUN apt install -y git curl python3-pip ffmpeg

# Upgrade pip to the latest version
RUN pip3 install --upgrade pip

# Copy the requirements file into the container
COPY requirements.txt /requirements.txt

# Install Python dependencies from requirements.txt
RUN pip3 install --upgrade -r /requirements.txt

# Create the application directory
RUN mkdir /RadioPlayerV3

# Set the working directory
WORKDIR /RadioPlayerV3

# Copy the start script into the container
COPY start.sh /start.sh

# Set the start script as the command to run the bot
CMD ["/bin/bash", "/start.sh"]
