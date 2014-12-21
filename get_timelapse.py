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
#srcpath = "../Timelapse/"
srcpath = "./input/"
dstpath = "./video1/"

# Main method
def main(options, args):
    """Main method."""

    days={}
    image_database = ImageDb()

    print("HEllow orld!")
    for (dirpath, dirnames, filenames) in os.walk(srcpath):
        for filename in filenames:
            match = re.search('saxtorp(\d+)-(\d+)-(\d+)_(\d+)-(\d+)-(\d+)*', filename)
            if match:
                (year, month, date, hour, minute, second) = match.groups()
                image_time = time.strptime(year+month+date+hour+minute+second, "%y%m%d%H%M%S")
                image_database.add_image(image_time)

#    image_database.print_days()

#    image_database.print_images()

#    img = image_database.get_first_image("141017")
#    if img:
#        img.print_image()

                



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

    def add_image(self, image_time, interesting=False):
        date = time.strftime("%y%m%d", image_time)
        
        if not date in self.days.keys():
            self.days[date] = Day(date)
        self.days[date].add_image(image_time, interesting)

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
        if date in self.days.keys():
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

    def add_image(self, image_time, interesting=False):
        clock = time.strftime("%H%M%S", image_time)

        if not clock in self.images.keys():
            self.images[clock] = Image(image_time, interesting)
        else:
            self.images[clock].print_image()

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
        image_list = []
        first = self.get_first_image()
        last  = self.get_last_image()
        
        diff = (time.mktime(last) - time.mktime(first)) / (nbrofimages+1)
        for index in range(nbrofimages):
            timetofind = time.mktime(first) + (index+1)*diff
            
            image = self.get_image_by_time(time.localtime(timetofind))
            image_list.append(image)

        return image_list

    def get_image_by_time(self, image_time):
        image_keys = self.images.keys()
        image_keys.sort()
        for key in image_keys:
            return None
        

    def print_images(self):
        sorted_keys = self.images.keys()
        sorted_keys.sort()
        for key in sorted_keys:
            print("    "+key)

        return True


class Image(object):

    def __init__(self, image_time, interesting=False):

        self.interesting = interesting
        self.image_time = image_time
        self.selected = 0

    def print_image(self):
        print("IMAGE: "+time.strftime("%Y-%m-%d %H:%M:%S", self.image_time))
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
