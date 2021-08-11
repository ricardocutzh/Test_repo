FROM ubuntu:20.04

RUN apt update

WORKDIR /home

COPY scripts/job1.sh job1.sh

RUN chmod +x job1.sh

ENTRYPOINT [ "bash", "-c" ]

CMD [ "/home/job1.sh 1 2 3 4 5 6 7 8 9 10 11 12 13" ]