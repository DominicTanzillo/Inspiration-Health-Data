# Inspiration-Health-Data  
510-First-Project  
## Team  
### Students  
- Mrinal Goel
- Dominic Tanzillo  

### Professor  
- Brinnae Bent, PhD  

### Original Data Source  
Chris Mason, PhD, and Eliah Overbey, PhD in conjunction with NASA and SpaceX  

---

## Project Overview  

### Data  
We worked with open-source data from NASA’s Inspiration4 Mission, a 3-day flight in September 2021 that sent four private astronauts into low Earth orbit.  

Blood samples were collected before, during, and after flight (L-92, L-44, L-3; R+1, R+45, R+82). Serum was separated and sent for immune and cardiovascular cytokine panels (Eve Technologies, Alamar) and comprehensive metabolic testing (Quest Diagnostics). These data capture how cytokines and metabolic measures shift during spaceflight.  

Citation  
Mason CE, Overbey EG, Grigorev K, Nelson TM.  
> "SpaceX Inspiration4 Blood Serum Metabolic Panel and Immune/Cardiac Cytokine Arrays (Comprehensive Metabolic Panel and Multiplex)," NASA Open Science Data Repository, Version 3. [DOI link](http://doi.org/10.26030/mc5d-p710)  

Raw datasets available at [NASA GeneLab](https://osdr.nasa.gov/bio/repo/data/studies/OSD-575).  

---  

### Project Scope  
We focused on the Comprehensive Metabolic Panel (CMP) and Cardiovascular Serum Proteins as markers of astronaut health under microgravity.  

The sample size is small (n=4), but balanced: two men and two women, enabling basic sex-based comparisons. 

---

## Project Architecture  

### Repo Structure  
After iterating through multiple deployment issues, the repo was organized as:  

```
.
├── app.py                   # Main app entrypoint (runs the web/app interface)
├── main.py                  # Command-line entrypoint for running the pipeline
├── preprocessing.py         # Preprocessing script to clean raw data before analysis
├── scripts/                 # Core analysis modules
│   ├── featureEngineering.py # Functions to create derived features from cleaned data
│   ├── stats.py              # Statistical analysis methods and calculations
│   └── graphMaking.py        # Visualization utilities for data and results
├── data/                    # Raw input datasets (CSV files directly from source)
│   └── *.csv
├── cleaned_data/            # Outputs after preprocessing (ready for feature engineering)
│   └── *.csv
├── final_data/              # Tidy, analysis-ready datasets for the app or reporting
│   └── *.csv
├── writeup.ipynb            # Supplementary documentation and narrative analysis (notebooks)
├── README.md                # Project summary, setup instructions, and usage guide
├── requirements.txt         # Python dependencies for reproducibility
├── Dockerfile               # Container setup for deployment on Hugging Face

```
Please note that this tree was generated via ChatGPT: [prompt](https://chatgpt.com/share/68db83d2-e904-8008-8226-3137ff231942)

### Project Pipeline  
1. Preprocessing: Cleaned and organized astronaut biomarker datasets  
2. Exploration: Identified key features and focused on the most informative biomarkers  
3. Feature engineering: Created new measures (e.g., Anion Gap) and aligned data on a flight-day timeline  
4. Reshaping: Converted data into tidy format for easier analysis and plotting  
5. Statistics: Ran within-astronaut and group-level tests  
6. Visualization: Built interactive charts and deployed them in a Streamlit app  

### Deployment to Hugging Face  

The interactive dashboard is deployed on Hugging Face: [Inspiration-Health-Data](https://huggingface.co/spaces/DTanzillo/Inspiration-Health-Data)  

To run locally:

```
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

## Full write-up for this project's process and to try it yourself:

[Write-Up](writeup.ipynb) in Jupyter Notebook. Template curtesy of Duke's AIPI Progam's 520 Class (Originally, this was used for a bike share project)

## Key-Take Aways
### Lessons Learned for Building Projects
* SciPy wheels: Latest releases may not build on Hugging Face so we pinned to 1.12.0.
* NumPy conflicts: Cutting-edge versions caused dependency clashes. 
* Repo layout: Keeping app.py at root simplified imports and Docker path issues. Stable pinning solved it.
* Data availability: Committed final_data/ into repo so app always finds CSVs. Hugging Face is really particular!

### Final Outputs

* Interactive Dashboard: [Hugging Face Space visualizing astronaut biochemistry across mission days.](https://huggingface.co/spaces/DTanzillo/Inspiration-Health-Data)
* Graphs: Plotly charts with selectable analytes, astronauts, error bands, and reference ranges.
* Data Storytelling Deliverables: README, [Write-Up](writeup.ipynb), class presentation.
* Blog Post: [On Substack](https://open.substack.com/pub/dominictanzillo/p/an-application-to-visual-astronaut?r=1ucxnk&utm_campaign=post&utm_medium=web&showWelcomeOnShare=true)