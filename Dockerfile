FROM centos:8
RUN dnf update -y 
RUN dnf install -y python3
RUN curl https://bootstrap.pypa.io/get-pip.py | python3
RUN mkdir -p /app
WORKDIR /app
COPY requirements.txt . 
RUN pip install -r requirements.txt
COPY . . 

ENTRYPOINT [ "python3", "snoop.py"]
