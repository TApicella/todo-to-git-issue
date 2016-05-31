""" A script for creating github issues automatically from TODO comments """

import requests, os, shutil, argparse
from comment_strings import comment_strings as cs

def warn(msg, strict=False, fparams=None):
	""" Prints out warnings or throws an exception if --strict is set """
	if strict:
		if fparams:
			rollback(fparams)
		raise Exception(msg)
	else:
		print msg

def setupBackupFolder():
	""" If a backup folder for this script doesn't exist, create it and add it to .gitignore """
	if not os.path.isdir("./todo-to-git-backup"):
		os.makedirs("./todo-to-git-backup")
		with open("./.gitignore", 'ab') as g:
			g.write("./todo-to-git-backup")

def backupFile(fparams):
	""" Backup the file being parsed """
	print "Backing up %s" % fparams["fname"]
	shutil.copyfile(fparams["fpath"], fparams["bpath"])

def rollback(fparams, msg=""):
	""" Copy the backup file back to the original directory """
	print "Rolling back changes. %s" % msg
	shutil.copyfile(fparams["bpath"], fparams["fpath"])


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

def determineComment(ext):
	"""" Try to determine the line comment format """
	if ext in cs:
		return cs[ext]
	else:
		raise Exception("Comment string could not be determined. Please manually specify using the --comment flag")


def parseFile(filepath, args):
	""" Generate issues for a given file """

	if os.path.isdir(filepath):
		for path, dirs, files in os.walk(filepath):
		    for f in files:
		        parseFile(path+"/"+f, args)
	else:
		splitpath = filepath.split("/")

		FILENAME = splitpath[-1]
		FILEPATH = filepath
		BACKUP_PATH = "./todo-to-git-backup/%s" % FILENAME
		EXTENSION = FILENAME.split('.')[-1]

		fileparams = {"fname":FILENAME, "fpath":FILEPATH, "bpath":BACKUP_PATH, 'ext':EXTENSION}
		backupFile(fileparams)

		comment_string = args.comment

		if not comment_string:
			comment_string = determineComment(EXTENSION)

		with open(FILEPATH, 'rb') as original:
			lines = original.readlines()

		with open(FILEPATH, 'wb') as new:
			for line in lines:
				if line.strip().startswith(comment_string):
					print "Found comment"
					if line.strip().lower().startswith(comment_string+"todo") or line.strip().lower().startswith(comment_string+" todo"):
						print "also found TODO: %s" % line



if __name__ == '__main__':
	#TODO: stuff yo
    parser = argparse.ArgumentParser(description="A script to automatically create github issues from TODO comments", epilog="(ADD EXAMPLE)")
    parser.add_argument('-r', '--recursive', action='store_true', default=False, help='You must use --recursive if you want to iterate over a directory')
    parser.add_argument('-s', '--strict', action='store_true', default=False, help="Use --strict to force a rollback and exit on warnings as well as errors")
    parser.add_argument('-c', '--comment', default=None, help="Manually define the comment character(s)")
    parser.add_argument('filepaths', nargs='+', help='One or more files or directories to parse for TODO statements')
    args = parser.parse_args()

    setupBackupFolder()
    for fp in args.filepaths:
    	parseFile(fp, args)
#~/Documents/Python/todo-to-git-issue/.git $ less config
