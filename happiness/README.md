# Automated Dataset Analysis

The dataset we are analyzing offers valuable insights into various factors affecting well-being across different countries, represented through various quantitative measures. With 2,363 observations spanning from 2005 to 2023, it includes key indicators such as the "Life Ladder," "Log GDP per capita," "Social support," "Healthy life expectancy at birth," "Freedom to make life choices," and measures of affect such as "Positive affect" and "Negative affect." 

### Data Overview

- **Country Coverage**: The data includes 165 unique countries, with Lebanon having the highest frequency of entries (18).
- **Temporal Span**: The observations span 19 years, with an average year of 2014.76.
- **Key Metrics**: 
  - The mean "Life Ladder" score is approximately 5.48, signaling an average level of subjective well-being across the dataset.
  - "Log GDP per capita" averages at 9.40, which provides insights into economic conditions.
  - The social support metric has an average of 0.81, indicating a relatively strong social framework in many sampled countries.

### Missing Values

The analysis revealed several missing values across various columns, highlighting gaps that could impact the reliability of the insights drawn:
- "Log GDP per capita" has 28 missing entries.
- "Healthy life expectancy at birth" exhibits the highest number of missing values, at 63.
- Other metrics like "Generosity" and "Perceptions of corruption" also show notable missing data.

### Correlation Analysis

A heatmap was generated to visualize the correlation between various aspects of well-being:
- **Strong Positive Correlations**:
  - A significant correlation exists between "Life Ladder" and "Log GDP per capita" (0.78), suggesting that higher GDP per capita is associated with greater reported life satisfaction.
  - Similarly, "Social support" and "Healthy life expectancy" also show strong relationships with the "Life Ladder".
- **Negative Correlations**:
  - There is a notable negative correlation between "Life Ladder" and "Perceptions of corruption" (-0.43), indicating that countries with higher corruption perceptions tend to report lower well-being.

This correlation analysis indicates that economic performance, social support systems, and perceptions of governance are critical determinants of well-being.

### Country-Level Analysis

The dataset was also explored to gain insights into well-being standings by country:
- A count plot highlighted the distribution of data entries by country, providing a visual representation of which countries are overrepresented in the dataset.
- Notably, countries with high entries may indicate either a larger sample size or more fluctuations in well-being indicators over time, which could merit further investigation.

### Temporal Distribution

A distribution visualization of years indicates that most data concentrate around the mid-2010s. This temporal bias may suggest that insights drawn from this dataset could be more applicable to this period rather than reflecting more recent situations accurately. 

### Implications

The findings from this dataset have several implications:
- **Policy Development**: Nations may benefit from focusing on enhancing economic performance while also addressing social support and corruption to improve overall well-being.
- **Further Research**: The high number of missing values in some key indicators, such as healthy life expectancy, points to the need for further data collection to provide a more holistic view of global well-being.
- **Cross-Country Strategies**: Countries may look towards those with higher life ladder scores and stronger social support systems as models for improving their own metrics.

### Conclusion

Overall, the dataset offers a rich framework for understanding global well-being. The relationships identified between well-being indicators and the economic/social context could inform policy interventions aimed at fostering improvements in citizens' life satisfaction levels. Better data collection and continued monitoring of these indicators will be essential for ongoing analysis and improvement efforts.

![D:\TDS_Project_2\project2\output\missing_values.png](D:\TDS_Project_2\project2\output\missing_values.png)

![D:\TDS_Project_2\project2\output\correlation_heatmap.png](D:\TDS_Project_2\project2\output\correlation_heatmap.png)

![D:\TDS_Project_2\project2\output\count_plot_Country name.png](D:\TDS_Project_2\project2\output\count_plot_Country name.png)

![D:\TDS_Project_2\project2\output\distribution_year.png](D:\TDS_Project_2\project2\output\distribution_year.png)

