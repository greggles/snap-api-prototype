Feature: Testing SNAP Financial Factors Web API for Illinois

  Scenario:
    Given the household is in Illinois
    Given a 1-person household
    Given the household does not include an elderly or disabled member
    Given the household has income of $0 monthly
    Given the household has assets of $0 monthly
     When we run the benefit estimator
     Then we find the family is likely eligible
     Then we find the estimated benefit is $194 per month

  Scenario:
    Given the household is in Illinois
    Given a 2-person household
    Given the household does not include an elderly or disabled member
    Given the household has income of $0 monthly
    Given the household has assets of $0 monthly
     When we run the benefit estimator
     Then we find the family is likely eligible
     Then we find the estimated benefit is $355 per month

  Scenario:
    Given the household is in Illinois
    Given a 3-person household
    Given the household does not include an elderly or disabled member
    Given the household has income of $0 monthly
    Given the household has assets of $0 monthly
     When we run the benefit estimator
     Then we find the family is likely eligible
     Then we find the estimated benefit is $355 per month
