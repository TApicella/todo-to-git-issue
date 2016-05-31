""" A script for creating github issues automatically from TODO comments """

import requests, os, shutil, argparse


def warn(msg, strict=False):
	""" Prints out warnings or throws an exception if --strict is set """
	if strict:
		raise Exception(msg)
	else:
		print msm

def setupBackupFolder():
	""" If a backup folder for this script doesn't exist, create it and add it to .gitignore """
	if not os.path.isdir("./todo-to-git-backup"):
		os.makedirs("./todo-to-git-backup")
		with open("./.gitignore", 'ab') as g:
			g.write("./todo-to-git-backup")

def backupFile(fpath, fname):
	""" Backup the file being parsed """
	shutil.copyfile(fpath, "./todo-to-git-backup/%s" % fname)

def validateArgs(args):
	""" Confirm that the arguments are valid """

	#Make sure --recursive is used for directories and all paths valid
	has_directories = False
	for f in args.filepaths:
		if not os.path.exists():
			raise Exception("File/Directory %s not found!")
		if os.path.isdir(f):
			has_directories = True
	if has_directories and not args.recursive:
		raise Exception("You must use the flag --recursive if you include directories in your list of files")
	if not has_directories and args.recursive:
		message = "WARNING: Recursive specified, but no directories specified"
		warn(message, args.strict)

def parseFile(filepath, args):
	""" Generate issues for a given file """

	if os.path.isdir(filepath):
		for path, dirs, files in os.walk(filepath):
		    for f in files:
		        parseFile(path+"/"+f, args)
	else:
		splitpath = filepath.split("/")
		filename = splitpath[-1]
		backupFile(filepath, filename)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A script to automatically create github issues from TODO comments", epilog="(ADD EXAMPLE)")
    parser.add_argument('-r', '--recursive', action='store_true', default=False, help='You must use --recursive if you want to iterate over a directory')
    parser.add_argument('-s', '--strict', action='store_true', default=False, help="Use --strict to force a rollback and exit on warnings as well as errors")
    parser.add_argument('filepaths', nargs='+', help='One or more files or directories to parse for TODO statements')

#~/Documents/Python/todo-to-git-issue/.git $ less config