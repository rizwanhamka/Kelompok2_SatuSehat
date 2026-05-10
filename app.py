from datetime import datetime, timezone

import requests
from flask import Flask, jsonify
from flasgger import Swagger

app = Flask(__name__)

# ─────────────────────────────────────────────────────────────
# SWAGGER CONFIG
# ─────────────────────────────────────────────────────────────
app.config["SWAGGER"] = {
    "title": "SATU SEHAT API",
    "uiversion": 3
}

swagger = Swagger(app)

# ─────────────────────────────────────────────────────────────
# SATU SEHAT CONFIG
# ─────────────────────────────────────────────────────────────
AUTH_URL = "https://api-satusehat-stg.dto.kemkes.go.id/oauth2/v1"
BASE_URL = "https://api-satusehat-stg.dto.kemkes.go.id/fhir-r4/v1"

CLIENT_ID = "i8J4lqsJRiQ42SCsUiTFIvD8ziAlbtNWYoiNLN2YJqvi5t1d"
CLIENT_SECRET = "EF91AzuqLQVMeJEwRKb97bBanjlpHREtnrtSpkQhBtYJbkAuJjjCL2vhcTXhOHAK"

ORG_ID = "10000004"

NIK_PASIEN = "1000000000000001"
NIK_DOKTER = "1000000000000002"

# ─────────────────────────────────────────────────────────────
# GET ACCESS TOKEN
# ─────────────────────────────────────────────────────────────
def get_access_token():
    url = f"{AUTH_URL}/accesstoken?grant_type=client_credentials"

    response = requests.post(
        url,
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
    )

    response.raise_for_status()

    return response.json()["access_token"]


# # ─────────────────────────────────────────────────────────────
# # HEALTH CHECK
# # ─────────────────────────────────────────────────────────────
# @app.route("/health", methods=["GET"])
# def health():
#     """
#     Health Check
#     ---
#     tags:
#       - Health
#     responses:
#       200:
#         description: API Running
#     """

#     return jsonify({
#         "status": "ok",
#         "service": "SATU SEHAT API"
#     })


# ─────────────────────────────────────────────────────────────
# SEARCH PATIENT BY NIK
# ─────────────────────────────────────────────────────────────
@app.route("/patient", methods=["GET"])
def search_patient():
    """
    Search Patient by NIK
    ---
    tags:
      - Patient
    parameters:
      - name: nik
        in: query
        type: string
        required: true
        example: 1000000000000001
    responses:
      200:
        description: Patient found
      404:
        description: Patient not found
    """

    try:
        token = get_access_token()

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(
            f"{BASE_URL}/Patient",
            headers=headers,
            params={
                "identifier": f"https://fhir.kemkes.go.id/id/nik|{NIK_PASIEN}"
            }
        )

        response.raise_for_status()

        return jsonify(response.json())

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ─────────────────────────────────────────────────────────────
# SEARCH PRACTITIONER BY NIK
# ─────────────────────────────────────────────────────────────
@app.route("/practitioner", methods=["GET"])
def search_practitioner():
    """
    Search Practitioner by NIK
    ---
    tags:
      - Practitioner
    parameters:
      - name: nik
        in: query
        type: string
        required: true
        example: 1000000000000002
    responses:
      200:
        description: Practitioner found
      404:
        description: Practitioner not found
    """

    try:
        token = get_access_token()

        headers = {
            "Authorization": f"Bearer {token}"
        }

        response = requests.get(
            f"{BASE_URL}/Practitioner",
            headers=headers,
            params={
                "identifier": f"https://fhir.kemkes.go.id/id/nik|{NIK_DOKTER}"
            }
        )

        response.raise_for_status()

        return jsonify(response.json())

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ─────────────────────────────────────────────────────────────
# CREATE LOCATION
# ─────────────────────────────────────────────────────────────
@app.route("/location", methods=["POST"])
def create_location():
    """
    Create Location
    ---
    tags:
      - Location
    responses:
      201:
        description: Location created
    """

    try:
        token = get_access_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "resourceType": "Location",
            "identifier": [
                {
                    "system": f"http://sys-ids.kemkes.go.id/location/{ORG_ID}",
                    "value": "RUANG-POLI-UMUM-01"
                }
            ],
            "status": "active",
            "name": "Ruang Poli Umum",
            "description": "Ruang Poli Umum Rawat Jalan",
            "mode": "instance",
            "physicalType": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/location-physical-type",
                        "code": "ro",
                        "display": "Room"
                    }
                ]
            },
            "managingOrganization": {
                "reference": f"Organization/{ORG_ID}"
            }
        }

        response = requests.post(
            f"{BASE_URL}/Location",
            headers=headers,
            json=payload
        )

        response.raise_for_status()

        return jsonify(response.json()), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ─────────────────────────────────────────────────────────────
