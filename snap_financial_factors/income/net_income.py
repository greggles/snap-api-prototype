from typing import Dict
from snap_financial_factors.deductions.earned_income_deduction import EarnedIncomeDeduction
from snap_financial_factors.deductions.dependent_care_deduction import DependentCareDeduction
from snap_financial_factors.deductions.medical_expenses_deduction import MedicalExpensesDeduction
from snap_financial_factors.deductions.child_support_payments_deduction import ChildSupportPaymentsDeduction
from snap_financial_factors.deductions.standard_deduction import StandardDeduction
from snap_financial_factors.input_data.input_data import InputData
from snap_financial_factors.income.income_result import IncomeResult


class NetIncome:
    '''
    Returns the adjusted net income (gross income minus deductions).
    '''

    def __init__(self,
                 input_data: InputData,
                 gross_income: int,
                 deductions_data: Dict,
                 child_support_payments_treatment: str) -> None:
        # Load user input data
        self.input_data = input_data
        self.monthly_job_income = input_data.monthly_job_income
        self.state_or_territory = input_data.state_or_territory
        self.household_size = input_data.household_size
        self.dependent_care_costs = input_data.dependent_care_costs
        self.household_includes_elderly_or_disabled = input_data.household_includes_elderly_or_disabled
        self.medical_expenses_for_elderly_or_disabled = input_data.medical_expenses_for_elderly_or_disabled
        self.court_ordered_child_support_payments = input_data.court_ordered_child_support_payments
        self.rent_or_mortgage = input_data.rent_or_mortgage
        self.homeowners_insurance_and_taxes = input_data.homeowners_insurance_and_taxes

        self.deductions_data = deductions_data
        self.gross_income = gross_income
        self.child_support_payments_treatment = child_support_payments_treatment

    def calculate(self):
        explanation = []
        explanation_intro = (
            'To find out if this household is eligible for SNAP and estimate ' +
            'the benefit amount, we start by calculating net income. Net income ' +
            'is equal to total gross monthly income, minus deductions.'
        )
        explanation.append(explanation_intro)

        # Add up income.
        income_explanation = (
            "Let's start with total household income. " +
            f"This household's gross income is ${self.gross_income}."
        )
        explanation.append(income_explanation)

        # Add up deductions:
        deductions = [
            StandardDeduction(
                state_or_territory=self.state_or_territory,
                household_size=self.household_size,
                deductions_data=self.deductions_data
            ),
            EarnedIncomeDeduction(monthly_job_income=self.monthly_job_income),
            DependentCareDeduction(dependent_care_costs=self.dependent_care_costs),
            MedicalExpensesDeduction(
                household_includes_elderly_or_disabled=self.household_includes_elderly_or_disabled,
                medical_expenses_for_elderly_or_disabled=self.medical_expenses_for_elderly_or_disabled
            ),
            ChildSupportPaymentsDeduction(
                child_support_payments_treatment=self.child_support_payments_treatment,
                court_ordered_child_support_payments=self.court_ordered_child_support_payments,
            )
        ]

        deduction_results = []

        for deduction in deductions:
            calculation = deduction.calculate()
            deduction_explanations = calculation.explanation

            # Append each deduction's explanations to overall Net Income explanation
            for deduction_explanation in deduction_explanations:
                explanation.append(deduction_explanation)

            deduction_results.append(calculation.result)

        total_deductions_value = sum(deduction_results)

        total_deductions_explanation = (
            f"Next, we add all applicable deductions together: "
        )
        explanation.append(total_deductions_explanation)
        explanation.append('')

        # Construct math explanation for total deductions:
        total_deductions_math_explanation = ''
        applicable_deductions = [
            deduction for deduction in deduction_results if deduction > 0
        ]
        applicable_deductions_len = len(applicable_deductions)
        for index, deduction_value in enumerate(applicable_deductions):
            if index == (applicable_deductions_len - 1):
                total_deductions_math_explanation += f"${deduction_value} = "
            else:
                total_deductions_math_explanation += f"${deduction_value} + "
        total_deductions_math_explanation += f"{total_deductions_value}"
        explanation.append(total_deductions_math_explanation)

        total_deductions_summary = (
            f"The total of all deductions is <strong>${total_deductions_value}</strong>. "
        )
        explanation.append(total_deductions_summary)

        net_income = self.gross_income - total_deductions_value

        # Adjusted net income can't be negative
        if 0 > net_income:
            net_income = 0

        calculation_explanation = (
            f"Gross income (<strong>${self.gross_income}</strong>) minus " +
            f"total deductions (<strong>${total_deductions_value}</strong>) " +
            f"equals net income: <strong>${net_income}.</strong>"
        )
        explanation.append(calculation_explanation)

        return IncomeResult(
            name='Net Income',
            result=net_income,
            explanation=explanation,
            sort_order=1
        )
