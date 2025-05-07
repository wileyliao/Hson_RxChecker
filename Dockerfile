FROM python:3.10

WORKDIR /app

# 複製 requirements.txt 並安裝 Python 套件
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt


# 設定環境變數
ENV FLASK_APP=rx_checker_app.py
ENV FLASK_ENV=production

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:3001", "rx_checker_app:app"]
