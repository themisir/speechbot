FROM python:3.11.6-slim-bookworm AS base
LABEL authors="Misir Jafarov"
WORKDIR /app
RUN apt-get update && apt-get install -y \
    ffmpeg
RUN python --version

FROM base AS dependencies
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt

FROM dependencies AS final
COPY *.py .
CMD python3 main.py