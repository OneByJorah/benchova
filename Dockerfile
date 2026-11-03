# =============================================================================
# benchova — LLM benchmarking platform
# JorahOne
# =============================================================================
FROM python:3.11-alpine

WORKDIR /app

# Install curl for healthcheck
# Exact Alpine versions disappear from the repository, which breaks the build
# hadolint ignore=DL3018
RUN apk add --no-cache curl

# Copy application
COPY collector/ ./collector/
COPY index.html ./
COPY *.md ./

# Create runtime directories
RUN mkdir -p results outputs data && chown -R 1000:0 results outputs data

RUN adduser -u 1000 -D appuser

EXPOSE 8081

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD ["curl", "-f", "http://localhost:8081/"]

USER 1000

# Collect system info, then serve the dashboard on 8081
CMD ["sh", "-c", "python3 collector/system_info.py > results/system_info.json || true; exec python3 -m http.server \"${DASHBOARD_PORT:-8081}\" --bind \"${DASHBOARD_HOST:-0.0.0.0}\""]
