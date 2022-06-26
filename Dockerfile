FROM python:3.9-slim-bullseye
EXPOSE 5026
COPY . /server
WORKDIR /server
RUN pip3 install -r requirements.txt
ENV FLASK_APP isamerican_server
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5026"]
