FROM python:3.10
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
## Copy all files from current directory to /app in container
COPY . . 
CMD ["flask", "run", "--host", "0.0.0.0"]