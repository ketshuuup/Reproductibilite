FROM gcc:15

WORKDIR /app
COPY exo1.c exo2.c run.sh /app/

RUN gcc -O0 -Wall -ffp-contract=off -o associativity exo1.c
RUN gcc -O0 -Wall -ffp-contract=off -o banking exo2.c -lm

RUN chmod +x run.sh

ENV OUT_DIR=/out

CMD ["./run.sh"]