# Airflow Project on GCP

## USE CASE

This data has been gathered at two solar power plants in India over a 34 day period. It has two pairs of files - each pair has one power generation dataset and one sensor readings dataset. The power generation datasets are gathered at the inverter level - each inverter has multiple lines of solar panels attached to it. The sensor data is gathered at a plant level - single array of sensors optimally placed at the plant.

There are a few areas of concern at the solar power plant -

*  Can we predict the power generation for next couple of days? - this allows for better grid management
*  Can we identify the need for panel cleaning/maintenance?
*  Can we identify faulty or suboptimally performing equipment?

# DATA PIPEPLINE OBJECTIVE

*  Ensure the analyst gets the refreshed data from the Data Grids as they fresh.
*  Ensures the analyst are able to query data from the BigQuery as opposed to using csv.

# Airflow Version and dependencies

*  apt-get update && apt-get install -y python-setuptools python-pip python-dev libffi-dev libssl-dev zip wget
*  pip install apache-airflow[gcp, statsd,sentry]==1.10.10

# DAG ARCHITECTURE
* The data from the Grid are landing in CSV format in the Google Storage.
* The files are then pushed as listed objects in Landing Buckets.
* Then load the files into BigQuery.
* Create tables with the latest data.
* Ones the data is aged, it is moved into Backup bucket.

## Login into Airflow:

*  User : admin
*  Pwd  : admin


# Step 1: DAG Web Interface
<p align="center">
  <img src="https://github.com/BundeAmos/Veriff/blob/master/Screenshot%20from%202021-08-31%2016-23-36.png" width=2000 px title="DAG Page">
  <
</p>

  
  
  
  # Step 2: DAG Web Interface[Tree View]
<p align="center">
  <img src="https://github.com/BundeAmos/Veriff/blob/master/Screenshot%20from%202021-08-31%2016-43-49.png" width=2000 px title="DAG Page">
  <
</p>
  
  
  
  # Step 3: DAG Web Interface[Graph View]
<p align="center">
  <img src="https://github.com/BundeAmos/Veriff/blob/master/Screenshot%20from%202021-08-31%2016-48-17.png" width=2000 px title="DAG Page">
  <
</p>
  
  
    
  # Step 4: DAG Web Interface[Calendar View]
<p align="center">
  <img src="https://github.com/BundeAmos/Veriff/blob/master/Screenshot%20from%202021-08-31%2016-50-32.png" width=2000 px title="DAG Page">
  <
</p>

  
  
  # CHALLENGES FACED
  
  *  Infrastructral cost especially in the AWS, given that I had exhausted the free trial; inhibited me from a real POC.
  *  The data is more static, I neede data that is in motion to replicate the renewed data or refresh data.
  *  Even in the Google Cloud Compute the VMs proved costly in installing a production equivalent Airflow setup. 
  *  The apache airflow dependency really deprecae in case of mismatch, and as search they need lot of observation.
  
