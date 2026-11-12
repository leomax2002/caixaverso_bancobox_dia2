FROM python:3.12-slim-bookworm

WORKDIR /app

COPY requirements.txt .

RUN apt-get update \
    && apt-get install -y --no-install-recommends iputils-ping curl \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && python -m pip install --no-cache-dir --upgrade "setuptools==78.1.1" \
    && python -c "import setuptools; print(setuptools.__version__); assert setuptools.__version__ == '84.1.0'"

COPY . .

ENV BOX_AMBIENTE=producao

EXPOSE 8000

RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup appuser \
    && chown -R appuser:appgroup /app

USER appuser

CMD ["gunicorn", "-b", "0.0.0.0:8000", "--workers", "1", "--threads", "4", "wsgi:app"]
