FROM python:3.7.2-slim
RUN mkdir /mycode

COPY main.py /mycode/

COPY churn_modelo.p /mycode/

COPY churn_recent.db /mycode/

COPY .gitignore /mycode/

COPY requirements.txt /

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python","/mycode/main.py"]
