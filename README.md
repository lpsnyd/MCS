# MCS
## Esri Maritime Chart Server Update Script

There are two scripts to update your Esri Maritime Chart Server (MCS) Extension for
ArcGIS Server. 
NOAA's Office of Coast Survey (OCS) deploys ENC S-57 excahnge sets
on a weekly schedule. This batch script will keep the MCS service and viewer up-to-date
and synced with the latest available ENCs through OCS' webiste -
http://www.charts.noaa.gov/ENCs/ENCs.shtml.
United State Army Corps of Engineers (USACE) deploys inland ENCs (IENC) on a weekly
schedule. The python script will keep the MCS service and viewer up-to-date
and synced with the latest available ENCs through the USACE website.

## Getting Started
Clone this repository to the directory folder you will plan to run the script for updating
your MCS from, i.e. c:\scripts

## Prerequisites
For batch file:
1. You must have ArcGIS Server and ArcGIS for Maritime: Server installed. 
2. wget.exe
wget can be replaced with some other tool to download internet resources
3. WZUNIZIP (WinZip Command Line Support Add-On)
WinZip Command Line Support Add-On can be replaced with 7zip tools
For python script:
Must have Python 2.7 installed - has not been tested with Python 3.4

## Install and Configuration
Set the following variables to your local environment.
sd (script directory) - This is the directory the .bat file is within 
td (temp directory) - This is the directory where the ENCs are downloaded to
ENCROOT - Variable assigning ENC_ROOT
zipUrl - Sets the zip download from NOAA's external chart download site
logfile - Sets the logfile path
serverdirectory - Set this to your local directory on ArcGIS Server that
points to your MCS datasets folder. This can be ommitted or used depending
if you need to deploy the script to multiple servers that have different
"datasets" paths.


## Deployment
Set MCS_ENC_autoupdate.bat file as a scheduled task through Windows Task Scheduler to run
on whatever schedule you need. 
Set get_ienc.py file as a scheduled task through Windows Task Scheduler to run on whatever
schedule you need.

## Authors
Leland Snyder
