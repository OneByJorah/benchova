# =============================================================================
# Ollama Benchmark Dashboard — LLM benchmarking platform
# JorahOne
# =============================================================================
FROM python:3.11-alpine

WORKDIR /app

# Install curl for healthcheck
RUN apk add --no-cache curl=8.22.0-r0

# Copy application
COPY collector/ ./collector/
COPY server.py ./
COPY index.html ./
COPY *.md ./

# Create runtime directories (appuser 1000 owns them)
RUN mkdir -p results outputs data && chown -R 1000:1000 results outputs data

RUN adduser -u 1000 -D appuser

EXPOSE 8081

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["curl", "-f", "http://localhost:8081/"]

USER 1000

# Collect system info on startup
CMD ["sh", "-c", "python3 collector/system_info.py || true; exec python3 server.py"]
