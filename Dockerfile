FROM python:3.8-slim AS compile-image

RUN apt-get -y update
RUN apt-get install -y --no-install-recommends build-essential gcc

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


FROM compile-image AS build-image

ENV APP_HOME=/app
COPY --from=compile-image . $APP_HOME

ENV USER=app
RUN adduser --system --group $USER

WORKDIR $APP_HOME
COPY . $APP_HOME

RUN chmod +x ${APP_HOME}
USER $USER

CMD uvicorn api:app --reload --host 0.0.0.0 --port 8080

EXPOSE 8080