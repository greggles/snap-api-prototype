import pytest
from snap_financial_factors.input_data.parse_input_data import ParseInputData


def parse_input_data(input_data):
    return ParseInputData(input_data).parse()


def test_no_input_data():
    parse = parse_input_data(None)
    assert parse.valid is False
    assert parse.errors == ['No input data received.']
    assert parse.result is None


def test_valid_input_data():
    parse = parse_input_data({
        'state_or_territory': 'IL',
        'monthly_job_income': 0,
        'monthly_non_job_income': 0,
        'household_size': 1,
        'household_includes_elderly_or_disabled': 'false',
        'resources': 0
    })
    assert parse.valid is True
    assert parse.errors == []
    assert parse.result is not None


def test_valid_input_data_with_int_parsing():
    parse = parse_input_data({
        'state_or_territory': 'IL',
        'monthly_job_income': '0',
        'monthly_non_job_income': '0',
        'household_size': '1',
        'household_includes_elderly_or_disabled': 'false',
        'resources': '0'
    })
    assert parse.valid is True
    assert parse.errors == []
    assert parse.result is not None


def test_valid_input_data_with_int_and_bool_parsing():
    parse = parse_input_data({
        'state_or_territory': 'IL',
        'monthly_job_income': '0',
        'monthly_non_job_income': '0',
        'household_size': '1',
        'household_includes_elderly_or_disabled': 'true',
        'resources': '0'
    })
    assert parse.valid is True
    assert parse.errors == []
    assert parse.result is not None


def test_missing_required_integer():
    parse = parse_input_data({
        'state_or_territory': 'IL',
        'monthly_non_job_income': 0,
        'household_size': 1,
        'household_includes_elderly_or_disabled': 'false',
        'resources': 0
    })
    assert parse.valid is False
    assert parse.errors == ['Missing required input: monthly_job_income']
    assert parse.result is None


def test_missing_required_bool():
    parse = parse_input_data({
        'state_or_territory': 'IL',
        'monthly_job_income': 0,
        'monthly_non_job_income': 0,
        'household_size': 1,
        'resources': 0
    })
    assert parse.valid is False
    assert parse.errors == ['Missing required input: household_includes_elderly_or_disabled']
    assert parse.result is None


def test_optional_bool_accepts_none():
    parse = parse_input_data({
        'state_or_territory': 'IL',
        'monthly_job_income': 0,
        'monthly_non_job_income': 0,
        'household_size': 1,
        'household_includes_elderly_or_disabled': 'false',
        'resources': 0,
        'use_emergency_allotment': None
    })
    assert parse.valid is True
    assert parse.errors == []
    assert parse.result is not None


def test_optional_bool_successfully_parsed_from_true_string():
    parse = parse_input_data({
        'state_or_territory': 'IL',
        'monthly_job_income': 0,
        'monthly_non_job_income': 0,
        'household_size': 1,
        'household_includes_elderly_or_disabled': 'false',
        'resources': 0,
        'use_emergency_allotment': 'true'
    })
    assert parse.valid is True
    assert parse.errors == []
    assert parse.result is not None
    assert parse.input_data['use_emergency_allotment'] is True


def test_optional_bool_successfully_parsed_from_false_string():
    parse = parse_input_data({
        'state_or_territory': 'IL',
        'monthly_job_income': 0,
        'monthly_non_job_income': 0,
        'household_size': 1,
        'household_includes_elderly_or_disabled': 'false',
        'resources': 0,
        'use_emergency_allotment': 'false'
    })
    assert parse.valid is True
    assert parse.errors == []
    assert parse.result is not None
    assert parse.input_data['use_emergency_allotment'] is False


def test_optional_bool_accepts_python_native_bool_true():
    parse = parse_input_data({
        'state_or_territory': 'IL',
        'monthly_job_income': 0,
        'monthly_non_job_income': 0,
        'household_size': 1,
        'household_includes_elderly_or_disabled': 'false',
        'resources': 0,
        'use_emergency_allotment': True
    })
    assert parse.valid is True
    assert parse.errors == []
    assert parse.result is not None
    assert parse.input_data['use_emergency_allotment'] is True


