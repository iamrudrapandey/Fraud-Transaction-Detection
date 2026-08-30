from pathlib import Path
import sys
import sqlite3
import logging
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

# ============================================================
# PROJECT PATH
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT_DIR / "src"))

from predict import predict_transaction


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("fraudguard")


# ============================================================
# DATABASE
# ============================================================

DB_PATH = ROOT_DIR / "fraudguard.db"


def get_connection():
    connection = sqlite3.connect(
        DB_PATH,
        timeout=10
    )
    connection.row_factory = sqlite3.Row
    return connection


def create_database():
    connection = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                Time REAL,

                V1 REAL,
                V2 REAL,
                V3 REAL,
                V4 REAL,
                V5 REAL,
                V6 REAL,
                V7 REAL,
                V8 REAL,
                V9 REAL,
                V10 REAL,
                V11 REAL,
                V12 REAL,
                V13 REAL,
                V14 REAL,
                V15 REAL,
                V16 REAL,
                V17 REAL,
                V18 REAL,
                V19 REAL,
                V20 REAL,
                V21 REAL,
                V22 REAL,
                V23 REAL,
                V24 REAL,
                V25 REAL,
                V26 REAL,
                V27 REAL,
                V28 REAL,

                Amount REAL,

                prediction TEXT,
                fraud_probability REAL,
                risk_level TEXT,
                threshold REAL,

                created_at TEXT
            )
        """)

        connection.commit()

        logger.info("Database initialized successfully")

    except sqlite3.Error as error:
        logger.exception("Database initialization failed")
        raise RuntimeError("Database initialization failed")

    finally:
        if connection:
            connection.close()


create_database()


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="Fraud Transaction Detection API",
    description="ML-powered fraud transaction detection system",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

 allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://fraud-transaction-detection-kj8o.onrender.com"
],
    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# GLOBAL ERROR HANDLERS
# ============================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    logger.warning(
        "Validation error on %s: %s",
        request.url.path,
        exc.errors()
    )

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "VALIDATION_ERROR",
            "message": "Invalid transaction data.",
            "details": exc.errors()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception(
        "Unhandled server error on %s",
        request.url.path
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected server error occurred."
        }
    )


# ============================================================
# TRANSACTION MODEL
# ============================================================

class Transaction(BaseModel):

    Time: float

    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float

    Amount: float = Field(..., ge=0)

    @field_validator("*")
    @classmethod
    def validate_numbers(cls, value):
        if isinstance(value, float):
            if value != value:
                raise ValueError("NaN values are not allowed.")

            if value in (float("inf"), float("-inf")):
                raise ValueError(
                    "Infinite values are not allowed."
                )

        return value


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "success": True,
        "status": "online",
        "service": "Fraud Transaction Detection API",
        "version": "1.0.0",
        "database": "SQLite"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    connection = None

    try:

        connection = get_connection()

        connection.execute(
            "SELECT 1"
        )

        return {
            "success": True,
            "status": "healthy",
            "database": "connected"
        }

    except sqlite3.Error:

        logger.exception(
            "Health check database error"
        )

        return {
            "success": True,
            "status": "degraded",
            "database": "disconnected"
        }

    finally:

        if connection:
            connection.close()


# ============================================================
# PREDICTION
# ============================================================

@app.post("/predict")
def predict(transaction: Transaction):

    connection = None

    try:

        logger.info(
            "Prediction request received | Amount: %.2f",
            transaction.Amount
        )

        # ----------------------------------------------------
        # Convert request to dictionary
        # ----------------------------------------------------

        data = transaction.model_dump()

        # ----------------------------------------------------
        # ML PREDICTION
        # ----------------------------------------------------

        try:

            result = predict_transaction(data)

        except Exception:

            logger.exception(
                "Machine learning prediction failed"
            )

            raise HTTPException(
                status_code=500,
                detail={
                    "success": False,
                    "error": "MODEL_ERROR",
                    "message": "Unable to generate prediction."
                }
            )

        # ----------------------------------------------------
        # Validate ML result
        # ----------------------------------------------------

        if not result or not isinstance(result, dict):

            logger.error(
                "ML model returned invalid result"
            )

            raise HTTPException(
                status_code=500,
                detail={
                    "success": False,
                    "error": "INVALID_MODEL_RESPONSE",
                    "message": "The prediction model returned an invalid response."
                }
            )

        # ----------------------------------------------------
        # Extract result
        # ----------------------------------------------------

        prediction = result.get(
            "prediction"
        )

        if prediction not in [
            "FRAUD",
            "LEGITIMATE"
        ]:

            logger.error(
                "Invalid prediction returned: %s",
                prediction
            )

            raise HTTPException(
                status_code=500,
                detail={
                    "success": False,
                    "error": "INVALID_PREDICTION",
                    "message": "The model returned an invalid prediction."
                }
            )

        try:

            fraud_probability = float(
                result.get(
                    "fraud_probability_percent",
                    0
                )
            )

            threshold = float(
                result.get(
                    "threshold",
                    0
                )
            )

        except (TypeError, ValueError):

            logger.exception(
                "Invalid probability or threshold returned by model"
            )

            raise HTTPException(
                status_code=500,
                detail={
                    "success": False,
                    "error": "INVALID_MODEL_DATA",
                    "message": "The model returned invalid numerical data."
                }
            )

        risk_level = result.get(
            "risk_level",
            "UNKNOWN"
        )

        # ----------------------------------------------------
        # DATABASE
        # ----------------------------------------------------

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO predictions (
                    Time,

                    V1,
                    V2,
                    V3,
                    V4,
                    V5,
                    V6,
                    V7,
                    V8,
                    V9,
                    V10,
                    V11,
                    V12,
                    V13,
                    V14,
                    V15,
                    V16,
                    V17,
                    V18,
                    V19,
                    V20,
                    V21,
                    V22,
                    V23,
                    V24,
                    V25,
                    V26,
                    V27,
                    V28,

                    Amount,

                    prediction,
                    fraud_probability,
                    risk_level,
                    threshold,
                    created_at
                )

                VALUES (
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
                )
            """, (
                data["Time"],

                data["V1"],
                data["V2"],
                data["V3"],
                data["V4"],
                data["V5"],
                data["V6"],
                data["V7"],
                data["V8"],
                data["V9"],
                data["V10"],
                data["V11"],
                data["V12"],
                data["V13"],
                data["V14"],
                data["V15"],
                data["V16"],
                data["V17"],
                data["V18"],
                data["V19"],
                data["V20"],
                data["V21"],
                data["V22"],
                data["V23"],
                data["V24"],
                data["V25"],
                data["V26"],
                data["V27"],
                data["V28"],

                data["Amount"],

                prediction,
                fraud_probability,
                risk_level,
                threshold,

                datetime.now().isoformat()
            ))

            connection.commit()

            database_id = cursor.lastrowid

        except sqlite3.Error:

            logger.exception(
                "Database insert failed"
            )

            if connection:
                connection.rollback()

            raise HTTPException(
                status_code=500,
                detail={
                    "success": False,
                    "error": "DATABASE_ERROR",
                    "message": "Prediction was generated, but could not be saved to the database."
                }
            )

        logger.info(
            "Prediction saved successfully | ID: %s | Prediction: %s",
            database_id,
            prediction
        )

        return {
            **result,
            "database_id": database_id,
            "saved_to_database": True,
            "success": True
        }

    except HTTPException:
        raise

    except Exception:

        logger.exception(
            "Unexpected prediction error"
        )

        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": "PREDICTION_ERROR",
                "message": "Unable to process the transaction."
            }
        )

    finally:

        if connection:
            connection.close()


