FROM python:3.13.1
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock Makefile ./
RUN uv sync --frozen

CMD ["/bin/bash"]