def test_optional_bool_accepts_python_native_bool_false():
    parse = parse_input_data({
        'state_or_territory': 'IL',
        'monthly_job_income': 0,
        'monthly_non_job_income': 0,
        'household_size': 1,
        'household_includes_elderly_or_disabled': 'false',
        'resources': 0,
        'use_emergency_allotment': False
    })
    assert parse.valid is True
    assert parse.errors == []
    assert parse.result is not None
    assert parse.input_data['use_emergency_allotment'] is False


def test_optional_bool_raises_on_int():
    with pytest.raises(ValueError) as error:
        parse_input_data({
            'state_or_territory': 'IL',
            'monthly_job_income': 0,
            'monthly_non_job_income': 0,
            'household_size': 1,
            'household_includes_elderly_or_disabled': 'false',
            'resources': 0,
            'use_emergency_allotment': 3
        })
    assert str(error.value) == 'Unexpected value for use_emergency_allotment'


def test_missing_multiple():
    parse = parse_input_data({
        'state_or_territory': 'IL',
        'monthly_job_income': 0,
        'household_size': 1,
        'resources': 0
    })
    assert parse.valid is False
    assert parse.errors == [
        'Missing required input: monthly_non_job_income',
        'Missing required input: household_includes_elderly_or_disabled',
    ]
    assert parse.result is None


def test_valid_utility_allowance():
    parse = parse_input_data({
        'state_or_territory': 'IL',
        'monthly_job_income': '0',
        'monthly_non_job_income': '0',
        'household_size': '1',
        'household_includes_elderly_or_disabled': 'false',
        'resources': '0',
        'utility_allowance': 'HEATING_AND_COOLING',
    })

    assert parse.valid is True
    assert parse.errors == []
    assert parse.result is not None


def test_valid_utility_allowance_of_none():
    parse = parse_input_data({
        'state_or_territory': 'IL',
        'monthly_job_income': '0',
        'monthly_non_job_income': '0',
        'household_size': '1',
        'household_includes_elderly_or_disabled': 'false',
        'resources': '0',
        'utility_allowance': 'NONE',
    })

    assert parse.valid is True
    assert parse.errors == []
    assert parse.result is not None


def test_valid_utility_allowance_of_empty_string():
    parse = parse_input_data({
        'state_or_territory': 'IL',
        'monthly_job_income': '0',
        'monthly_non_job_income': '0',
        'household_size': '1',
        'household_includes_elderly_or_disabled': 'false',
        'resources': '0',
        'utility_allowance': '',  # Parser should convert '' to None.
    })

    assert parse.valid is True
    assert parse.errors == []
    assert parse.result is not None


def test_clearly_invalid_utility_allowance():
    parse = parse_input_data({
        'state_or_territory': 'IL',
        'monthly_job_income': '0',
        'monthly_non_job_income': '0',
        'household_size': '1',
        'household_includes_elderly_or_disabled': 'false',
        'resources': '0',
        'utility_allowance': 'UNKNOWN',
    })

    assert parse.valid is False
    assert parse.errors == [
        'Unknown standard utility allowance: UNKNOWN'
    ]
    assert parse.result is None


def test_sneakily_invalid_utility_allowance():
    parse = parse_input_data({
        'state_or_territory': 'IL',
        'monthly_job_income': '0',
        'monthly_non_job_income': '0',
        'household_size': '1',
        'household_includes_elderly_or_disabled': 'false',
        'resources': '0',
        'utility_allowance': 'TELEPHONE',  # Should be just "PHONE".
    })

    assert parse.valid is False
    assert parse.errors == [
        'Unknown standard utility allowance: TELEPHONE'
    ]
    assert parse.result is None
