# 使用官方 Python 輕量版
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 先安裝套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式碼
COPY . .

# Cloud Run 會自動給 PORT 環境變數
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT}
