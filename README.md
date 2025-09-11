# Inspiration-Health-Data
510-First-Project
## Team
### Students
Dominic Tanzillo
Mrinal Goel
### Professor
Brinnae Bent, PhD

### Original Data Source
Chris Mason, PhD, and Eliah Overbey, PhD in Conjuction with NASA and SpaceX

## Project Overview

### Data
We began with data from NASA's Inspiration4 Mission: A 3-Day Trip Circulating Around Earth in Micrograbity.

> SpaceX Inspiration4 Blood Serum Metabolic Panel and Immune/Cardiac Cytokine Arrays (Comprehensive Metabolic Panel and Multiplex) Study

#### NASA Open-Source Database
Description:
> The SpaceX Inspiration4 mission was a 3-day mission with four private astronauts to low Earth orbit that occurred in September 2021. The crew collected biospecimen samples before, during, and after flight. One of these biospecimen collections included whole blood collected via venipuncture, with serum extracted from blood using a serum separator tube (SST). Samples were collected pre-flight (L-92, L-44, L-3) and post-flight (R+1, R+45, R+82). Serum samples were submitted for immune and cardiovascular cytokine biomarker profiling panels at two different companies (Eve Technologies and Alamar), and to Quest Diagnostics for comprehensive metabolic panel testing. Data was used to measure changes in cytokines and metabolic measures during spaceflight. This study derives results from the Comprehensive Metabolic Panel and Multiplex assays, and the blood serum data in this study are related to other studies using data from the same experiment; OSD-569 (whole blood), OSD-570 (peripheral blood mononuclear cells), OSD-571 (plasma), OSD-572 (skin, oral, and nasal swabs), OSD-573 (Dragon capsule samples), OSD-574 (skin biopsy), OSD-656 (urine), and OSD-630 (stool).

##### Study Citation
>Mason CE, Overbey EG, Grigorev K, Nelson TM. "SpaceX Inspiration4 Blood Serum Metabolic Panel and Immune/Cardiac Cytokine Arrays (Comprehensive Metabolic Panel and Multiplex)", NASA Open Science Data Repository, Version 3, http://doi.org/10.26030/mc5d-p710

Raw data set available from NASA's Gene Lab [here](https://osdr.nasa.gov/bio/repo/data/studies/OSD-575).

### Project Scope
We focused on the Comprehensive Metabolic Panel (CMP) and Cardiovascular Serum Proteins. These are related to baseline astronaut health in response to microgravity and we can model the health trajectories over time.

Participant size is limited at $n=4$. Interestingly, we have two male and two female subjects and so we can compare across the sexes.

## Project Architecture

### Requirements
See [enviornment.yml](environment.yml)

## Project Pipeline
For this project, there are Submitted and Transformed Datasets. We began with the transformed datasets as they provided better visibility for preprocessing.

### Preprocessing
### EDA
### Feature Manipulation

## Outputs
### Social Media
### Graphs


---
## Assignment Description
Module Project 1: Data Storytelling         The Untold Stories in Public Data
This project is an opportunity to apply your data science skills to find and tell a compelling, data-driven story. You and your partner will select a publicly available dataset, explore and preprocess the data, engineer relevant features, and use visualizations and narrative techniques to communicate your insights. The project emphasizes thoughtful framing, ethical considerations, and clear communication to a general audience.

Learning Goals
Practice sourcing and evaluating real-world datasets
Use exploratory data analysis to uncover trends, patterns, and surprises
Apply preprocessing and feature engineering techniques to enhance analysis
Understand and reflect on data limitations, bias, and ethical implications
Translate technical findings into a clear, engaging public-facing product
Collaborate using GitHub and follow best practices for reproducible analysis

Deliverables
Your final deliverables consist of a public communication piece, a GitHub repository, and an in-class presentation.

1. Public Communication Deliverable (submitted as link)
Choose one of the following formats to communicate your data story to a general audience. Your work should be accessible, engaging, and accurate while still grounded in your analysis. It is fine to submit a link to an unlisted YouTube video or a draft blog in Byline, but make sure we can access it!

Format Options (pick one):

A blog post
A podcast episode
A YouTube video 
An infographic + brief written explanation

Must include:

A clear and engaging title
An explanation of why this story matters and who it's for (your audience)
Key findings supported by visualizations and examples
Discussion of data limitations, bias, and ethical implications (in accessible language)
A compelling narrative arc—what surprised you? What should we take away?
2. GitHub Repository (submitted as link)
Your repo must include:

All code used for preprocessing, EDA, and feature engineering (scripts, not just notebooks)
A README with:
Overview of your project
Dataset description and citation
Step-by-step instructions to reproduce your analysis
Use of branches and pull requests
Each group member must make at least one PR
Use best practices for reviews and commits
Raw and cleaned data (or, if restricted, a clear description of how to access/generate it)

3. Presentation (8 minutes max) (presented in class on Sep 30th)
Prepare a clear and engaging presentation that summarizes:

Your audience and why this story matters
Your dataset and topic of interest
Key trends and visualizations uncovered during EDA
Any engineered features that shaped your analysis
The story your data tells and its ethical implications
Final takeaways
Example Projects
Blog: “Greener for Some: Who Has Access to Urban Green Space in U.S. Cities?”
Video: “Why Are Some Intersections So Dangerous? A Look at Traffic Fatalities”
Podcast: “Food Deserts: Data vs. Reality”
Infographic: “What Public Salary Data Tells Us About Pay Gaps by Gender”

---

Updating the yaml

```
conda install <package>
conda env export --from-history > environment.yml
```