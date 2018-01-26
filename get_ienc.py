"""
Author: Leland Snyder
Updated 1/26/2018
This script will update your Esri Maritime Chart Server (MCS) Extension for ArcGIS Server. United States Army Corps of
Engineers (USACE) deploys inland ENC (IENC) excahnge sets on a weekly schedule. This script will keep the MCS service and viewer up-to-date and synced with the latest available ENCs.
"""

import distutils.core
import fnmatch
import os
from shutil import rmtree
import sys
import traceback
import urllib
from zipfile import ZipFile
import socket
from datetime import datetime

dt = str(datetime.now()).replace(" ","_").replace(":","~").partition(".")[0]
print os.getcwd()
os.chdir(os.path.dirname(os.path.realpath(__file__)))
print os.getcwd()
## If using MCS on different servers, use HOSTNAME to set different directories.
if socket.gethostname() == 'HOSTNAME': ## replace HOSTNAME with machine name
    server = r"PATH_TO_ARCGISSERVER\directories\maritimeserver\ENC_IENC\datasets\IENC" ## replace PATH and datasets folder
    cwd = os.getcwd() + os.path.sep + "IENC_temp"
elif socket.gethostname() == 'HOSTNAME2': ## replace HOSTNAME2 with machine name
    server = r"PATH_TO_ARCGISSERVER\directories\maritimeserver\ENC_IENC\datasets\IENC" ## replace PATH and datasets folder
    cwd = os.getcwd() + os.path.sep + "IENC_temp"
else:
    server = r"PATH_TO_ARCGISSERVER\directories\maritimeserver\ENC_IENC\datasets\IENC"
    cwd = r"DIRECTORY_FOR_TEMP\IENC_temp" ## replace DIRECTORY_FOR_TEMP with temp directory

print socket.gethostname()
print server
print cwd

## Optional variables for IENC download.
IENCUrl = 'http://ec2-54-235-76-27.compute-1.amazonaws.com/ienc/products/files/u37/ienc_s57/IENC_S57.zip'
swPassUrl = 'http://ec2-54-235-76-27.compute-1.amazonaws.com/ienc/products/files/SWPass/3UASW000.zip'
buoyUrl = 'http://ec2-54-235-76-27.compute-1.amazonaws.com/ienc/products/files/buoys/3UABUOYS.zip'

if not os.path.isdir(cwd):
    os.mkdir(cwd)

# Checks to see whether or not the IENC datasets folder exists, and if so, deletes it
# Not sure whether distutils.dir_util.copy_tree(encDatasets, server) line 68 mirrors or overwrites all.
if os.path.isdir(server):
    rmtree(server)

start = datetime.now()

try:
    Downloads = cwd + os.sep + "Downloads"

    if not os.path.exists(Downloads):
        os.mkdir(Downloads)

    # Create a name for the file to be downloaded
    name = IENCUrl.rsplit("/", 1)[-1]

    # Set the full path for the downloaded file
    filename = os.path.join(Downloads, name)

    print "Downloading %s to %s" % (IENCUrl, filename)
    urllib.urlretrieve(IENCUrl, filename)

    encOut = cwd + os.sep + "Parent" + os.sep + (os.path.basename(filename)).replace(".zip","")
    encDatasets = cwd + os.sep + "Datasets"
    if not os.path.exists(encDatasets):
        os.mkdir(encDatasets)
	
    print "\tDeleting previous %s directory structure..." % (encDatasets)
    for f in os.listdir(encDatasets):
        fPath = os.path.join(encDatasets,f)
        if os.path.isfile(fPath):
            os.unlink(fPath)
        elif os.path.isdir(fPath):
            rmtree(fPath)
            print "\t\tDeleting directory structure %s " % (fPath)
    print "\n\tExtracting to %s" % (encOut)

    zip_file = ZipFile(filename)

    ZipFile.extractall(zip_file, encOut)

    pattern = '*.zip'
    for root, dirs, files in os.walk(encOut):
        for f_name in fnmatch.filter(files, pattern):
            outPath = os.path.join(encDatasets, os.path.splitext(f_name)[0])
            print "\t\tExtracting %s" % (os.path.join(encDatasets, f_name))
            ZipFile(os.path.join(root, f_name)).extractall(outPath)

    zip_file.close()

    distutils.dir_util.copy_tree(encDatasets, server)
    print "\tCopying %s to %s" % (encDatasets, server)

    end = datetime.now()
    duration = end - start

    print "Completed successfully in %s minutes" % str(duration.total_seconds()/60)

except:
##  Errors = traceError()
##  print Errors
    traceback.print_exc()
    end = datetime.now()
    duration = end - start
    print "Failed in %s minutes." % str(duration.total_seconds()/60)
