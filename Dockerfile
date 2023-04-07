FROM emmercm/libtorrent:2.0.8-alpine 

WORKDIR /app 

COPY . . 

RUN apk add bash jq curl py3-pip

RUN pip install --no-cache-dir -r requirements.txt 

EXPOSE 8000

# Start the application
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]



