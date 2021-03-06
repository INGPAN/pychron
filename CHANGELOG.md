CHANGELOG
============
2.0.5
------------------
* added switching between blank histories
* added BlankDiffView
* started Workspace
* added switching between sample_view(Jake) and query_view(Al) in browser
* added "Time View" to sample table context menu. Use to display list of analyses based on
    date ranges defined by the selected labnumbers
* added project, irradiation enabled toggles
* if high or low post only filters defined load the analysis table with the date range
* added detector ic view
* added comment template
* use notebook for scan manager graphs
* updated Procedures. don't open multiple extraction line canvases
* added Find References context menu action
* added user login
* added ability to archive loads
* added identifier (Labnumber) top level filter
* added Filter/Results focus switching
* added group emailing
* gitified pyscripts
* added frequency template
* added LabBook Plugin
* added open boxes to spectrum
* added uncorrected ratios to Series
* unified conditionals editing
* added database version checking
* updated conditionals. can do and/or with multiple variables e.g Ar40>10 and age<10.0
* added wake command to ExtractionLinePyScript. jitters mouse to wake from screen saver
* added Edit Initialiation action and view
* added Labeling to LabBook
* changed Pychrondata to Pychron. 
* added ability to set Pychron root directory in the preferences. Uses ~/Pychron as default
* moved use_login,multi_user from initializtion file to preferences.

2.0.4
------------------
* implemented "overlap" concept for automated runs
* select existing users from db when writing an experiment
* record diode output (heat_power) and response (temp) for each analysis
* when diode enabled scan pyrometer and display colormapped indicator for temperature
* measure baselines between peak hops. can explicitly define a peak hop as a baseline.
* added context menu actions to Experiment Editor. Move to End, Move to Start, Move to ...
* APIS support
* updated Experiment estimated duration. 
* added Visual ExtractionLine Script programmer
* added Peak hop editor
* added context menu actions to UnknownsPane(unselect, group selected, clear grouping) and AnalysisTable(unselect, replace, append)
* added Open Additional Window action. use to open multiple windows of the same task type e.i two recall windows
* added Split Editor action
* updated grouping of unknowns. added auto_group toggle to UnknownsPane
* added date querying to top-level filtering in Browser
* updated frequency run addition
* added trough and rubberband patterns. modified stage map to accommodate rubberband pattern
* added graphical filtering to Browser
* added data reduction tagging
* added ability to configure recall view
* started permutator. use to generate all permutations of a dataset
* started summary views accessible for recall task
* added use_cdd_warming to experiment queue
* added preset decay constants for easy switching
* added default snapshot name (RunID_Pos) when used from pyscript, e.g. 12345-01A_3
* added note, last_modified to irrad_ProductionTable
* updated editing default_fits
* added snapshot view to recall
* added fontsize control to recall
* added task switching
* added time view to browser
* added ability to add event markers to spectrometer scan graph
* added snapshot to spectrometer scan
* added bgcolor control for experiment editor
* optimized plotpanel
* added "window" to AutomatedRunCondition. use to take a mean or std of "window" points
* added more options for AutomatedRunConditions
* added Queue/Default Conditionals
* updated user notification
* added procedures concept e.g. QuickAir
* added ImportIrradiationHolderAction
* added end_after and skip context menu actions