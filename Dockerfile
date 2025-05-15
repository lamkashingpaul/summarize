# postgres
FROM postgres:17.5 AS postgres
RUN apt-get update && apt-get install -y \
    postgresql-server-dev-17 \
    gcc \
    make \
    git \
    && git clone https://github.com/pgvector/pgvector.git \
    && cd pgvector && make && make install \
    && cd .. && rm -rf pgvector \
    && apt-get remove --purge -y gcc make git \
    && apt-get autoremove -y \
    && apt-get clean
EXPOSE 5432
