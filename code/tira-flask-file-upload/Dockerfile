from python:3.6

RUN pip3 install flask nose approvaltests \
	&& apt-get update \
	&& apt-get install tree
WORKDIR /app
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host=0.0.0.0"]
