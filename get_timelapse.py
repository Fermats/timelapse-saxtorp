#!/usr/bin/python

#from os import walk
import os
import time
import shutil
import re
import sys
from optparse import OptionParser  # pylint: disable=deprecated-module

intpath = "./interesting/timelapse"
movpath = "./interesting/movement"
srcpath = "./Timelapse/"
dstpath = "./video1/"

# Main method
def main(options, args):
    """Main method."""

    days={}
    image_database = ImageDb()

    print("HEllow orld!")
    for (dirpath, dirnames, filenames) in os.walk(srcpath):
        #    print dirpath
        #    print dirnames
        #    print filenames
        for filename in filenames:
            #print("AAAAAAAAAAAAAAAAA")
            match = re.search('saxtorp(\d+)-(\d+)-(\d+)_(\d+)-(\d+)-(\d+)*', filename)
#real            match = re.search('saxtorp(\d+)-(\d+)-(\d+)_(\d+)-(\d+)-(\d+)*', filename)
            if match:
                (year, month, date, hour, minute, second) = match.groups()
                image_database.add_image(year+month+date, hour, minute, second)

    image_database.print_days()

    image_database.print_images()

    image_database.get_first_image("141017").print_image()

                



#                fromfile = dirpath+"/"+filename
#                topath = dstpath+"20"+year+"-"+month+"-"+date+"/"
                #            print("FILE: "+filename)
#                print("Copy")
#                print("From: "+fromfile)
#                print("To  : "+topath)
                
#                if not os.path.exists(topath):
#                    os.makedirs(topath)
                    #        shutil.move(fromfile, tofile)
#                    shutil.copy2(fromfile, topath)

    return True


class ImageDb(object):
    """Use this class to .

    Args:
        sizes (dict): This dict ...
    """

    def __init__(self):

        self.days = {}

    def add_image(self, date, hour, minute, second, interesting=False):

        if not date in self.days.keys():
            self.days[date] = Day(date)
        self.days[date].add_image(date, hour, minute, second, interesting)

        return True

    def get_day(self, date):
        # Return the requested date object.
        return self.days[date]

    def get_first_day(self):
        days = self.days.keys()
        days.sort()
        return self.days[days[0]]

    def get_last_day(self):
        days = self.days.keys()
        days.sort()
        return self.days[days[len(days)-1]]

    def get_first_image(self, date):
        if self.days[date]:
            return self.days[date].get_first_image()
        
        return None

    def get_nbrofdays(self):
        # Return the number of days of data.
        return len(self.days.keys())

    def print_days(self):
        print("The dates in the DB are:")

        sorted_keys = self.days.keys()
        sorted_keys.sort()
        for key in sorted_keys:
            print(key)
        return True

    def print_images(self):
        print("The dates and images in DB are:")
        sorted_keys = self.days.keys()
        sorted_keys.sort()
        for key in sorted_keys:
            print(key)
            self.days[key].print_images()
        return True

class Day(object):
    """Use this class to .

    Args:
        sizes (dict): This dict ...
    """

    def __init__(self, date):

        self.images = {}
        self.date = date

    def add_image(self, date, hour, minute, second, interesting=False):

        if not hour+minute+second in self.images.keys():
            self.images[hour+minute+second] = Image(date, hour, minute, second, interesting)

        return True

    def get_nbrofimages(self):
        # Return the number of images of a day.
        return len(self.images.keys())

    def get_first_image(self):
        images = self.images.keys()
        images.sort()
        return self.images[images[0]]

    def get_last_image(self):
        images = self.images.keys()
        images.sort()
        return self.images[images[len(images)]-1]

    def get_x_images(self, nbrofimages):
        first = self.get_first_image()
        last  = self.get_last_image()
        t_first = time.strptime(first.date+first.hour+first.minute+first.second, "%y%m%d%H%M%S")
        t_last  = time.strptime(last.date+last.hour+last.minute+last.second, "%y%m%d%H%M%S")
        diff = time.time() # Stopped here
        

    def print_images(self):
        sorted_keys = self.images.keys()
        sorted_keys.sort()
        for key in sorted_keys:
            print("    "+key)

        return True


class Image(object):

    def __init__(self, date, hour, minute, second, interesting=False):

        self.interesting = interesting
        self.date = date
        self.hour = hour
        self.minute = minute
        self.second = second
        self.selected = 0

    def print_image(self):
        print("IMAGE: "+self.date+" "+self.hour+self.minute+self.second)
        return True




def parse_args():
    """Function that does command line argument and options parsing"""
    parser = OptionParser()
    parser.usage += " <config-files>"

    parser.add_option(
        '-o', '--fjweo', dest='database',
        help="Database "
             "to use.")
    parser.add_option(
        '-l', '--lebsize', dest='lebsize', action='store_true',
        default=False,
        help="Use this if you want to set the size option "
             "in nbr of lebs and not in bytes. Only applicable for UBI.")

    (options, args) = parser.parse_args()

    return options, args


if __name__ == '__main__':
    # pylint: disable=invalid-name
    if sys.version_info[:2] <= (2, 7):
        get_input = raw_input
    else:
        get_input = input

    (OPTIONS, ARGS) = parse_args()
    main(OPTIONS, ARGS)
