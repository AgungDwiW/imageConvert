# our base image
FROM python:3.6-alpine

RUN ln -s /usr/lib/x86_64-linux-gnu/libz.so /lib/
RUN ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /lib/
RUN pip install -U pip

RUN apk add --no-cache --virtual .build-deps gcc musl-dev
RUN pip install cython

# install Python modules needed by the Python app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

# copy files required for the app to run
COPY *.py /usr/src/app/

# tell the port number the container should expose
EXPOSE 5000
WORKDIR /usr/src/app

RUN apk del .build-deps gcc musl-dev

# run the application
CMD ["python", "/usr/src/app/run.py"]
