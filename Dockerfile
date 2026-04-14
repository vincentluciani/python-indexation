FROM python:3.11-slim

#WORKDIR /app
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COPY src/extract_information ./extract_information/
# COPY send_information ./send_information/
# COPY src/run_sitemap_to_elastic.py .
# COPY elastic_setup ./elastic_setup/
#RUN chmod +x ./elastic_setup_sh/build_settings.sh
COPY elastic_setup/ ./elastic_setup/
COPY src/ ./src/
COPY config/ ./config/
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
#CMD ["python", "run_sitemap_to_elastic.py"]
