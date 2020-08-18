<br>
<br>

<h1 style="text-align:center;"> Cegal Tools package for loading and visualising well log data</h1>
<h4 style="text-align:center;"> An geoscience tool for loading, plotting and evaluating well log data using python 🐍</h4>

<br><br>
    

    
<br>


> The Cegal Tools package aims to minimize time and effort for a geoscientist wanting to work with well logs using python.


> Based on open source tools such as plotly, pandas and lasio, Cegal Tools allow for simple loading, manipulation and visualising of well logs from las files.

    
> Several built in plotting methods provides an easy to use, out of the box well log tool for geoscientists using or wanting to learn python.

<br><br>



Cegal well tool package; written by Hilde Tveit Håland & Thomas Bartholomew Grant, Cegal ASA, May 2020.
    
    
License: BSD-3-Clause 

<br><br>

### Content

 * [Using the well plotter from the Cegal Tools package](#Using-the-well-plotter-from-the-Cegal-Tools-package) 
 * [Creating a Well object using the Cegal Tools](#Creating-a-Well-object-using-the-Cegal-Tools)
 * [Built in plots for the Well object](#Built-in-plots-for-the-Well-object) 
 * [Adding logs and writing Well object as las file](#Adding-logs-and-writing-Well-object-as-las-file)
 
 <br>

<br><br>

## Using the well plotter from the Cegal Tools package

<br>

Installing cegal tools package:

* **!pip install cegaltools**



The purpose of Cegal Tools Plotting is create a quick and easy way to QC well logs in a jupyter notebook. It's built using plotly, so run in a different IDEs html plots will launch in your default browser. 

<br><br>    

    from cegaltools.plotting import CegalWellPlotter as cwp
    
    cwp.plot_logs(df=dataframe, 
              logs=['gammaray','density', 'porosity'], 
              log_scale_logs='resistivity',
              lithology_logs='lithology', 
              lithology_proba_logs='lithology_probability')
              
    out:
 
![Log viewer](https://github.com/cegaltools/cegaltools/images/cwp_plot_logs.png)            


<br><br>

    cwp.plot_correlation(df=dataframe)

    out:

![correlation plot](https://github.com/cegaltools/cegaltools/images/cwp_correlation.png)

<br><br>

    cwp.plot_coverage(df=dataframe)

    out: 
 
![Coverage plot](https://github.com/cegaltools/cegaltools/images/cwp_plot_coverage.png)   

<br>

