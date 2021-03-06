# flake8: noqa
import json
from behave import given, when, then, step
from snap_financial_factors.benefit_estimate import BenefitEstimate
from snap_financial_factors.input_data.parse_input_data import ParseInputData


@given('the household is in {state}')
def step_impl(context, state):
    context.input_data = {}
    context.input_data['state_or_territory'] = state

@given('{no_or_an} emergency allotment waiver')
def step_impl(context, no_or_an):
    use_emergency_allotment = (no_or_an == 'an')
    context.input_data['use_emergency_allotment'] = use_emergency_allotment

@given('a {number:d}-person household')
def step_impl(context, number):
    context.input_data['household_size'] = number

@given('the household {does_or_does_not} include an elderly or disabled member')
def step_impl(context, does_or_does_not):
    result = (does_or_does_not == 'does')
    context.input_data['household_includes_elderly_or_disabled'] = result

@given('the household has earned income of ${number:d} monthly')
def step_impl(context, number):
    context.input_data['monthly_job_income'] = number

@given('the household has other income of ${number:d} monthly')
def step_impl(context, number):
    context.input_data['monthly_non_job_income'] = number

@given('the household has assets of ${number:d}')
def step_impl(context, number):
    context.input_data['resources'] = number

@given('the household has dependent care costs of ${number:d} monthly')
def step_impl(context, number):
    context.input_data['dependent_care_costs'] = number

@given('the household has medical expenses for elderly or disabled members of ${number:d} monthly')
def step_impl(context, number):
    context.input_data['medical_expenses_for_elderly_or_disabled'] = number

@given('the household has court-ordered child support payments of ${number:d} monthly')
def step_impl(context, number):
    context.input_data['court_ordered_child_support_payments'] = number

@given('the household has rent or mortgage costs of ${number:d} monthly')
def step_impl(context, number):
    context.input_data['rent_or_mortgage'] = number

@given('the household has homeowners insurance and taxes costs of ${number:d} monthly')
def step_impl(context, number):
    context.input_data['homeowners_insurance_and_taxes'] = number

@given(u'the household pays for AC or heat (or otherwise qualifies for AC/heat utility allowance)')
def step_impl(context):
    context.input_data['utility_allowance'] = 'HEATING_AND_COOLING'

@given(u'the household pays for water and trash collection (or otherwise qualifies for limited utility allowance)')
def step_impl(context):
    context.input_data['utility_allowance'] = 'BASIC_LIMITED_ALLOWANCE'

@given(u'the household pays for a single utility besides AC, heat, and phone')
def step_impl(context):
    context.input_data['utility_allowance'] = 'SINGLE_UTILITY_ALLOWANCE'

@given(u'the household pays phone bills only')
def step_impl(context):
    context.input_data['utility_allowance'] = 'PHONE'

@given(u'the household is not billed separately for any utilities')
def step_impl(context):
    context.input_data['utility_allowance'] = 'NONE'

@given(u'the household has utility costs of ${number:d} monthly')
def step_impl(context, number):
    context.input_data['utility_costs'] = number

@when('we run the benefit estimator...')
def step_impl(context):
    parsed_input_data = ParseInputData(context.input_data).parse().result
    benefit_estimate = BenefitEstimate(parsed_input_data)
    context.api_result = benefit_estimate.calculate()

@then('we find the family is likely {eligible}')
def step_impl(context, eligible):
    expected_result = (eligible == 'eligible')
    api_result = context.api_result['eligible']

    if (api_result != expected_result):
        print('api_result:')
        print(api_result)
        print('expected_result:')
        print(expected_result)

    assert(api_result == expected_result)

@then('we find the estimated benefit is ${number:d} per month')
def step_impl(context, number):
    expected_result = number
    api_result = context.api_result['estimated_monthly_benefit']

    if (api_result != expected_result):
        print('api_result:')
        print(api_result)
        print('expected_result:')
        print(expected_result)

    assert(api_result == expected_result)
