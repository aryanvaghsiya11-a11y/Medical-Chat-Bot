FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the application code
COPY . /code/

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose port 7860 for Hugging Face Spaces
EXPOSE 7860

# Run gunicorn on port 7860
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]
