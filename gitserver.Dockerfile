FROM node:alpine

# Install Git and tini, and install git-http-server globally
RUN apk add --no-cache tini git \
  && yarn global add git-http-server \
  && adduser -D -g git git

# Switch to the git user
USER git
WORKDIR /home/git

RUN git init --bare repository.git && \
    git config --global user.name "chua zhuo en" && \



    git config --global user.email "2302292@sit.singaporetech.edu.sg"


ENTRYPOINT ["tini", "--", "git-http-server", "-p", "3000", "/home/git"]