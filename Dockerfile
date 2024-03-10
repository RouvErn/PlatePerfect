FROM python:3.10.6-buster
COPY PlatePerfect /PlatePerfect
COPY requirements_prod.txt requirements.txt
COPY setup.py setup.py
#COPY Makefile Makefile
#RUN make reset_local_files
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install .
CMD uvicorn PlatePerfect.api.fast:app --host 0.0.0.0
