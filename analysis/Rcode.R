library(tidyverse)

#Add data source - input.csv

data<-read.csv(file = file_source)

#### Columns/variables
# "registered"
# "age"
# "sex"
# "ethnicity"
# "patient_id"

#Convert data type for date fields
data$undetermined_ICD_date <- as.Date(data$undetermined_ICD_date, format = "%Y-%m-%d")
data$intentional_ICD_date <- as.Date(data$intentional_ICD_date, format = "%Y-%m-%d")
data$sequelae_ICD_date <- as.Date(data$sequelae_ICD_date, format = "%Y-%m-%d")
data$Last_GP_date <- as.Date(data$Last_GP_date, format = "%Y-%m-%d")

#Define binary age variable to use as a filter
data$age16 <- ifelse(data$age >= 16, 1,0)

# create age bands

# filter the data for (1) patients registered at GP practice (2) above 16 (3) have a ICD-10 code
data <- data%>%
  filter(registered == 1 & age16 ==1 & (intentional_ICD_flag == 1 | undetermined_ICD_flag==1 | sequelae_ICD_flag ==1))

#Problem - The binary flag fields that were defined in the study definition are not correct.
# They show flags when there are no dates.

# Retrieve the latest date for suicide codes on death certificate. can change to MIN if required.
# There seem to be multiple dates for attempted suicide. 
# This suggests that suicide attempts can be made multiple times
# Do we look at the latest suicide attempt only, as that is 
# presumed to be the one that led to death
data$deathdate = pmax(data$intentional_ICD_date,data$undetermined_ICD_date,data$sequelae_ICD_date, na.rm=TRUE)

# Some records have Cause of death date after the GP consulation date.- this is only dummy data though


#remove records without death date - should not need to do this.
data <- data%>%
  drop_na(deathdate)

#Need to compare date of latest GP consultation with death date.
#data$days_after_contact<-difftime(data$deathdate ,data$Last_GP_date)
data$days_after_contact<-data$deathdate-data$Last_GP_date

data$death_30<-ifelse(data$days_after_contact<=30, 1, 0)
data$death_60<-ifelse(data$days_after_contact<=60, 1, 0)
data$death_90<-ifelse(data$days_after_contact<=90, 1, 0)
data$death_120<-ifelse(data$days_after_contact<=120, 1, 0)

# List of variables
# "age"                  
# "undetermined_ICD_flag"
# "intentional_ICD_flag"
# "sequelae_ICD_flag"    
# "sex"
# "ethnicity"
# "death_30"
# "death_60"
# "death_90"             
# "death_120"

t30<-data %>%
  select(age,undetermined_ICD_flag,intentional_ICD_flag,
         sequelae_ICD_flag,sex,ethnicity,death_30,death_60,death_90,death_120) %>%
  group_by(sex) %>%
  count(death_30)

sex_30<-t1%>%
  pivot_wider(
  names_from = death_30,
  names_sep = ".",
  values_from = c(n)
)

# Total Number
# COD diagnosis group
# Gender
# COD and Gender




