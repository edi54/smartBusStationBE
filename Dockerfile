FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 컨테이너 안에서 작업 디렉토리
WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# src/ 포함해서 전체 프로젝트 복사
COPY . .

# src/main.py 실행
CMD ["python", "src/main.py"]