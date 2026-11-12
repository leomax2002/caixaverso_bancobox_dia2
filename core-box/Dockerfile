FROM python:3.13-slim-bookworm

WORKDIR /app

COPY requirements.txt .

RUN apt-get update \
    && apt-get install -y --no-install-recommends iputils-ping curl \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --no-cache-dir --upgrade pip "setuptools==84.1.0" wheel \
    && python -m pip install --no-cache-dir -r requirements.txt \
    && python -m pip list | grep setuptools

COPY . .

ENV BOX_AMBIENTE=producao

EXPOSE 8000

RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup appuser \
    && chown -R appuser:appgroup /app

USER appuser

CMD ["gunicorn", "-b", "0.0.0.0:8000", "--workers", "1", "--threads", "4", "wsgi:app"]
