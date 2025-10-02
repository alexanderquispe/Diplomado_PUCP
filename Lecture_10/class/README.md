## Simpson's Paradox Dashboard with Python

This dashboard was based off of the dashboard made by [Bach and Tan](https://github.com/DigitalCausalityLab/simpsonsparadox) to demonstrate the same phenomenon. This example is taken from Glymour et al. (2016)

### Running locally

To run locally, it is advisable to first create a virtual environment

You will need to have Python installed and in your `PATH`. While located in the root directory of this repository, 

```
python -m venv env
```

Now activate the virtual environment:

#### Windows

```
env/Scripts/activate
```

#### Linux/MacOS

```
source env/bin/activate
```

Now you must install the necessary dependencies to run the dashboard:

```
pip install -r requirements.txt
```

This should take a few minutes. Once it is done, you can run the streamlit application:

```
streamlit run src/streamlit_app.py
```

This should start a locally hosted server and automatically open a browser tab with the application

### References

Glymour, Madelyn, Judea Pearl, and Nicholas P. Jewell. Causal inference in statistics: A primer. John Wiley & Sons, 2016. 
