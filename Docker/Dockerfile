FROM ubuntu:latest

RUN apt-get update \
 && apt-get install -y \
        git \
        python3 \
        python3-pip \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN pip install \
        copier~=9.2 \
        copier-templates-extensions~=0.3 \
        dbrownell_Common

COPY copier_script copier_script

ENTRYPOINT ["./copier_script"]
