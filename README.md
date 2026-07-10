# AI Executive Assistant

개인 맞춤 AI 전문비서 프로젝트입니다. MP-00은 실행 가능한 모노레포 골격과 로컬 인프라를 제공합니다.

## 구조

- `apps/web`: Next.js 15 + TypeScript 웹 대시보드
- `services/api`: FastAPI 백엔드
- `services/worker`: Celery 작업자
- `infra`: PostgreSQL, Redis, Caddy를 포함한 Docker Compose 설정

## 시작하기

```powershell
Copy-Item .env.example .env
corepack enable
corepack pnpm install
corepack pnpm dev
```

백엔드는 Python 3.12 기준입니다.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e services/api -e services/worker
uvicorn app.main:app --app-dir services/api --reload
```

Docker Compose를 사용할 수 있으면 `docker compose -f infra/docker-compose.yml up --build`로 전체 로컬 스택을 시작할 수 있습니다.

## 품질 명령

```powershell
corepack pnpm lint
python -m pytest services/api/tests services/worker/tests
```

비밀값과 외부 API 토큰은 저장소나 로그에 넣지 않습니다.

