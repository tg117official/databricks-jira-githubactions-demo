from src.pipeline.transforms import source_to_bronze


def test_source_to_bronze_standardizes_name_and_country():
    input_rows = [
        {
            "customer_id": 1,
            "customer_name": " Alice ",
            "country": "india",
            "amount": 100.0,
        }
    ]

    result = source_to_bronze(input_rows)

    assert len(result) == 1
    assert result[0]["customer_name"] == "Alice"
    assert result[0]["country"] == "INDIA"
    assert result[0]["ingestion_status"] == "BRONZE_LOADED"


def test_source_to_bronze_keeps_amount():
    input_rows = [
        {
            "customer_id": 2,
            "customer_name": "Bob",
            "country": "usa",
            "amount": 250.0,
        }
    ]

    result = source_to_bronze(input_rows)

    assert result[0]["amount"] == 250.0