FROM python:3.7-slim
EXPOSE 80

WORKDIR /usr/src/project

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic

CMD ["sh", "-c", "gunicorn -b '0.0.0.0:80' expensesproject.wsgi:application"]
