FROM python:3.11-slim-bullseye as build
WORKDIR /wheels

COPY requirements.txt /opt/snoop/
RUN apt-get update \
  && apt-get install -y build-essential \
  && pip3 wheel -r /opt/snoop/requirements.txt

FROM python:3.11-slim-bullseye
WORKDIR /opt/snoop

COPY --from=build /wheels /wheels
COPY . /opt/snoop/

RUN pip3 install --no-cache-dir -r requirements.txt -f /wheels \
  && rm -rf /wheels

WORKDIR /opt/snoop

ENTRYPOINT ["python", "snoop.py"]