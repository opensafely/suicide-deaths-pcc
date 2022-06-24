from cohortextractor import codelist_from_csv

codes_injury_poisoning_undet_intent = codelist_from_csv(
    "codelists/user-HIsmail-icd10_injury_poisoning_undet_intent.csv",
    system="icd10",
    column="code"
)

codes_intentional_self_harm = codelist_from_csv(
    "codelists/user-HIsmail-icd10_intentional_self_harm.csv",
    system="icd10",
    column="code"
)

codes_sequelae_self_harm_injury_poisoning = codelist_from_csv(
    "codelists/user-HIsmail-icd10_sequelae_self_harm_injury_poisoning.csv",
    system="icd10",
    column="code"
)
