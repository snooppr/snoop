# vim:set ft=dockerfile:
FROM python:3-alpine

LABEL maintainer="Andrius Kairiukstis <k@andrius.mobi>"

WORKDIR /app

ADD requirements.txt .

RUN pip install --upgrade pip \
&& apk add --virtual .build-dependencies \
           build-base \
					 libxml2-dev \
					 libxslt-dev \
&&  python3 -m pip install -r requirements.txt \
&&  apk del .build-dependencies \
&&  rm -rf /var/cache/apk/* \
           /tmp/* \
           /var/tmp/*

ADD . .

ENTRYPOINT ["/app/docker-entrypoint.sh"]
