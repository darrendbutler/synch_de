library(tidyverse)
library(lme4)

# Install the here package if it's not already installed
if (!require("here")) {
  install.packages("here")
}

# Load the here package
library("here")

# navigate files from project root
# data directory and access described in readME
here() 

# Read Data
data <- read_csv('data/processed/features.csv') %>%
  janitor::clean_names() %>%
  # Create ordinal feature for education_level
  mutate(education_level_ordinal = case_when(
    education_level=='P7 or below' ~ 1,
    education_level=='S1' ~ 2,
    education_level=='S2' ~ 3,
    education_level=='S3' ~ 4,
    education_level=='S4' ~ 5,
    education_level=='S5 or above' ~ 6,
    education_level=='Completed A level' ~ 7
  )) %>%
  # Create ordinal ranked feature for education_level. Q: What is a rank?
  mutate(education_level_ordinal_ranked = rank(education_level_ordinal)) %>%
  # Scale the numerical variables. Q: What's the scaling method here? z-scores?
  mutate_if(is.numeric, scale)

# Descriptive Stats
# Install the here package if it's not already installed
if (!require("table1")) {
  install.packages("table1")
}
library(table1)
data_non_scaled = read_csv('data/processed/features.csv')
table1(~ unique_practice_questions_answered  + 
                 proportion_of_prior_insutrction + 
                 exam_points + education_level, 
               data = data_non_scaled)

# Second analysis: Practice effect considering education level

# Run an additive and interactive model 
# Q: Should the interactive or additive model be used?
model_add <- lm(exam_points ~ unique_practice_questions_answered + education_level, data)
summary(model_add)

if (!require("sjPlot")) {
  install.packages("sjPlot")
}
sjPlot::tab_model(model_add)
# Interactive model with practice and education
model_int <- lm(exam_points ~ unique_practice_questions_answered * education_level, data)
summary(model_int)
anova(model_add, model_int)

# small sample N
data$education_level %>% table %>% as.numeric %>% mean


# Predict exam_points using interactive model.
# Q: Why did you use the predicted values instead of the actual values?
# Q: Low priority: Is there a simpler visualization we an use to communicate 
#    the interaction? It may be hard for readers to identify the levels by
#.   color. On the other hand, I can explicitly point out, that we can
#.   see the interaction because some lines are less steep.
data$predicted <- predict(model_int, newdata = data)

plot_interaction_practice_education_ordinal_ranked <- function(data) {
  # Scale the x and y variables
  #data$unique_practice_questions_answered_scaled <- scale(data$unique_practice_questions_answered)
  #data$predicted_scaled <- scale(data$predicted)
  
  data$predicted <- data$predicted/max(data$predicted) # make it % correct
  data$exam_points <- data$exam_points/max(data$exam_points)
  
  ggplot(data, aes(x = unique_practice_questions_answered, y = predicted, color = as.factor(education_level))) +
    geom_line() + 
    #geom_smooth(method = "lm", se = TRUE) + # Linear regression line with SE
    labs(title = "",
         x = "% Practice Questions Answered",
         y = "% Correct Exam Points",
         color = "Education Level") +
    theme_minimal() +
    scale_color_discrete(name = "Education Level") +
    scale_y_continuous(breaks = seq(0, 1, 0.05))
}

# Example call to the function
plot_interaction_practice_education_ordinal_ranked(data)


data$exam_points_perc <- data$exam_points/max(data$exam_points)

ggplot(data, aes(x = unique_practice_questions_answered, y = exam_points_perc)) +
  geom_point() + 
  geom_smooth(method = "lm", se = TRUE) + # Linear regression line with SE
  labs(title = "",
       x = "% Practice Questions Answered",
       y = "% Correct Exam Points",
       color = "Education Level") +
  theme_minimal() +
  scale_color_discrete(name = "Education Level") +
  scale_y_continuous(breaks = seq(0, 1, 0.05))



# CREATE MORE ACCESSIBLE INTERACTION PLOT
# Load the viridis package for accessible color palette
#install.packages("viridis")  # If not installed
library(viridis)

