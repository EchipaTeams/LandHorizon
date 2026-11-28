# The API only: Python 3.14 and the locked dependencies. The COGs are not in the image; docker-compose.yml
# mounts them from a volume at /app/data/processed, where api/main.py looks for them.
FROM python:3.14-slim

# rasterio's wheel bundles GDAL but links to the system's libexpat, which the slim image lacks.
RUN apt-get update && apt-get install -y --no-install-recommends libexpat1 && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.13.7 /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=never
WORKDIR /app

# Dependencies first, so a code change doesn't reinstall them. --no-dev: no pytest in the image.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY api/ api/
RUN useradd --system --no-create-home api
USER api
EXPOSE 8000
CMD ["/app/.venv/bin/fastapi", "run", "api/main.py", "--host", "0.0.0.0", "--port", "8000"]
