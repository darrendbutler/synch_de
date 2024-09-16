library(tidyverse)
library(lme4)

d <- read_csv('features.csv') %>%
  janitor::clean_names() %>%
  mutate(education_level_ordinal = case_when(
    education_level=='P7 or below' ~ 1,
    education_level=='S1' ~ 2,
    education_level=='S2' ~ 3,
    education_level=='S3' ~ 4,
    education_level=='S4' ~ 5,
    education_level=='S5 or above' ~ 6,
    education_level=='Completed A level' ~ 7
  )) %>%
  mutate(education_level_ordinal_ranked = rank(education_level_ordinal)) %>%
  mutate_if(is.numeric, scale)

# First analysis: Practice effect

m <- lm(exam_points ~ unique_practice_questions_answered + education_level_ordinal_ranked, d)
summary(m)
m_int <- lm(exam_points ~ unique_practice_questions_answered * education_level_ordinal_ranked, d)
anova(m, m_int)

d$predicted <- predict(m_int, newdata = d)

ggplot(d, aes(x = unique_practice_questions_answered, y = predicted, color = as.factor(education_level_ordinal_ranked))) +
  geom_line() +
  labs(title = "Interaction between Unique Practice Questions Answered and Education Level",
       x = "X",
       y = "Predicted Exam Points",
       color = "Education Level") +
  theme_minimal() +
  scale_color_discrete(name = "Education Level")

# Second analysis: Practice and prior instruction

m <- lm(exam_points ~ proportion_of_prior_insutrction + unique_practice_questions_answered + education_level_ordinal_ranked, d)
summary(m)

m_int<- lm(exam_points ~ proportion_of_prior_insutrction*unique_practice_questions_answered + education_level_ordinal_ranked, d)
anova(m, m_int)

sjPlot::tab_model(m_int)

plot(m_int) # there is an outlier



d$predicted <- predict(m_int, newdata = d)

d2 <- d %>% 
  mutate(high_pi = proportion_of_prior_insutrction > median(proportion_of_prior_insutrction, na.rm=TRUE)) %>%
  filter(!is.na(high_pi))

ggplot(d2, aes(x = unique_practice_questions_answered, y = predicted, color = high_pi)) +
  geom_point() +
  geom_smooth(method = "lm", aes(group = high_pi)) +
  labs(title = "Interaction Plot", x = "Practice", y = "Exam Points") +
  theme_minimal()

summary(m_int)

# Remove students with less than x number of survey; unique_practice_questions_answered_scaled_by_max

# Re-run with categorical

m <- lm(exam_points ~ proportion_of_prior_insutrction + education_level_ordinal_ranked, d)
summary(m)

m_int <- lm(exam_points ~ prior_insutruction_reporting_frequency_scaled_by_max * education_level_ordinal_ranked, d)
anova(m, m_int)

summary(m_int)

library(ggplot2)

# Create predictions using the interaction model


ggplot(d, aes(x = unique_practice_questions_answered, y = predicted, color = as.factor(education_level_ordinal_ranked))) +
  geom_line() +
  labs(title = "Interaction between Unique Practice Questions Answered and Education Level",
       x = "X",
       y = "Predicted Exam Points",
       color = "Education Level") +
  theme_minimal() +
  scale_color_discrete(name = "Education Level")



library(ggplot2)

# Create a new data frame with predictions from the interaction model
d_model$predicted <- predict(m_int, newdata = d)

# Plot the interaction
ggplot(d_model, aes(x = unique_practice_questions_answered, y = predicted)) +
  geom_line() +
  labs(title = "Interaction between Unique Practice Questions Answered and Education Level",
       x = "Unique Practice Questions Answered",
       y = "Predicted Exam Points") +
  theme_minimal()


# 
usdm::vifcor(d %>% select_if(is.numeric)) 


summary(m)
plot(m)

cor(d$prior_insutruction_reporting_frequency, d$unique_practice_questions_answered)
cor(d$proportion_of_prior_insutrction, d$unique_practice_questions_answered, use='pairwise.complete.obs')



plot(d$prior_insutruction_reporting_frequency, d$unique_practice_questions_answered)

plot(d$prior_insutruction_reporting_frequency_scaled_by_max, d$unique_practice_questions_answered_scaled_by_max)

d_tmp <- d %>%
  mutate(high_inst = prior_insutruction_reporting_frequency < median(prior_insutruction_reporting_frequency, na.rm=TRUE)) %>%
  mutate(high_prac = unique_practice_questions_answered < median(unique_practice_questions_answered, na.rm=TRUE))
  
xtabs(~high_inst+high_prac, d_tmp)


summary(m)
plot(m)
