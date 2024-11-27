# Use the official Python 3.9 slim-buster image as the base image
FROM python:3.9-slim-buster

# Set the working directory in the container to /python-docker
WORKDIR /python-docker

# Copy the requirements.txt file from the host machine to the container
COPY requirements.txt requirements.txt

# Upgrade pip and install the Python dependencies listed in requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all files from the current directory (on the host) to the container
COPY . .
EXPOSE 8080
# Define the default command to run the Flask app, accessible from any network interface
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
