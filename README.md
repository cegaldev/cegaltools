<br>
<br>

<h1 style="text-align:center;"> Cegal Tools package <br> loading and visualising well log data</h1>
<h4 style="text-align:center;"> An geoscience tool for loading, plotting and evaluating well log data using python 🐍</h4>

<br><br>
    

    
<br>


> The Cegal Tools package aims to minimize time and effort for a geoscientist wanting to work with well logs using python.


> Based on open source tools such as plotly, pandas and lasio, Cegal Tools allow for simple loading, manipulation and visualising of well logs from las files.

    
> Several built in plotting methods provides an easy to use, out of the box well log tool for geoscientists using or wanting to learn python.

<br><br>



Cegal well tool package; written by [Hilde Tveit Håland](https://www.linkedin.com/in/hilde-tveit-h%C3%A5land-216a267b
) and [Thomas Bartholomew Grant](https://www.linkedin.com/in/thomas-bartholomew-grant-31b86359), Cegal ASA, August 2020.


    
    
License: BSD-3-Clause 

<br><br>

### Content

 * [Using the well plotter from the Cegal Tools package](#Using-the-well-plotter-from-the-Cegal-Tools-package) 
 * [Creating a Well object using the Cegal Tools](#Creating-a-Well-object-using-the-Cegal-Tools)
 * [Built in plots for the Well object](#Built-in-plots-for-the-Well-object) 
 * [Adding logs and writing Well object as las file](#Adding-logs-and-writing-Well-object-as-las-file)
 
 <br>

Check out the Example notebooks in the Notebooks folder for more detailed examples 🍰

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
 
![Log viewer](https://github.com/cegaltools/cegaltools/blob/master/images/cwp_plot_logs.png)            

The four log options for cwp.plot_logs are:
1. logs: logs to plot with normal scale
1. log_scale_logs: logs to plot with logarithmic scale
1. lithology_logs: lithology logs to plot as full trace color fill
1. lithology_proba_logs: lithology probability logs scaled from 0 to 1



<br><br>

    cwp.plot_correlation(df=dataframe)

    out:

![correlation plot](https://github.com/cegaltools/cegaltools/blob/master/images/cwp_correlation.png)

<br><br>

    cwp.plot_coverage(df=dataframe)

    out: 
 
![Coverage plot](https://github.com/cegaltools/cegaltools/blob/master/images/cwp_plot_coverage.png)   

<br><br>


## Creating a Well object using the Cegal Tools

    from cegaltools.wells import Well
    
Create a Well object from las file:

    well_from_las = Well(filename='well_log.las', path='../path to file/')
    
If you have well log data as a dataframe you can create a Well object by passing the dataframe instead of a filename and setting there parameter from_dataframe to True. 

You also have the option of passing a well name, this will be added to the las file header values if you save the Well object to a las file:
                    
    well_from_df = Well(filename=df, from_dataframe=True, dataframe_name='test_well')
    
Attributes on the Well object:

    well_from_las.__dict__
    
    out:
    {'path': '',
     'filename': 'well_log.las',
     'well_object': <lasio.las.LASFile at 0x1902a0941c0>,
     'id': 'ddb49e54ffc6b02e4043025647809060a2dba1c491f59e927ae99dd1'}

Lasio is used to read the las file, by accessing the well_object attribute you can work with and edit the well log file as per the excellent [lasio project and documentation.](https://lasio.readthedocs.io/en/latest/basic-example.html)

<br><br>
   
   

## Built in plots for the Well object


The Cegal Well Plotter functions can be called as methods for the Well object:

    well_from_las.plot_logs()
    
    well_from_las.plot_correlation()
    
    well_from_las.plot_coverage()

<br><br>

## Adding logs and writing Well object as las file

<br>

### Adding a new log

Adding logs to a Well object is done indirectly via lasios insert curve function, however the Well object requires the Well object id (sha244 hash generated for the Well object) to be passed together with new curve. The purpose for this is to assure that logs are written to the correct Well object if called from functions or in loops etc.

The new curve should be passed as a tuple with the Well object id:

> (Well_object.id, new_curve)


    well_from_las.add_to_well((well_from_las.id, new_curve), log_name='this is a new curve')


<br><br>

### Writing Well object to las file

<br>

To save the Well object with the added curve back to a las file we can simply call write_las on the object, while providing a name for the file to be written. The file will be saved in the current directory:

    well_from_las.write_las(filename='our_edited_force_well')