# SciPy Probability Distributions Visualizer

Visualize probability distributions from **SciPy** using **Plotly-Dash**.

 - [Probability Distributions](https://en.wikipedia.org/wiki/List_of_probability_distributions)
 - [SciPy Stats Reference](https://docs.scipy.org/doc/scipy/reference/stats.html)
 - [Plotly Dash](https://dash.plotly.com/)
  
### Demo

Freely hosted [here](http://nbpub.pythonanywhere.com/), availability not guaranteed.

----

### Contents
 - [Code Notes](#code-notes)
   - [Overview](#overview)
   - [For Me](#for-me)
 - [Installation](#installation)
   - [WSGI](#wsgi)

## Code Notes

### Overview

 - **[app.py](/app.py)**
   - load distributions from SciPy, setup dash application, handle callbacks
 - **[distributions.py](/distributions.py)** 
   - functions to
     - update info text and parameter inputs on page with distribution choice   
	 - generate histogram and violin plots from given distribution and parameters
	   - five thousand points generated: `<distribution>.rvs(<shape_parameters>,<loc>,<scale>,5000)

### For Me

 - Python
   - class inspection to extract distributions and their information from SciPy
 - SciPy
   - experience with probability distributions, code, documentation
 - Dash, Plotly
   - graphs with custom hover data, colors, titles
     - only use **[Go]()** figures, so plotly-express and pandas are not required packages  
   - advanced callback usage, *works, but imperfectly. not production grade*
     - distribution selection from dropdown determines parameters (and info text) which determine graphs
	   - graphs updated by sliders or text inputs
	   - sliders and text boxes update if their corresponding partner is changed
	     - *circular callback warning*, causes graphs to update twice each time
   - simple single page application, easy deployment
   - minimal CSS styling, no CSS/JSS toolkits like Bootstrap
     - could use something to display LaTeX, SciPy docs utilize sphinx which uses MathJax?

## Installation

 - requirements.txt lists all packages frozen in my development environment
 - install [dash](https://dash.plotly.com/installation) and [SciPy](https://scipy.org/install/) in a Python environment to run the applcation

----

The code can be run from a virtual environment on your local machine. 
[Download](https://github.com/NBPub/probability_distribution_viz/archive/refs/heads/main.zip) the code to a new directory, `your-directory` 

*Only the python files `.py` and assets (`your-directory/assets`) directory are necessary to run the application.*

```bash
# Adapt for your operating system

cd your-directory
python -m venv venv
venv\scripts\activate
python -m pip install --upgrade pip

# install packages via requirements.txt
pip install -r requirements.txt 
# or install packages separately
pip install dash scipy

# ensure server settings are ok
python -m app
```

The application will be available on the default port, `8050`, at `http://127.0.0.1:8050/`. 
Change DEBUG settings or adapt deployment for WSGI by modying the [run command](/app.py#L155).

### WSGI

 - comment out run command
 - import `app` from [app.py](/app.py) into your WSGI of choice
   - I think PythonAnywhere uses **[uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/)** with NGINX