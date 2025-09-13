#!/usr/bin/env bash
set -euo pipefail

# ===== 可調參數 =====
PROJECT_ID="scenic-dynamo-471901-b6"   # 你的 GCP 專案 ID
SERVICE="coachy-api"                   # Cloud Run 服務名稱
REGION="us-central1"                   # 建議 us-central1/ us-east1 / us-west1
IMAGE="gcr.io/${PROJECT_ID}/${SERVICE}"

# ===== 檢查檔案 =====
[[ -f Dockerfile ]] || { echo "❌ 找不到 Dockerfile（請在 repo 根目錄執行）"; exit 1; }
[[ -f main.py ]]    || { echo "❌ 找不到 main.py（請在 repo 根目錄執行）"; exit 1; }

# 顯示關鍵環境變數（僅顯示是否存在）
echo "🔧 檢查 Cloud Run 環境變數（部署時會使用）："
echo "  - CORS_ORIGINS：自行於 Cloud Run 服務設定"
echo "  - API_TOKEN    ：自行於 Cloud Run 服務設定"

# ===== 設定專案 =====
echo "➡️  設定 gcloud 專案為: ${PROJECT_ID}"
gcloud config set project "${PROJECT_ID}" >/dev/null

# 用 git 短版 commit 當作 tag（可追蹤來源）
REV="$(git rev-parse --short HEAD 2>/dev/null || echo manual)"
TAG_IMAGE="${IMAGE}:${REV}"

echo "🏗️  Build & Push: ${TAG_IMAGE}"
gcloud builds submit --tag "${TAG_IMAGE}" .

echo "🚀 Deploy 到 Cloud Run 服務: ${SERVICE}（region=${REGION}）"
gcloud run deploy "${SERVICE}" \
  --image "${TAG_IMAGE}" \
  --platform managed \
  --region "${REGION}" \
  --allow-unauthenticated

# 取得 URL
URL=$(gcloud run services describe "${SERVICE}" --region "${REGION}" --format='value(status.url)')
echo "✅ 部署完成：${URL}"

# 簡單健康檢查
echo "🔍 測試 /health"
curl -s "${URL}/health" || true
echo -e "\n"

echo "📘 Swagger：${URL}/docs"
echo "🔒 受保護路由（需 X-API-Token）：${URL}/secret"
