FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY extract_information ./extract_information/
COPY send_information ./send_information/
COPY main.py .
COPY elastic_setup ./elastic_setup/
#RUN chmod +x ./elastic_setup_sh/build_settings.sh

#CMD ["python", "main.py"]
