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
srcpath = "../Timelapse/"
#srcpath = "./input/"
dstpath = "./video1/"

# Main method
def main(options, args):
    """Main method."""

    days={}
    image_database = ImageDb()

    print("HEllow orld!")

    hello = create_database_from_files(srcpath, 'saxtorp(\d+)-(\d+)-(\d+)_(\d+)-(\d+)-(\d+)-.*')


#    day1 = hello.get_day("140607")

#    timelapse_database = day1.get_x_images(100)

    timelapse_database = hello.get_x_images_per_day(100)

#    timelapse_database.print_images()
#    day1.print_images()



#    hello.print_images()


#    for (dirpath, dirnames, filenames) in os.walk(srcpath):
#        for filename in filenames:
#            match = re.search('saxtorp(\d+)-(\d+)-(\d+)_(\d+)-(\d+)-(\d+)*', filename)
#            if match:
#                (year, month, date, hour, minute, second) = match.groups()
#                image_time = time.strptime(year+month+date+hour+minute+second, "%y%m%d%H%M%S")
#                image_database.add_image(image_time)

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

def create_database_from_files(srcpath, file_pattern):
    image_database = ImageDb()
    for (dirpath, dirnames, filenames) in os.walk(srcpath):
        for filename in filenames:
            match = re.search(file_pattern, filename)
            if match:
                (year, month, date, hour, minute, second) = match.groups()
                image_time = time.strptime(year+month+date+hour+minute+second, "%y%m%d%H%M%S")
                image_database.add_image(image_time)
    return image_database


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

    def get_last_image(self, date):
        if date in self.days.keys():
            return self.days[date].get_last_image()
        return None

    def get_x_images_per_day(self, nbrofimages):
        new_db = ImageDb()
        for key in self.days.keys():
            day = self.days[key].get_x_images(nbrofimages)
            new_db.days[key] = day
        return new_db
            

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
#            print(key)
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
            print("Duplicate:")
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
        return self.images[images[len(images)-1]]

    def get_x_images(self, nbrofimages):
        if len(self.images.keys()) <= nbrofimages:
#            print("Length to  : "+str(len(self.images.keys()))+"    date: "+self.date)
            return self
    
        new_day = Day(self.date)
        first = self.get_first_image()
        last  = self.get_last_image()
        
        diff = (time.mktime(last.image_time) - time.mktime(first.image_time)) / (nbrofimages+1)
        timetofind = time.mktime(first.image_time) + diff
        image_keys = self.images.keys()
        image_keys.sort()
        prev_key = image_keys[0]
        for key in image_keys:
            prev_time = time.mktime(self.images[prev_key].image_time)
            curr_time = time.mktime(self.images[key].image_time)
            if curr_time > timetofind:
                if abs(curr_time-timetofind) < abs(prev_time-timetofind):
                    new_day.add_image(self.images[key].image_time)
                else:
                    new_day.add_image(self.images[prev_key].image_time)
                    
                timetofind += diff
                if len(new_day.images.keys()) >= nbrofimages:
                    break
        
#        print("Length from: "+str(len(self.images.keys())))
#        print("Length to  : "+str(len(new_day.images.keys())))
        return new_day

    def get_image_by_time(self, image_time):
        image_keys = self.images.keys()
        image_keys.sort()
        for key in image_keys:
            return None
        

    def print_images(self):
        sorted_keys = self.images.keys()
        sorted_keys.sort()
        print(self.date)
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
