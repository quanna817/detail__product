FROM python:3.11-buster

RUN mkdir app
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY main.py /app/
COPY database.py /app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

# ENV PATH="${PATH}:/root/.local/bin"
# ENV PYTHONPATH=.

# COPY requirements.txt .
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# COPY src/ .