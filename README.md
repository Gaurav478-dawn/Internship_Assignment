# Project Submission: Disease Spread/ Covid Analysis

**Name:** Gaurav Khadka
**Domain:** AI in HealthCare

## Project Title
Interactive COVID-19 Analytics Dashboard

## Problem Statement
The COVID-19 pandemic generated a massive volume of time-series data across the globe. Static reports often fail to capture the dynamic nature of the disease's spread, making it difficult to analyze infection rates, recovery progress, and mortality trends over specific timeframes. There is a critical need for an interactive tool that enables users to filter data by date and region to gain actionable insights into the pandemic's trajectory.

## Objective
The primary objective of this project is to develop a fluid, interactive dashboard using Python that allows users to:
1.  Visualize the global progression of the pandemic including Confirmed, Active, Recovered, and Death counts.
2.  Perform granular analysis on specific nations to understand local disease trajectories.
3.  Compare infection spread against mortality rates using dynamic, togglable charts.
4.  Provide a user-friendly interface with sliders and dropdowns for data exploration without requiring code modifications.

## Dataset Description
The project utilizes the **Novel Corona Virus 2019 Dataset**, specifically the `covid_19_data.csv` file. Key features include:
* **ObservationDate:** The date of the data record.
* **Province/State:** The state or province level detail (if available).
* **Country/Region:** The country level detail.
* **Confirmed:** Cumulative number of confirmed cases.
* **Deaths:** Cumulative number of deaths.
* **Recovered:** Cumulative number of recovered cases.

*Note: Feature engineering was applied to calculate "Active" cases (Confirmed - Deaths - Recovered) and "Mortality Rate" ((Deaths / Confirmed) * 100).*

## Methodology / Approach
1.  **Data Ingestion & Cleaning:**
    * Loaded raw CSV data using Pandas.
    * Converted dates to datetime objects for accurate time-series plotting.
    * Standardized country names (e.g., handling 'Mainland China') to ensure consistent aggregation.
2.  **Feature Engineering:**
    * Calculated 'Active Cases' to provide a more accurate picture of current strain on healthcare systems.
    * Computed 'Mortality Rate' percentages for trend analysis.
3.  **UI & Interaction Design:**
    * Developed a "Fluid UI" layout using `ipywidgets` to create a seamless user experience within the notebook.
    * Implemented toggle buttons to switch views between Global and Nation analysis to reduce visual clutter.
    * Created dynamic HTML "KPI Cards" to display summary statistics prominently.
4.  **Visualization:**
    * Utilized **Plotly** for rendering interactive line and area charts that support zooming and hovering.

## Tools & Technologies Used
* **Python:** Core programming language.
* **Pandas:** For efficient data manipulation and aggregation.
* **Plotly (Express & Graph Objects):** For creating high-quality, interactive visualizations.
* **ipywidgets:** For building the interactive controls (Sliders, Dropdowns, Toggles) directly in the environment.
* **Google Colab:** The development and execution environment.

## Steps to Run the Project
1.  **Prerequisites:** Ensure the following Python libraries are installed:
    ```bash
    pip install pandas plotly ipywidgets
    ```
2.  **Data Setup:**
    * Download the `covid_19_data.csv` file.
    * Upload the file to your Google Colab session (click the folder icon on the left sidebar and drag the file in).
3.  **Execution:**
    * Copy the provided Python code into a code cell.
    * Run the cell.
4.  **Usage:**
    * **Select View:** Use the toggle buttons to switch between "Global" and "Nation" modes.
    * **Filter Date:** Drag the slider to adjust the time range for the analysis.
    * **Analyze Nation:** In "Nation" mode, select a country from the dropdown. Use the Chart toggle to switch between "Spread Trajectory" and "Mortality Rate".

## Results / Output
The program outputs a comprehensive dashboard featuring:
* **Global Overview:** A trend line showing the accumulation of cases worldwide and summary cards for total metrics.
* **Nation Analysis:**
    * **Spread Trajectory:** A multi-line chart comparing Confirmed, Active, and Death counts over time.
    * **Mortality Rate:** A filled area chart displaying the fluctuation of the mortality percentage.
    * **Dynamic KPIs:** Summary boxes that update instantly based on the selected country and date range.
