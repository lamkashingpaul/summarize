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

# redis
FROM redis:8.0.2 AS redis

# api
FROM python:3.13-slim AS api
EXPOSE 80
ENV ENV=production
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
COPY ./api /app
WORKDIR /app
RUN uv sync --frozen --no-cache
CMD ["/app/.venv/bin/fastapi", "run", "src/main.py", "--port", "80"]

# web
FROM node:24.3.0-slim AS web-base
ENV NODE_ENV=production
ENV CI=1
ENV PNPM_HOME=/pnpm
ENV PATH=$PNPM_HOME:$PATH
RUN corepack enable
USER node
WORKDIR /app

FROM web-base AS web-source
COPY --chown=node:node ./web /app

FROM web-source AS web-deps
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --prod --frozen-lockfile

FROM web-source AS web-build
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile
RUN pnpm run build

FROM web-base AS web
EXPOSE 3000
COPY --from=web-build --chown=node:node /app/.next/standalone /app/
COPY --from=web-build --chown=node:node /app/.next/static /app/.next/static
COPY --from=web-build --chown=node:node /app/public /app/public
CMD [ "node", "server.js" ]
