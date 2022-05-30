FROM python:3.9.12

WORKDIR /tmp/app
COPY source/py/requirements.txt ./
RUN python -m pip install pip --upgrade && \
    pip install --no-cache-dir -r requirements.txt

WORKDIR /tmp/app/data
WORKDIR /tmp/app/
COPY source/py/main.py ./

CMD [ "python", "main.py" ]