plot_interaction_practice_education <- function(data, unique_practice_questions_answered, predicted, education_level) {
  # Plot interaction between unique practice questions and education level
  ggplot(data, aes(x = unique_practice_questions_answered, y = predicted, color = education_level)) +
    geom_line() +
    labs(title = "Interaction between Unique Practice Questions Answered and Education Level",
         x = "Practice Questions Answered Z-scored",
         y = "Predicted Exam Points Z-scored",
         color = "Education Level") +
    theme_minimal() +
    scale_color_viridis_d(name = "Education Level")  # Use discrete viridis color palette
}

# Call the function
plot_interaction_practice_education(data, data$unique_practice_questions_answered, predicted, data$education_level)


# Second analysis: Practice effect considering prior instruction and education level

model_add <- lm(exam_points ~ proportion_of_prior_insutrction + unique_practice_questions_answered + education_level_ordinal_ranked, data)
summary(model_add)

model_int<- lm(exam_points ~ proportion_of_prior_insutrction*unique_practice_questions_answered + education_level_ordinal_ranked, data)
summary(model_int)

anova(model_add, model_int)

# Q: TODO: Can we save this to a file?  
sjPlot::tab_model(model_int)

plot(model_int) # there is an outlier


# Visualize Interaction between Prior Instruction and Practice

data$predicted <- predict(model_int, newdata = data)


#Mark learners about the median high performance
d2 <- data %>% 
  mutate(high_pi = proportion_of_prior_insutrction > median(proportion_of_prior_insutrction, na.rm=TRUE)) %>%
  filter(!is.na(high_pi))

ggplot(d2, aes(x = unique_practice_questions_answered, y = predicted, color = high_pi)) +
  geom_point() +
  geom_smooth(method = "lm", aes(group = high_pi)) +
  labs(title = "Interaction Between Prior Insutrction and Practice", x = "Practice", y = "Exam Points") +
  theme_minimal()

###### Q: Is the rest of this extra code? ####################################

summary(model_int)

# Remove students with less than x number of survey; unique_practice_questions_answered_scaled_by_max

# Re-run with categorical

model_add <- lm(exam_points ~ proportion_of_prior_insutrction + education_level_ordinal_ranked, data)
summary(model_add)

model_int <- lm(exam_points ~ prior_insutruction_reporting_frequency_scaled_by_max * education_level_ordinal_ranked, data)
anova(model_add, model_int)

summary(model_int)

library(ggplot2)

# Create predictions using the interaction model


ggplot(data, aes(x = unique_practice_questions_answered, y = predicted, color = as.factor(education_level_ordinal_ranked))) +
  geom_line() +
  labs(title = "Interaction between Unique Practice Questions Answered and Education Level",
       x = "X",
       y = "Predicted Exam Points",
       color = "Education Level") +
  theme_minimal() +
  scale_color_discrete(name = "Education Level")



library(ggplot2)

# Create a new data frame with predictions from the interaction model
d_model$predicted <- predict(model_int, newdata = data)

# Plot the interaction
ggplot(d_model, aes(x = unique_practice_questions_answered, y = predicted)) +
  geom_line() +
  labs(title = "Interaction between Unique Practice Questions Answered and Education Level",
       x = "Unique Practice Questions Answered",
       y = "Predicted Exam Points") +
  theme_minimal()


# 
usdm::vifcor(data %>% select_if(is.numeric)) 


summary(model_add)
plot(model_add)

cor(data$prior_insutruction_reporting_frequency, data$unique_practice_questions_answered)
cor(data$proportion_of_prior_insutrction, data$unique_practice_questions_answered, use='pairwise.complete.obs')



plot(data$prior_insutruction_reporting_frequency, data$unique_practice_questions_answered)

plot(data$prior_insutruction_reporting_frequency_scaled_by_max, data$unique_practice_questions_answered_scaled_by_max)

d_tmp <- data %>%
  mutate(high_inst = prior_insutruction_reporting_frequency < median(prior_insutruction_reporting_frequency, na.rm=TRUE)) %>%
  mutate(high_prac = unique_practice_questions_answered < median(unique_practice_questions_answered, na.rm=TRUE))
  
xtabs(~high_inst+high_prac, d_tmp)


summary(model_add)
plot(model_add)

