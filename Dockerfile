#Use an official Python runtime as a parent image
FROM python:2.7-slim

COPY requirements.txt ./
COPY api-paste.ini ./
COPY psn ./psn

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 3310 available to the world outside this container
EXPOSE 3310

# Run app.py when the container launches
CMD ["gunicorn", "--paste", "api-paste.ini"]