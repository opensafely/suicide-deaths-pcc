from cohortextractor import (
    StudyDefinition,
    patients,
    codelist,
    codelist_from_csv)
from codelists import (
    codes_ethnicity6,
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
        registered AND
        age > 16 AND

        (sequelae_self_harm_injury_poisoning OR
        injury_poisoning_undet_intent OR
        intentional_self_harm)

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
    # TODO: ADD SHORT DESCRIPTION
    # TODO: THINK ABOUT BETTER VARIABLE NAME?
    injury_poisoning_undet_intent=patients.with_these_codes_on_death_certificate(
        between=["2019-01-28", "2020-03-31"],
        codelist=codes_injury_poisoning_undet_intent,
        returning="binary_flag",
    ),
    injury_poisoning_undet_intent_date=patients.with_these_codes_on_death_certificate(
        between=["2019-01-28", "2020-03-31"],
        codelist=codes_injury_poisoning_undet_intent,
        returning="date_of_death",
        date_format="YYYY-MM-DD",
    ),
    # TODO: ADD SHORT DESCRIPTION
    # TODO: THINK ABOUT BETTER VARIABLE NAME?
    intentional_self_harm=patients.with_these_codes_on_death_certificate(
        between=["2019-01-28", "2020-03-31"],
        codelist=codes_intentional_self_harm,
        returning="binary_flag",
    ),
    intentional_self_harm_date=patients.with_these_codes_on_death_certificate(
        between=["2019-01-28", "2020-03-31"],
        codelist=codes_intentional_self_harm,
        returning="date_of_death",
        date_format="YYYY-MM-DD",
    ),
    # TODO: ADD SHORT DESCRIPTION
    # TODO: THINK ABOUT BETTER VARIABLE NAME?
    sequelae_self_harm_injury_poisoning=patients.with_these_codes_on_death_certificate(
        between=["2019-01-28", "2020-03-31"],
        codelist=codes_sequelae_self_harm_injury_poisoning,
        returning="binary_flag",
    ),
    sequelae_self_harm_injury_poisoning_date=patients.with_these_codes_on_death_certificate(
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
    # Define ethnicity variable
    ethnicity=patients.categorised_as(
        {
            "Unknown": "DEFAULT",
            "White": "eth='1'",
            "Mixed": "eth='2'",
            "Asian": "eth='3'",
            "Black": "eth='4'",
            "Other": "eth='5'",
        },
        eth=patients.with_these_clinical_events(
            codes_ethnicity6,
            returning="category",
            find_last_match_in_period=True,
            include_date_of_match=False,
            return_expectations={
                "category": {
                    "ratios": {"1": 0.2, "2": 0.2, "3": 0.2, "4": 0.2, "5": 0.2}
                },
                "incidence": 0.75,
            },
        ),
        return_expectations={
            "category": {
                "ratios": {
                    "White": 0.2,
                    "Mixed": 0.2,
                    "Asian": 0.2,
                    "Black": 0.2,
                    "Other": 0.2,
                }
            },
            "incidence": 0.8,
        },
    ),
)
