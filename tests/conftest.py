"""Configuración común de las pruebas (pytest la carga sola, antes que los archivos test_*.py)."""

import os

# Antes de importar la API: las pruebas usan SIEMPRE el modelo de prueba ("demo"),
# aunque en tu computadora exista models/modelo.pkl o tengas MODEL_PATH en el .env.
os.environ.pop("MODEL_PATH", None)
os.environ.pop("REQUIRE_MODEL", None)

import pytest  # noqa: E402

import model_service  # noqa: E402
from app import app  # noqa: E402

# El primer cliente del dataset: es el ejemplo del contrato en el README.
VALID_CUSTOMER = {
    "gender": "Female", "SeniorCitizen": 0, "Partner": "Yes", "Dependents": "No",
    "tenure": 1, "PhoneService": "No", "MultipleLines": "No phone service",
    "InternetService": "DSL", "OnlineSecurity": "No", "OnlineBackup": "Yes",
    "DeviceProtection": "No", "TechSupport": "No", "StreamingTV": "No",
    "StreamingMovies": "No", "Contract": "Month-to-month", "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check", "MonthlyCharges": 29.85, "TotalCharges": 29.85,
}


@pytest.fixture
def client():
    """Cliente de prueba: llama a la API sin tener que encenderla."""
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def fresh_model(monkeypatch):
    """Para pruebas que cambian MODEL_PATH: olvida el modelo antes y después."""
    model_service.reset()
    yield monkeypatch
    monkeypatch.undo()
    model_service.reset()
