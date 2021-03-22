FROM python:3.7

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install --upgrade tensorflow tensorflow-probability

# Batch

ADD /requirements.txt ./app/
RUN pip install --no-cache-dir -r app/requirements.txt
ADD *.py ./app/
ADD run.sh ./app/

# Lambda

RUN pip install awslambdaric --target ./app/
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie

# Run

WORKDIR app

ENTRYPOINT ["bash", "run.sh"]
