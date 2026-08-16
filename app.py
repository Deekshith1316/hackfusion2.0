from __future__ import annotations

import random
from datetime import datetime

from flask import Flask, jsonify, render_template

app = Flask(__name__)

PATIENTS = [
    {
        "id": "P-104",
        "name": "Aisha Rahman",
        "age": 61,
        "condition": "Hypertension",
        "location": "Home Care",
        "alert": "Mild dizziness",
    },
    {
        "id": "P-215",
        "name": "Daniel Brooks",
        "age": 48,
        "condition": "Post-surgery recovery",
        "location": "Remote Unit A",
        "alert": "Mobility check",
    },
    {
        "id": "P-334",
        "name": "Sofia Nguyen",
        "age": 72,
        "condition": "CHF monitoring",
        "location": "Home Care",
        "alert": "No immediate concern",
    },
    {
        "id": "P-412",
        "name": "Michael Torres",
        "age": 54,
        "condition": "Diabetes",
        "location": "Remote Unit B",
        "alert": "Blood sugar trend rising",
    },
]


def calculate_risk_score(patient):
    heart_rate = random.randint(68, 120)
    spo2 = random.randint(88, 99)
    temperature = round(random.uniform(36.3, 39.0), 1)
    systolic = random.randint(100, 170)
    diastolic = random.randint(65, 105)
    respiration = random.randint(12, 28)
    activity = random.randint(1000, 11000)

    score = 20
    score += max(0, heart_rate - 90) * 1.4
    score += max(0, 95 - spo2) * 3
    score += max(0, temperature - 37.5) * 12
    score += max(0, systolic - 120) * 0.6
    score += max(0, respiration - 18) * 2
    score += max(0, 6000 - activity) * 0.003 if activity < 6000 else 0

    score = max(0, min(100, round(score)))

    if score >= 75:
        risk_level = "Critical"
        recommendation = "Escalate clinician review and trigger emergency follow-up."
    elif score >= 50:
        risk_level = "Watch"
        recommendation = "Increase monitoring frequency and check medication adherence."
    else:
        risk_level = "Stable"
        recommendation = "Continue routine monitoring and lifestyle support."

    alerts = []
    if heart_rate > 100:
        alerts.append("Elevated heart rate")
    if spo2 < 94:
        alerts.append("Low oxygen saturation")
    if temperature > 37.8:
        alerts.append("Fever risk")
    if systolic > 140 or diastolic > 90:
        alerts.append("Blood pressure above target")
    if not alerts:
        alerts.append("Vitals within expected range")

    return {
        "patientId": patient["id"],
        "name": patient["name"],
        "age": patient["age"],
        "condition": patient["condition"],
        "location": patient["location"],
        "alert": patient["alert"],
        "heartRate": heart_rate,
        "spo2": spo2,
        "temperature": temperature,
        "bloodPressure": f"{systolic}/{diastolic}",
        "respiration": respiration,
        "activity": activity,
        "riskScore": score,
        "riskLevel": risk_level,
        "recommendation": recommendation,
        "alerts": alerts,
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/patients")
def api_patients():
    patients = [calculate_risk_score(patient) for patient in PATIENTS]
    summary = {
        "totalPatients": len(patients),
        "critical": sum(1 for p in patients if p["riskLevel"] == "Critical"),
        "watch": sum(1 for p in patients if p["riskLevel"] == "Watch"),
        "stable": sum(1 for p in patients if p["riskLevel"] == "Stable"),
    }
    return jsonify({
        "generatedAt": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "summary": summary,
        "patients": patients,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
