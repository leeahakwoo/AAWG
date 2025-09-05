@echo off
chcp 65001 >nul
title FAISS → ChromaDB 마이그레이션 실행기

echo ========================================
echo 🚀 FAISS → ChromaDB 마이그레이션 시작
echo ========================================
echo.

cd /d "C:\Users\cherr\AAWG"

echo 📦 Python 환경 확인 중...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python이 설치되지 않았거나 PATH에 없습니다.
    pause
    exit /b 1
)

echo.
echo 🔧 마이그레이션 스크립트 실행 중...
python execute_migration.py

echo.
echo ========================================
echo 🎉 마이그레이션 완료!
echo ========================================
echo.
echo 📝 다음 단계:
echo 1. 서버 재시작: cd AAWGA\backend ^&^& python app.py
echo 2. 테스트: http://localhost:8000/api/system/status
echo 3. ChromaDB 웹 UI: cd AAWGA\chroma_db ^&^& python web_server.py
echo.

pause
