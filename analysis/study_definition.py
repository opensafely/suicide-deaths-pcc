from cohortextractor import (
    StudyDefinition,
    patients,
    codelist,
    codelist_from_csv)
from codelists import (
    codes_injury_poisoning_undet_intent,
    codes_intentional_self_harm,
    codes_sequelae_self_harm_injury_poisoning
)

study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "2019-01-28", "latest": "2020-03-31"},
        "rate": "uniform",
        "incidence": 0.5,
    },
    population=patients.satisfying(
        """
        # Restrict to registered patients above 16yo
        registered AND
        age > 16 AND

        # Restrict population to patients with suicide death ICD10 code
        (sequelae_ICD_flag OR
        undetermined_ICD_flag OR
        intentional_ICD_flag)
        """
    ),
    # Define registered variable
    registered=patients.registered_as_of(
        "2020-03-31",
        return_expectations={"incidence": 0.9},
    ),
    # Define age variable
    age=patients.age_as_of(
        "2020-03-31",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),
    # Suicide death with Undetermined intent
    undetermined_ICD_flag=patients.with_these_codes_on_death_certificate(
        between=["2019-01-28", "2020-03-31"],
        codelist=codes_injury_poisoning_undet_intent,
        returning="binary_flag",
    ),
    undetermined_ICD_date=patients.with_these_codes_on_death_certificate(
        between=["2019-01-28", "2020-03-31"],
        codelist=codes_injury_poisoning_undet_intent,
        returning="date_of_death",
        date_format="YYYY-MM-DD",
    ),
    # Suicide death with evidence of intentional self-harm

    intentional_ICD_flag=patients.with_these_codes_on_death_certificate(
        between=["2019-01-28", "2020-03-31"],
        codelist=codes_intentional_self_harm,
        returning="binary_flag",
    ),
    intentional_ICD_date=patients.with_these_codes_on_death_certificate(
        between=["2019-01-28", "2020-03-31"],
        codelist=codes_intentional_self_harm,
        returning="date_of_death",
        date_format="YYYY-MM-DD",
    ),
    # TODO: ADD SHORT DESCRIPTION
    # TODO: THINK ABOUT BETTER VARIABLE NAME?
    sequelae_ICD_flag=patients.with_these_codes_on_death_certificate(
        between=["2019-01-28", "2020-03-31"],
        codelist=codes_sequelae_self_harm_injury_poisoning,
        returning="binary_flag",
    ),
    sequelae_ICD_date=patients.with_these_codes_on_death_certificate(
        between=["2019-01-28", "2020-03-31"],
        codelist=codes_sequelae_self_harm_injury_poisoning,
        returning="date_of_death",
        date_format="YYYY-MM-DD",
    ),
    # Define sex variable
    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.49, "F": 0.51}},
        }
    ),
    # Define latest_gp_date as date of the latest GP consultation within the study period.
    last_gp_date=patients.with_gp_consultations(
        between=["2018-12-02", "2020-03-31"],
        # 02/12/2018 is 120 days before the start of the study period.
        # We want to see numbers of individuals who completed suicide death
        # within x days of a primary care contact (30/60/90/120 days).
        find_first_match_in_period=None,
        find_last_match_in_period=True,
        returning='date',
        date_format="YYYY-MM-DD",
        return_expectations=None
    ),
)
