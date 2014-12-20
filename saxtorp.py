#!/usr/bin/python

#from os import walk
import os
import shutil
import re

month_text = [
    '', 
    'januari', 
    'februari', 
    'mars', 
    'april', 
    'maj', 
    'juni', 
    'juli', 
    'augusti', 
    'september', 
    'oktober', 
    'november', 
    'december'
    ]

#months = ["jan","feb"

#srcpath = "/home/mats/haxing/file_parser/input/"
#dstpath = "/home/mats/haxing/file_parser/output/"
srcpath = "./alla_bilder/"
dstpath = "./Timelapse/"

for (dirpath, dirnames, filenames) in os.walk(srcpath):
#    print dirpath
#    print dirnames
#    print filenames
    for filename in filenames:
#        print("AAAAAAAAAAAAAAAAA")
        match = re.search('saxtorp(\d+)-(\d+)-(\d+)_(\d+)-(\d+)-(\d+)*', filename)
        if match:
            (year, month, date, hour, minute, second) = match.groups()
            fromfile = dirpath+"/"+filename
            topath = dstpath+"20"+year+"-"+month+"-"+date+"/"
            #            print("FILE: "+filename)
            print("Copy")
            print("From: "+fromfile)
            print("To  : "+topath)
        
            if not os.path.exists(topath):
                os.makedirs(topath)
            shutil.move(fromfile, topath)
            #shutil.copy2(fromfile, topath)


