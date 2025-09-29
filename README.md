# Inspiration-Health-Data  
510-First-Project  

## Team  
### Students  
- Dominic Tanzillo  
- Mrinal Goel  

### Professor  
- Brinnae Bent, PhD  

### Original Data Source  
Chris Mason, PhD, and Eliah Overbey, PhD in conjunction with NASA and SpaceX  

---

## Project Overview  

### Data  
We began with data from NASA's **Inspiration4 Mission: A 3-Day Trip Circulating Around Earth in Microgravity**.  

> *SpaceX Inspiration4 Blood Serum Metabolic Panel and Immune/Cardiac Cytokine Arrays (Comprehensive Metabolic Panel and Multiplex) Study*  

#### NASA Open-Source Database  
The SpaceX Inspiration4 mission was a 3-day mission with four private astronauts to low Earth orbit that occurred in September 2021. The crew collected biospecimen samples before, during, and after flight. One of these biospecimen collections included whole blood collected via venipuncture, with serum extracted from blood using a serum separator tube (SST). Samples were collected pre-flight (L-92, L-44, L-3) and post-flight (R+1, R+45, R+82).  

Serum samples were submitted for immune and cardiovascular cytokine biomarker profiling panels at two different companies (Eve Technologies and Alamar), and to Quest Diagnostics for comprehensive metabolic panel testing. Data was used to measure changes in cytokines and metabolic measures during spaceflight.  

##### Study Citation  
Mason CE, Overbey EG, Grigorev K, Nelson TM.  
*"SpaceX Inspiration4 Blood Serum Metabolic Panel and Immune/Cardiac Cytokine Arrays (Comprehensive Metabolic Panel and Multiplex)",* NASA Open Science Data Repository, Version 3, [DOI link](http://doi.org/10.26030/mc5d-p710)  

Raw dataset available from NASA's Gene Lab [here](https://osdr.nasa.gov/bio/repo/data/studies/OSD-575).  

---

### Project Scope  
We focused on the **Comprehensive Metabolic Panel (CMP)** and **Cardiovascular Serum Proteins**. These are related to baseline astronaut health in response to microgravity, and we can model the health trajectories over time.  

Participant size is limited at *n=4*. Importantly, we have two male and two female subjects, allowing comparison across sexes.  

---

## Project Architecture  

### Repo Structure  
After iterating through multiple deployment issues, the repo was organized as:  

```
.
├── app.py                   # main app entrypoint
├── scripts/                 # core analysis modules
│   ├── featureEngineering.py
│   ├── stats.py
│   └── graphMaking.py
├── data/                    # raw NASA datasets (original form)
│   ├── raw_serum.csv
│   └── raw_cardiovascular.csv
├── cleaned_data/            # datasets after EDA + preprocessing
│   ├── serum_cleaned.csv
│   └── cardiovascular_cleaned.csv
├── final_data/              # tidy, analysis-ready CSVs used in the app
│   ├── serum_cardiovascular.csv
│   └── clinical_chemistry.csv
├── requirements.txt         # Python dependencies
├── Dockerfile               # containerized build for Hugging Face
└── README.md
```

### Requirements  
We locked to stable, compatible versions to avoid conflicts on Hugging Face:  

```
numpy==1.26.4
pandas==2.2.2
scipy==1.12.0
plotly==5.24.1
streamlit==1.38.0
```

### Project Pipeline  
1. **Preprocessing**: Cleaned NASA-transformed datasets for astronaut biomarkers. 
2. **Exploratory Data Analysis**: Considered Relevant Features to Emphasis and Tunnel in On
2. **Feature Engineering**: Added derived measures (e.g., Anion Gap, flight-day indexing). Considered relevant statistics and how to display. 
3. **Tidy Conversion**: Wide to tidy long format with `tidy_from_wide()`.  
4. **Statistical Analysis**: Within-astronaut and group comparisons with SciPy.  
5. **Visualization**: Interactive Plotly charts embedded in Streamlit dashboard.  

---

## Deployment to Hugging Face  

Hugging Face Interactable [Available Here](https://huggingface.co/spaces/DTanzillo/Inspiration-Health-Data)

We initially tried the **Streamlit SDK**, then switched to **Docker** for full control on Hugging Face. To Run Locally:

```
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

## Full write-up for this project:

[Write-U](writeup.ipynb)

## Key-Take Aways
### Lessons Learned
* SciPy wheels: Latest releases may not build on Hugging Face so we pinned to 1.12.0.
* NumPy conflicts: Cutting-edge versions caused dependency clashes. Stable pinning solved it.
* Repo layout: Keeping app.py at root simplified imports and Docker path issues.
* Data availability: Committed final_data/ into repo so app always finds CSVs.

### Outputs

* Interactive Dashboard: [Hugging Face Space visualizing astronaut biochemistry across mission days.](https://huggingface.co/spaces/DTanzillo/Inspiration-Health-Data)
* Graphs: Plotly charts with selectable analytes, astronauts, error bands, and reference ranges.
* Data Storytelling Deliverables: README,[Write-Up](writeup.ipynb), class presentation.