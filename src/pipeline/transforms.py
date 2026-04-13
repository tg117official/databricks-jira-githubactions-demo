from __future__ import annotations

from typing import Iterable, List, Dict


def source_to_bronze(records: Iterable[Dict]) -> List[Dict]:
    """
    Simulates source -> bronze.
    Minimal standardization:
    - trims customer_name
    - uppercases country
    - keeps record as-is otherwise
    """
    output = []

    for row in records:
        customer_name = str(row.get("customer_name", "")).strip()
        country = str(row.get("country", "")).strip().upper()

        output.append(
            {
                "customer_id": row.get("customer_id"),
                "customer_name": customer_name,
                "country": country,
                "amount": row.get("amount"),
                "ingestion_status": "BRONZE_LOADED",
            }
        )

    return output


def bronze_to_silver_with_dq(records: Iterable[Dict]) -> List[Dict]:
    """
    Simulates bronze -> silver with simple DQ rules:
    - customer_id must not be null
    - customer_name must not be blank
    - amount must be >= 0
    - country must be one of allowed values
    """
    allowed_countries = {"INDIA", "USA", "UK", "UAE", "CANADA"}
    output = []

    for row in records:
        customer_id = row.get("customer_id")
        customer_name = str(row.get("customer_name", "")).strip()
        amount = row.get("amount")
        country = str(row.get("country", "")).strip().upper()

        dq_status = "PASS"
        dq_reason = "VALID"

        if customer_id is None:
            dq_status = "FAIL"
            dq_reason = "customer_id_is_null"
        elif not customer_name:
            dq_status = "FAIL"
            dq_reason = "customer_name_is_blank"
        elif amount is None or float(amount) < 0:
            dq_status = "FAIL"
            dq_reason = "amount_is_invalid"
        elif country not in allowed_countries:
            dq_status = "FAIL"
            dq_reason = "country_not_allowed"

        output.append(
            {
                "customer_id": customer_id,
                "customer_name": customer_name,
                "country": country,
                "amount": amount,
                "dq_status": dq_status,
                "dq_reason": dq_reason,
                "record_status": "SILVER_READY" if dq_status == "PASS" else "REJECTED",
            }
        )

    return output