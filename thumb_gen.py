#!/usr/bin/python
"""
Make thumbnails
read from argv/argc source path, destination path, thumbsize.
"""

import os
import Image
import sys
import glob



def make_thumb(img, size):
	print 'SIZE', size
	img.thumbnail(size, Image.ANTIALIAS)
	return img

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

	#get all files of source path
	files = getFileList(srcURL)
	thumbs = processFiles(files, int(width), int(height))
	saveThumbs(dstURL, thumbs)
	#Get Image Files
	#Get thumbnail
	#Save Thumb to destination with extension at beginning

main(sys.argv)
