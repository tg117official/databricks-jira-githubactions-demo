from src.pipeline.transforms import bronze_to_silver_with_dq


def test_bronze_to_silver_pass_record():
    input_rows = [
        {
            "customer_id": 1,
            "customer_name": "Alice",
            "country": "INDIA",
            "amount": 100.0,
        }
    ]

    result = bronze_to_silver_with_dq(input_rows)

    assert result[0]["dq_status"] == "PASS"
    assert result[0]["dq_reason"] == "VALID"
    assert result[0]["record_status"] == "SILVER_READY"


def test_bronze_to_silver_fails_blank_name():
    input_rows = [
        {
            "customer_id": 2,
            "customer_name": "   ",
            "country": "USA",
            "amount": 50.0,
        }
    ]

    result = bronze_to_silver_with_dq(input_rows)

    assert result[0]["dq_status"] == "FAIL"
    assert result[0]["dq_reason"] == "customer_name_is_blank"
    assert result[0]["record_status"] == "REJECTED"


def test_bronze_to_silver_fails_invalid_country():
    input_rows = [
        {
            "customer_id": 3,
            "customer_name": "Eve",
            "country": "MARS",
            "amount": 10.0,
        }
    ]

    result = bronze_to_silver_with_dq(input_rows)

    assert result[0]["dq_status"] == "FAIL"
    assert result[0]["dq_reason"] == "country_not_allowed"