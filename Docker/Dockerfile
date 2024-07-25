FROM ubuntu:latest

RUN apt-get update \
 && apt-get install -y \
        git \
        python3 \
        python3-pip \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN ln /usr/bin/python3 /usr/bin/python

RUN pip install \
        copier~=9.2 \
        copier-templates-extensions~=0.3 \
        dbrownell_Common

COPY ImageContent .

ENV PATH="$PATH:/minisign"

RUN git config --global user.email "you@example.com"
RUN git config --global user.name "Your Name"

ENTRYPOINT ["./copier_script"]
