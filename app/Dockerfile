#
FROM python:3.8

ENV PYTHONUNBUFFERED=1
# 
WORKDIR /code

# 
COPY requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
ENV PYTHONPATH=/code

#
EXPOSE 8000