# Load the readxl package
library(readxl)
library(ggplot2)
library(dplyr) # For data manipulation (calculating means)

# Read the Excel file
excel_data <- read_excel("SpecieVSAssemblyLength.xlsx") # Replace "data.xlsx" with your file name

# View the data
print(head(excel_data))

plot <- ggplot(excel_data, aes(x = Assembly_length, y = Specie, color = Specie, fill = Specie)) +
  geom_boxplot(alpha = 0.5, width = 0.5) +  # Adjust width for better boxplot appearance
  geom_jitter(width = 0.2, height = 0.1, alpha = 0.7) +
  scale_x_continuous(labels = function(x) paste0(x / 1e6, "M")) +
  labs(
    title = "Assembly Length by Specie",  # Corrected title
    x = "Assembly Length",               # Corrected x label
    y = "Specie"
  ) +
  theme_light() +  # Using theme_light() as a base
  theme(
    legend.position = "none",
    plot.title = element_text(hjust = 0.5), # Center the title
    axis.title.x = element_text(margin = margin(t = 10)), # Add space below x-axis label
    axis.title.y = element_text(margin = margin(r = 10))  # Add space to the right of y-axis label
  )

# Save the plot as a PNG file
ggsave("assembly_length_plot.png", plot, width = 8, height = 6, units = "in", dpi = 300)




# Calculate the mean assembly length for each species
mean_assembly_lengths <- excel_data %>%
  group_by(Specie) %>%
  summarise(mean_length = mean(Assembly_length))

# Calculate boxplot statistics to get the x-axis positions
boxplot_stats <- excel_data %>%
  group_by(Specie) %>%
  summarise(
    lower = quantile(Assembly_length, 0.25),
    upper = quantile(Assembly_length, 0.75)
  )

# Combine mean and boxplot stats
mean_assembly_lengths <- left_join(mean_assembly_lengths, boxplot_stats, by = "Specie")

# Create the plot
plot <- ggplot(excel_data, aes(x = Specie, y = Assembly_length, color = Specie, fill = Specie)) +
  geom_boxplot(alpha = 0.5, width = 0.5) +
  geom_segment(data = mean_assembly_lengths, 
               aes(x = as.numeric(factor(Specie)) - 0.2, xend = as.numeric(factor(Specie)) + 0.2, 
                   y = mean_length, yend = mean_length, color = Specie),
               linetype = "dashed") +
  scale_y_continuous(labels = function(x) paste0(x / 1e6, "M")) +
  labs(
    title = "Assembly Length by Specie",
    x = "Specie",
    y = "Assembly Length"
  ) +
  theme_light() +
  theme(
    legend.position = "none",
    plot.title = element_text(hjust = 0.5),
    axis.title.x = element_text(margin = margin(t = 10)),
    axis.title.y = element_text(margin = margin(r = 10))
  )

ggsave("assembly_length_boxplot_mean.png", plot, width = 8, height = 6, units = "in", dpi = 300)




plot <- ggplot(excel_data, aes(x = as.numeric(factor(Specie)) - 0.4, y = Assembly_length, color = Specie, fill = Specie)) +
  geom_violin(aes(x = as.numeric(factor(Specie))), alpha = 0.5, trim = FALSE) +  # Keep violins centered
  geom_boxplot(aes(x = as.numeric(factor(Specie))), width = 0.07, color = "black", alpha = 0.5, outlier.shape = NA) +  # Boxplot centered
  geom_jitter(width = 0.08, height = 0, alpha = 0.7, size = 1.5) +  # Reduce jitter width
  scale_x_continuous(breaks = 1:length(unique(excel_data$Specie)), labels = unique(excel_data$Specie)) +  # Fix x-axis labels
  scale_y_continuous(labels = function(x) paste0(x / 1e6, "M")) +
  labs(
    title = "Assembly Length by Specie",
    x = "Specie",
    y = "Assembly Length"
  ) +
  theme_light() +
  theme(
    legend.position = "none",
    plot.title = element_text(hjust = 0.5),
    axis.title.x = element_text(margin = margin(t = 10)),
    axis.title.y = element_text(margin = margin(r = 10))
  )


# Save the plot as a PNG file
ggsave("assembly_length_violin_boxplot_jitter.png", plot, width = 8, height = 6, units = "in", dpi = 300)