# ============================================================
# GET HISTORY
# ============================================================

@app.get("/history")
def get_history():

    connection = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                Time,
                Amount,
                prediction,
                fraud_probability,
                risk_level,
                threshold,
                created_at
            FROM predictions
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()

        history = []

        for row in rows:

            history.append({
                "id": row["id"],
                "Time": row["Time"],
                "Amount": row["Amount"],
                "prediction": row["prediction"],
                "fraud_probability": row["fraud_probability"],
                "risk_level": row["risk_level"],
                "threshold": row["threshold"],
                "created_at": row["created_at"]
            })

        return {
            "success": True,
            "total": len(history),
            "history": history
        }

    except sqlite3.Error:

        logger.exception(
            "Unable to load prediction history"
        )

        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": "DATABASE_ERROR",
                "message": "Unable to load prediction history."
            }
        )

    finally:

        if connection:
            connection.close()


# ============================================================
# STATISTICS
# ============================================================

@app.get("/stats")
def get_stats():

    connection = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM predictions
        """)

        total = cursor.fetchone()["total"]

        cursor.execute("""
            SELECT COUNT(*) AS fraud
            FROM predictions
            WHERE prediction = 'FRAUD'
        """)

        fraud = cursor.fetchone()["fraud"]

        cursor.execute("""
            SELECT COUNT(*) AS legitimate
            FROM predictions
            WHERE prediction = 'LEGITIMATE'
        """)

        legitimate = cursor.fetchone()["legitimate"]

        fraud_rate = (
            (fraud / total) * 100
            if total > 0
            else 0
        )

        return {
            "success": True,
            "total": total,
            "fraud": fraud,
            "legitimate": legitimate,
            "fraud_rate": round(
                fraud_rate,
                2
            )
        }

    except sqlite3.Error:

        logger.exception(
            "Unable to calculate statistics"
        )

        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": "DATABASE_ERROR",
                "message": "Unable to calculate transaction statistics."
            }
        )

    finally:

        if connection:
            connection.close()


# ============================================================
# CLEAR HISTORY
# ============================================================

@app.delete("/history")
def clear_history():

    connection = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM predictions
        """)

        deleted_count = cursor.rowcount

        connection.commit()

        logger.info(
            "Prediction history cleared | Records: %s",
            deleted_count
        )

        return {
            "success": True,
            "message": "Prediction history cleared successfully.",
            "deleted_records": deleted_count
        }

    except sqlite3.Error:

        logger.exception(
            "Unable to clear prediction history"
        )

        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": "DATABASE_ERROR",
                "message": "Unable to clear prediction history."
            }
        )

    finally:

        if connection:
            connection.close()