rem Author: Leland Snyder
rem Date Updated: 8/4/2015
rem This script is used to update the MCS(ENCOnline) services on MCS 4.1.11 installs
rem with configuration set to autoupdate=true. This elimated having to stop and start
rem the service to refresh senc files.

rem #Setting local variables
set sd="c:\scripts\"
set td="c:\temp\MCS_temp\"
set ENCROOT="ENC_ROOT"
set zipUrl="http://www.charts.noaa.gov/ENCs/All_ENCs.zip"

rem Set date add to logfile name
FOR /f "tokens=2-4 delims=/ " %%a IN ("%DATE%") DO (SET logfiledate=log-%%a-%%b-%%c)

set "logfile=%sd%\%logfiledate%.log"
Echo %logfile%
rem Pause
rem append PATH variable to include C:\Program Files\WinZip for the WinZip Command Line Support
rem Add-On as well as scripts directory containing wget.exe 
PATH=%PATH%;C:\Program Files\WinZip;C:\scripts

rem check computername and set variable for proper server directory

rem ocs-vs-appt7
IF %COMPUTERNAME% == YOUR_SERVER_HOSTNAME (set serverdirectory="PATH_TO_ARCGIS_SERVER_DIRECTORIES\MARITIMECHARTSERVER\datasets\ENC_ROOT")

rem Create temporary directory
md %td%
cd %td%

Echo %filedate% %time% - Script Begin...>>%logfile%
Echo(>>%logfile%
Echo Computername - %COMPUTERNAME%>>%logfile%
Echo Destination directory set to: %serverdirectory%>>%logfile%
Echo(>>%logfile%

rem Download zip containing ENCs
Echo Downloading ENC zip...>>%sd%\%logfiledate%.log
Echo(>>%logfile%
wget -v -N %zipUrl% -a C:\scripts\%logfiledate%.log 
Echo(>>%logfile%
Echo Download Complete...>>%logfile%
Echo(>>%logfile%

rem Delete previously unpackaged ENC_ROOT
rd /S /Q %td%%ENCROOT% 

rem Unpackage ENC zip
Echo Unzipping...>>%logfile%
Echo(>>%logfile%
wzunzip -d *.zip %td% >>%logfile%
Echo(>>%logfile%
Echo Unzip Complete...>>%logfile%
Echo(>>%logfile%

rem Robocopy ENC_ROOT to MCS directory
Echo Copying ENC_ROOT to server...>>%logfile%
Echo(>>%logfile%
ROBOCOPY "c:\temp\MCS_temp\ENC_ROOT" "%serverdirectory%" /MIR /ns /nc /nfl /ndl /np /log+:"C:\scripts\%logfiledate%.log"

Echo Autoupdating service...>>%logfile%
Echo(>>%logfile%

Echo %time% - Script Complete>>%logfile%
Echo -------------------------------->>%logfile%
Echo(>>%logfile%


