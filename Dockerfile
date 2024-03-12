FROM python:3.10.6-buster
COPY PlatePerfect PlatePerfect
COPY requirements.txt requirements.txt
#COPY Makefile Makefile
#RUN make reset_local_files
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD uvicorn PlatePerfect.api.fast:app --host 0.0.0.0 --port $PORT
