FROM python:3.9-buster
EXPOSE 8081
WORKDIR /app

RUN python -m pip install --upgrade pip && \
    python -m pip install --upgrade setuptools && \
    python -m pip install --upgrade wheel

COPY ./requirements.txt /app
RUN python -m pip install -r requirements.txt

# Added this because of huggingface_hub issue
RUN pip install huggingface_hub

# Add app files
ADD app /app

ENTRYPOINT [ "gunicorn" ]