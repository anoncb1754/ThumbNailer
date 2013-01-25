#!/usr/bin/python

"""
This python script creates square thumbnails from JPG and PNG images.


Prerequesites:
    * Python 2.7
    * PIL

Usage:
    Start script by 
    * providing the source folder containing the images as first argument
    * the target folder that will contain the thumbnails as second argument
    * the size of the square thumbnail as last argument.
    * e.g. python thumb_gen.py /sourcefolder /targetfolder 100
    This will take all JPG and PNG files from the sourcefolder and saves
    all thumbnails as square with width and height of 100 px to the specified
    targetfolder.
"""



import os
import Image
import sys
import glob

__author__ = "Carl Bednorz"
__version__ = "1.0"
__email__ = "carl.bednorz(at)gmail.com"
__license__ = "GPL 3.0"


def boxParamsCenter(width, height):
    """
    Calculate the box parameters for cropping the center of an image based
    on the image width and image height
    """
    if isLandscape(width, height):
        upper_x = int((width/2) - (height/2))
        upper_y = 0
        lower_x = int((width/2) + (height/2))
        lower_y = height
        return upper_x, upper_y, lower_x, lower_y
    else:
        upper_x = 0
        upper_y = int((height/2) - (width/2))
        lower_x = width
        lower_y = int((height/2) + (width/2))
        return upper_x, upper_y, lower_x, lower_y

def isLandscape(width, height):
    """
    Takes the image width and height and returns if the image is in landscape
    or portrait mode.
    """
    if width >= height:
        return True
    else:
        return False

def cropit(img, size):
    """
    Performs the cropping of the input image to generate a square thumbnail.
    It calculates the box parameters required by the PIL cropping method, crops
    the input image and returns the cropped square.
    """
    img_width, img_height = size
    upper_x, upper_y, lower_x, lower_y = boxParamsCenter(img.size[0], img.size[1])
    box = (upper_x, upper_y, lower_x, lower_y)
    region = img.crop(box)
    return region

def folderExists(path):
    if(os.path.exists(path) == False):
        sys.exit('Source or Destination folder does not exist! Please try again!')
    else:
        return

def makeThumb(img, size):
    """
    The input image is cropped and then resized by PILs thumbnail method.
    """
    cropped_img = cropit(img, size)
    cropped_img.thumbnail(size, Image.ANTIALIAS)
    return cropped_img

def checkSysArgv(args):
	if len(args) != 4:
		sys.exit('Wrong command line arguments! I accept the following format: [path to source folder] [path to destination folder] [thumb size]')

def getFileList(srcURL):
        '''
        Get all files of type png or tiff. Store the paths in a list.
        The list is than returned.
        @return: filelist - a list that stores all the png or tiff files of the source path
        '''
        filelist = []
        for root, dirs, files in os.walk(srcURL):
            for singlefile in files:
                if singlefile.endswith('.PNG') or singlefile.endswith('.png') or singlefile.endswith('.tiff') or singlefile.endswith('.TIFF') or singlefile.endswith('.jpg') or singlefile.endswith('.jpeg'):
                    filelist.append(root + '/' + singlefile) # raus genommen '/' +
                    #put single file into list
        return filelist

def checkTargetSize(target_size):
    print 'CHECK TARGET SIZE', target_size
    if int(target_size) <= 0:
        sys.exit("Invalid target size for thumbnails! Please try again!")

def processFiles(files, width, height):
        """
        Performs the creation of thumbs in a batch like manner.
        """
	thumbs = []
	size = width, height
        print "Hi there! I'm going to start the thumbnailing process..."
	for file in files:
		img = Image.open(file)
                thumbs.append(makeThumb(img, size=size))
                print "Thumbnail has been created..."
	return thumbs

def saveThumbs(dstURL, thumbs):
	"""
        Performs batch like saving of the created thumbnails.
        """
        i = 0
	for thumb in thumbs:
                try:
		    thumb.save(dstURL + '/' + 'thumb_' + str(i) + '.png', "PNG")
		    i = i+1
                    print 'Thumbnail has been saved successfully...'
                except IOError, Err:
                    print 'Cannot save file!'


def main(args):
        """
        Main function for thumbnail creation.
        First arguments are processed and then thumbnails are created from the 
        input image where the thumbnail represents a cropped square from the
        center of the input image.
        """
	checkSysArgv(sys.argv)
	srcURL = args[1]
	dstURL = args[2]
        thumb_target_size = args[3]
        checkTargetSize(thumb_target_size)
	folderExists(srcURL)
	folderExists(dstURL)
	files = getFileList(srcURL)
	thumbs = processFiles(files, int(thumb_target_size), int(thumb_target_size))
	saveThumbs(dstURL, thumbs)
        print 'All images have been thumbnailed successfully! Thx and Good Bye!'
main(sys.argv)
