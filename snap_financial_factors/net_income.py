from snap_financial_factors.fetch_deductions import FetchDeductions


class NetIncome:
    '''
    Returns the adjusted net income (gross income minus deductions).
    '''

    def __init__(self, input_data, deductions_data):
        # Load user input data
        self.input_data = input_data
        self.state_or_territory = input_data['state_or_territory']
        self.household_size = input_data['household_size']
        self.monthly_income = input_data['monthly_income']

        self.deductions_data = deductions_data

    def calculate(self):
        state_or_territory = self.state_or_territory
        household_size = self.household_size
        deductions_data = self.deductions_data
        monthly_income = self.monthly_income

        deductions = FetchDeductions(state_or_territory, household_size, deductions_data)
        standard_deduction = deductions.standard_deduction()

        income_minus_deductions = monthly_income - standard_deduction

        # Adjusted net income can't be negative
        if income_minus_deductions >= 0:
            return income_minus_deductions
        else:
            return 0
