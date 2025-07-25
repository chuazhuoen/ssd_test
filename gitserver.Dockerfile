USER git
WORKDIR /home/git

RUN git init --bare repository.git && \
    git config --global user.name "chua zhuo en" && \
    git config --global user.email "2302292@sit.singaporetech.edu.sg"

ENTRYPOINT ["tini", "--", "git-http-server", "-p", "3000", "/home/git"]
