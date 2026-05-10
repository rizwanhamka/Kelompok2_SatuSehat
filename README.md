# SATU SEHAT API

Backend API sederhana berbasis **Python + Flask** untuk simulasi integrasi dengan platform **SATU SEHAT Sandbox** menggunakan standar **FHIR R4**.

---

# Features

- OAuth2 Token Generator
- Search Patient by NIK
- Search Practitioner by NIK
- Create Location
- Create Encounter
- Swagger Documentation
- FHIR R4 Integration

---

# Tech Stack

| Layer             | Teknologi                 |
| ----------------- | ------------------------- |
| Language          | Python 3                  |
| Framework         | Flask                     |
| API Documentation | Flasgger / Swagger        |
| HTTP Client       | requests                  |
| API Standard      | FHIR R4                   |
| Authentication    | OAuth2 Client Credentials |

---

# Project Structure

```bash
project/
│
├── app.py
├── requirements.txt
└── README.md
```

---

# Installation

## 1. Clone Repository

```bash
git clone <repository-url>
cd project
```

---

## 2. Create Virtual Environment

### Linux / MacOS

```bash
python -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# requirements.txt

```txt
flask
flasgger
requests
```

---

# Running Application

```bash
python app.py
```

Server berjalan di:

```bash
http://127.0.0.1:5000
```

Swagger Documentation:

```bash
http://127.0.0.1:5000/apidocs
```

---

# SATU SEHAT Flow

```text
[1] Generate OAuth2 Token
        ↓
[2] Search Patient by NIK
        ↓
[3] Search Practitioner by NIK
        ↓
[4] Create Location
        ↓
[5] Create Encounter
```

---

# Configuration

Konfigurasi berada di dalam file `app.py`.

```python
AUTH_URL
BASE_URL
CLIENT_ID
CLIENT_SECRET
ORG_ID
NIK_PASIEN
NIK_DOKTER
```

---

# API Endpoints

| Method | Endpoint        | Description                |
| ------ | --------------- | -------------------------- |
| GET    | `/patient`      | Search patient by NIK      |
| GET    | `/practitioner` | Search practitioner by NIK |
| POST   | `/location`     | Create location            |
| POST   | `/encounter`    | Create encounter           |
| GET    | `/apidocs`      | Swagger UI                 |

---

# 1. Search Patient by NIK

## Endpoint

```http
GET /patient
```

## Example Request

```bash
curl http://127.0.0.1:5000/patient
```

## Example Response

```json
{
  "resourceType": "Bundle",
  "total": 1,
  "entry": [
    {
      "resource": {
        "id": "P02280547535",
        "resourceType": "Patient"
      }
    }
  ]
}
```

---

# 2. Search Practitioner by NIK

## Endpoint

```http
GET /practitioner
```

## Example Request

```bash
curl http://127.0.0.1:5000/practitioner
```

## Example Response

```json
{
  "resourceType": "Bundle",
  "total": 1,
  "entry": [
    {
      "resource": {
        "id": "10006926841",
        "resourceType": "Practitioner"
      }
    }
  ]
}
```

---

# 3. Create Location

## Endpoint

```http
POST /location
```

## Example Request

```bash
curl -X POST http://127.0.0.1:5000/location
```

## Example Response

```json
{
  "id": "dc01c797-547a-4e4d-97cd-4ece0630e380",
  "resourceType": "Location",
  "status": "active"
}
```

---

# 4. Create Encounter

## Endpoint

```http
POST /encounter
```

## Example Request

```bash
curl -X POST http://127.0.0.1:5000/encounter
```

## Example Response

```json
{
  "id": "326ae5b2-6ca9-4678-b36a-5d5335843def",
  "resourceType": "Encounter",
  "status": "arrived"
}
```

---

# Swagger Documentation

Swagger UI tersedia di:

```bash
http://127.0.0.1:5000/apidocs
```

Fitur Swagger:

- Interactive API Testing
- Request & Response Schema
- Endpoint Documentation
- Try It Out API

---

# OAuth2 Authentication

API menggunakan:

```text
OAuth2 Client Credentials
```

Endpoint token:

```http
POST /oauth2/v1/accesstoken?grant_type=client_credentials
```

---

# FHIR Resources Used

| Resource     | Description          |
| ------------ | -------------------- |
| Patient      | Data pasien          |
| Practitioner | Data dokter          |
| Location     | Lokasi pelayanan     |
| Encounter    | Registrasi kunjungan |

---

# HTTP Status Code

| Status | Description           |
| ------ | --------------------- |
| 200    | Success               |
| 201    | Resource Created      |
| 400    | Bad Request           |
| 401    | Unauthorized          |
| 404    | Resource Not Found    |
| 500    | Internal Server Error |

---

# Notes

- Menggunakan SATU SEHAT Sandbox Environment
- Data NIK menggunakan dummy sandbox
- Format response menggunakan FHIR R4 JSON
- Swagger dibuat menggunakan Flasgger
- Semua endpoint dapat diuji langsung melalui Swagger UI

---
