FROM python:3.10 as requirements-stage
WORKDIR /tmp
RUN pip install poetry==1.5.0
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10
WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Install Poetry in the final images
RUN pip install poetry==1.5.0

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "site_market.wsgi:application"]