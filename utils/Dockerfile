# Dockerfile — ReputMail Bot
# -------------------------
# Multi‑stage image: builder installs deps into layer, final stage is minimal.

FROM python:3.12-slim AS builder
WORKDIR /app

# Faster installs + no cache clutter
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --user -r requirements.txt

# ───────────────────────────────────────────────────────────────
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:$PATH"

# copy installed libs from builder
COPY --from=builder /root/.local /root/.local

# copy project files
COPY . .

# non‑root user (uid 1001)
RUN adduser --disabled-password --gecos '' botuser \
 && chown -R botuser:botuser /app
USER botuser

CMD ["python", "-m", "app.main"]
