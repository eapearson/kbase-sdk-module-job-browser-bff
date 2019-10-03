FROM alpine:3.10 as builder
MAINTAINER KBase Developer

# The build stage needs just enough to run the KBase SDK tools.

# update system and system dependencies
RUN apk upgrade --update-cache --available && \
    apk add --update --no-cache apache-ant bash git linux-headers make openjdk8 python3 python3-dev py3-setuptools python2

RUN mkdir -p /kb && \
    git clone --depth=1 https://github.com/kbase/kb_sdk /kb/kb_sdk && \
    cd /kb/kb_sdk && \
    make

COPY ./ /kb/module

RUN mkdir -p /kb/module/work/cache && \
    chmod -R a+rw /kb/module && \
    cd /kb/module && \
    PATH=$PATH:/kb/kb_sdk/bin && \
    make all

# Final image

FROM alpine:3.10
MAINTAINER KBase Developer

# update and add system dependencies
RUN apk upgrade --update-cache --available && \
    apk add --update --no-cache bash g++ git libffi-dev linux-headers make openssl-dev python3 python3-dev py3-setuptools

# install python dependencies for the service runtime.
RUN pip3 install \
    cffi==1.12.3 \
    coverage==4.5.4 \
    jinja2==2.10.1 \
    jsonrpcbase==0.2.0 \
    ndg-httpsclient==0.5.1 \
    nose==1.3.7 \
    python-dateutil==2.8.0 \
    pytz==2019.2 \
    requests==2.22.0 \
    uwsgi==2.0.18 \
    toml==0.10.0 \
    jsonschema==3.0.2

COPY --from=builder /kb/module /kb/module

RUN addgroup --system kbmodule && \
    adduser --system --ingroup kbmodule kbmodule && \
    chown -R kbmodule:kbmodule /kb/module && \
    chmod +x /kb/module/scripts/entrypoint.sh

WORKDIR /kb/module

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
