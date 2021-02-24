FROM python:3.7

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install --upgrade tensorflow tensorflow-probability

# Batch

ADD /requirements.txt ./app/
RUN pip install --no-cache-dir -r app/requirements.txt
ADD *.py ./app/
ADD run.sh ./app/

# Run

WORKDIR app

ENTRYPOINT ["bash", "run.sh"]
