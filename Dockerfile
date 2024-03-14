FROM python:3.10.6-buster
COPY PlatePerfect_2 PlatePerfect_2
COPY requirements.txt requirements.txt
COPY credentials.json credentials.json
#COPY Makefile Makefile
#RUN make reset_local_files
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD uvicorn PlatePerfect_2.api.fast_2:app --host 0.0.0.0 --port $PORT
