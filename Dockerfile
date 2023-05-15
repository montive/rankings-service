FROM python:3.9.16-bullseye

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 5002
COPY . .
# Run the application:
CMD python app.py