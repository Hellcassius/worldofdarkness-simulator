## https://cloud.google.com/appengine/docs/flexible/custom-runtimes/
FROM gcr.io/google-appengine/python

# Create a virtualenv for dependencies. This isolates these packages from
# system-level packages.
# Use -p python3 or -p python3.7 to select python version. Default is version 2.
RUN virtualenv /env

# Setting these environment variables are the same as running
# source /env/bin/activate.
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# Copy the application's requirements.txt and run pip to install all
# dependencies into the virtualenv.
ADD requirements.txt /app/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt

# Add the application source code.
ADD . /app
RUN ls
RUN echo $PORT

# Run a WSGI server to serve the application. gunicorn must be declared as
# a dependency in requirements.txt.
## https://stackoverflow.com/questions/10855197/gunicorn-worker-timeout-error
CMD gunicorn -t 90 -b :$PORT main:app
# CMD gunicorn -t 90 -b :8080 app:app