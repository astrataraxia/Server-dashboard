# 🖥️ 실시간 리눅스 서버 상태 대시보드

> **[🚀 Live Demo 바로가기](https://astral-ataraxia.com)**

---

## 1. 🎯 프로젝트 핵심

이 프로젝트는 **'실시간으로 동작하는' 라이브 서비스**를 통해 서버의 상태를 보여주는 Dashboard 구현 프로젝트이다.

1.  **인프라 운영:** 리눅스 서버를 안정적으로 세팅하고 24/7 운영하는 능력.
2.  **보안 구성:** 포트포워딩 없이, Cloudflare Zero Trust Tunnel을 활용해 외부 공격 표면(Attack Surface) 없이 서비스를 안전하게 노출하는 인프라 구성.
3.  **백엔드 개발:** Python(FastAPI)을 사용해 시스템 리소스를 처리하고, 경량 API를 구축하는 능력.
4.  **프론트엔드 시각화:** Vanilla JS를 활용해 API 데이터를 받아 시각화하는 능력.

<br>

## 2. 💎 MVP 핵심 기능 (Features)

이 대시보드는 서버의 핵심 상태를 실시간으로 보여주는 것에 집중합니다.

* **실시간 CPU 사용률:** 현재 CPU 부하를 동적 그래프로 시각화
* **실시간 메모리 사용률:** 전체 메모리 대비 현재 사용량을 %와 그래프로 시각화
* **서버 가동 시간 (Uptime):** 서버가 마지막 재부팅 후 얼마나 오래 안정적으로 운영되었는지 표시
* **디스크 사용량:** 루트(/) 파티션의 디스크 사용 현황 표시

<br>

## 3. 🛠️ 기술 스택 및 아키텍처 (Tech Stack & Architecture)

경량(Lightweight) 스택을 사용하여, 최소한의 리소스로 성능을 내도록 설계하였습니다.

### Architecture
1.  **Cloudflare Zero Trust:** 외부 IP 노출이나 포트 개방 없이, Cloudflare의 터널링을 통해서만 `domain` 트래픽을 내부 서버의 FastAPI 앱으로 안전하게 전달합니다.
2.  **FastAPI (Backend):** 8000번 포트(내부)에서 실행되며, 시스템 정보 조회 API 제공.
4.  **Static Files (Frontend):** Nginx 또는 FastAPI 자체의 Static Mount 기능을 이용해 `index.html`, `main.js` 서빙.

### Tech Stack
* **Backend:**
    * Python 3.13+
    * **FastAPI:** 비동기 처리가 가능한 고성능 경량 웹 프레임워크
    * **psutil:** OS의 프로세스 및 시스템 정보(CPU, Mem 등)를 가져오기 위한 핵심 라이브러리
    * **Uvicorn:** ASGI 서버
* **Frontend:**
    * Vanilla HTML5 / CSS3
    * **Vanilla JavaScript (ES6+):** `fetch` API를 사용한 비동기 데이터 요청
    * **Chart.js:** 실시간 데이터 시각화를 위한 경량 차트 라이브러리
* **Infrastructure:**
    * Linux (Rocky Linux)
    * Cloudflare Zero Trust Tunnel

<br>

## 4. 📊 API 엔드포인트 명세

이 대시보드가 사용하는 백엔드 API 명세입니다.

**`GET /api/v1/status`**

* **Description:** 서버의 현재 CPU, 메모리, 디스크, 가동 시간 정보를 반환합니다.
* **Success Response (200 OK):**