# CREATE ENCOUNTER
# ─────────────────────────────────────────────────────────────
@app.route("/encounter", methods=["POST"])
def create_encounter():
    """
    Create Encounter
    ---
    tags:
      - Encounter
    responses:
      201:
        description: Encounter created
    """

    try:
        token = get_access_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # ─── GET PATIENT ─────────────────────────────
        patient_response = requests.get(
            f"{BASE_URL}/Patient",
            headers=headers,
            params={
                "identifier": f"https://fhir.kemkes.go.id/id/nik|{NIK_PASIEN}"
            }
        )

        patient_data = patient_response.json()
        patient_resource = patient_data["entry"][0]["resource"]

        patient_id = patient_resource["id"]
        patient_name = patient_resource["name"][0]["text"]

        # ─── GET PRACTITIONER ────────────────────────
        practitioner_response = requests.get(
            f"{BASE_URL}/Practitioner",
            headers=headers,
            params={
                "identifier": f"https://fhir.kemkes.go.id/id/nik|{NIK_DOKTER}"
            }
        )

        practitioner_data = practitioner_response.json()
        practitioner_resource = practitioner_data["entry"][0]["resource"]

        practitioner_id = practitioner_resource["id"]
        practitioner_name = practitioner_resource["name"][0]["text"]

        # ─── CREATE LOCATION ─────────────────────────
        location_payload = {
            "resourceType": "Location",
            "identifier": [
                {
                    "system": f"http://sys-ids.kemkes.go.id/location/{ORG_ID}",
                    "value": "RUANG-POLI-UMUM-01"
                }
            ],
            "status": "active",
            "name": "Ruang Poli Umum",
            "description": "Ruang Poli Umum Rawat Jalan",
            "mode": "instance",
            "physicalType": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/location-physical-type",
                        "code": "ro",
                        "display": "Room"
                    }
                ]
            },
            "managingOrganization": {
                "reference": f"Organization/{ORG_ID}"
            }
        }

        location_response = requests.post(
            f"{BASE_URL}/Location",
            headers=headers,
            json=location_payload
        )

        location_response.raise_for_status()

        location_id = location_response.json()["id"]

        # ─── CREATE ENCOUNTER ────────────────────────
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        encounter_payload = {
            "resourceType": "Encounter",
            "status": "arrived",
            "class": {
                "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
                "code": "AMB",
                "display": "ambulatory"
            },
            "subject": {
                "reference": f"Patient/{patient_id}",
                "display": patient_name
            },
            "participant": [
                {
                    "type": [
                        {
                            "coding": [
                                {
                                    "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
                                    "code": "ATND",
                                    "display": "attender"
                                }
                            ]
                        }
                    ],
                    "individual": {
                        "reference": f"Practitioner/{practitioner_id}",
                        "display": practitioner_name
                    }
                }
            ],
            "period": {
                "start": now
            },
            "location": [
                {
                    "location": {
                        "reference": f"Location/{location_id}",
                        "display": "Ruang Poli Umum"
                    }
                }
            ],
            "statusHistory": [
                {
                    "status": "arrived",
                    "period": {
                        "start": now
                    }
                }
            ],
            "serviceProvider": {
                "reference": f"Organization/{ORG_ID}"
            },
            "identifier": [
                {
                    "system": f"http://sys-ids.kemkes.go.id/encounter/{ORG_ID}",
                    "value": f"ENC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                }
            ]
        }

        encounter_response = requests.post(
            f"{BASE_URL}/Encounter",
            headers=headers,
            json=encounter_payload
        )

        encounter_response.raise_for_status()

        return jsonify(encounter_response.json()), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=5000)
