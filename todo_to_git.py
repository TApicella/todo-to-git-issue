""" A script for creating github issues automatically from TODO comments """

import requests, os, shutil, argparse

def setupBackupFolder():
	""" If a backup folder for this script doesn't exist, create it and add it to .gitignore """
	if not os.path.isdir("./todo-to-git-backup"):
		os.makedirs("./todo-to-git-backup")
		with open("./.gitignore", 'ab') as g:
			g.write("./todo-to-git-backup")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A script to automatically create github issues from TODO comments", epilog="(ADD EXAMPLE)")
    parser.add_argument('-r', '--recursive', action='store_true', default=False, help='Use --recursive to run this script on all files within a given directory')
    parser.add_argument('filepaths', nargs='+', help='One or more files or directories to parse for TODO statements')

#~/Documents/Python/todo-to-git-issue/.git $ less config