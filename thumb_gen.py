#!/usr/bin/python
"""
Make thumbnails
read from argv/argc source path, destination path, thumbsize.

Cutting, Pasting and Merging Images

The Image class contains methods allowing you to manipulate regions within an image. To extract a sub-rectangle from an image, use the crop method.

Copying a subrectangle from an image
    box = (100, 100, 400, 400)
    region = im.crop(box)
The region is defined by a 4-tuple, where coordinates are (left, upper, right, lower). The Python Imaging Library uses a coordinate system with (0, 0) in the upper left corner. Also note that coordinates refer to positions between the pixels, so the region in the above example is exactly 300x300 pixels.

@todo:
    Advanced cropping: Crop the center of the image in relation to the whole image.
    So get the center first, then do the cropping!
"""

import os
import Image
import sys
import glob




def box_params_center(width, height):
    """
    Calculate the box parameters for cropping the center of an image based
    on the image width and image height
    
    """
    #center_x = width/2
    #center_y = height/2
    if is_landscape(width, height):
        """Get the center of the image and start cropping at upper left
        and lower right coordinate whereas the length of the rectangular
        has to be the same"""
        print 'Image is landscape'
        upper_x = int((width/2) - (height/2))
        upper_y = 0
        lower_x = int((width/2) + (height/2))
        lower_y = height
        print 'Coordinates center cropped box', upper_x, upper_y, lower_x, lower_y
        return upper_x, upper_y, lower_x, lower_y
    else:
        print 'Image is portrait'
        upper_x = 0
        upper_y = int((height/2) - (width/2))
        lower_x = width
        lower_y = int((height/2) + (width/2))
        return upper_x, upper_y, lower_x, lower_y

def is_landscape(width, height):
    
    if width >= height:
        return True
    else:
        return False

def box_params_upper_left(width):
    """
    First crop image rectangular in relation to width of input Image
    at the upper left corner. generate box parameters from it and then
    resize the image with thumbnail or even resize!
    """
    print 'The Width is', width
    upper_x = 0
    upper_y = 0
    lower_x = width/3
    lower_y = width/3
    return upper_x, upper_y, lower_x, lower_y

def calc_box_params_up_left_corner(targetSize):
    """
    Easiest Attempt, perform cropping at 0,0
    """
    upper_x = 0
    upper_y = 0
    lower_x = targetSize[0]
    lower_y = targetSize[1]
    print 'Target Size', targetSize, lower_x, lower_y
    
    

    

    


def calculate_box_params(width, height, thumb_size):
    """
    Problem is somewhere here:
    cropped thumb is always the half of the sys.argv width and height
    """
    center_x = width/2
    center_y = height/2
    print 'Center is: ', center_x, center_y
    print 'THUMBSIZE:', thumb_size
    upper_y = center_y - int(thumb_size[0]/4)
    upper_x = center_x - int(thumb_size[1]/4)
    print 'START CROP COORDINATES', upper_y, upper_x
    lower_y = center_y + int(thumb_size[0]/4)
    lower_x = center_x + int(thumb_size[1]/4)
    print 'END CROP COORDINATES', lower_y, lower_x
    return upper_x, upper_y, lower_x, lower_y

def cropit(img, size):
    #box = (0, 0, 100, 100)
    #region = img.crop(box)
    #print 'The cropped region is:', region
    #img_width = img.size[0]
    #img_height = img.size[1]
    img_width, img_height = size
    print 'Start crop sizes', size 
    #upper_x, upper_y, lower_x, lower_y = box_params_upper_left(img.size[0])
    upper_x, upper_y, lower_x, lower_y = box_params_center(img.size[0], img.size[1])
    box = (upper_x, upper_y, lower_x, lower_y)
    region = img.crop(box)
    print 'Region after cropping', region.size
    return region

def folder_exists(path):
    if(os.path.exists(path) == False):
        sys.exit('Source or Destination folder does not exist! Please try again!')
    else:
        return

def make_thumb(img, size):
	print 'SIZE', size
        new_size = (size, size) 
        #img.thumbnail(size, Image.ANTIALIAS)
        thumb_size = img.size
        print 'THUMB SIZE', thumb_size
	cropped_img = cropit(img, size)
        cropped_img.thumbnail(size, Image.ANTIALIAS)
        #cropped_img = cropit(img, size)
	return cropped_img

def check_sys_argv(args):
	if len(args) != 5:
		sys.exit('Wrong command line arguments! I accept the following format: [path to source folder] [path to destination folder] [width] [height]')

def get_sys_argvs(args):
	for item in sys.argv:
		print item

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

def processFiles(files, width, height):
	thumbs = []
	size = width, height
	for file in files:
		print 'AIGHT', file
		img = Image.open(file)
                print 'Start cropping'
		#cropped_img = cropit(img)
                #thumbs.append(cropped_img)
                thumbs.append(make_thumb(img, size=size))
	return thumbs

def saveThumbs(dstURL, thumbs):
	i = 0
	for thumb in thumbs:
		thumb.save(dstURL + '/' + 'thumb_' + str(i) + '.png', "PNG")
		i = i+1

def main(args):
	check_sys_argv(sys.argv)
	get_sys_argvs(sys.argv)
	
	srcURL = args[1]
	dstURL = args[2]
	width = args[3]
	height = args[4]


	#Check if paths are correct
	folder_exists(srcURL)
	folder_exists(dstURL)
	#get all files of source path
	files = getFileList(srcURL)
	thumbs = processFiles(files, int(width), int(height))
	saveThumbs(dstURL, thumbs)
	#Get Image Files
	#Get thumbnail
	#Save Thumb to destination with extension at beginning

main(sys.argv)
