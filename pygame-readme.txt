Steps for making pygame work on VENV without SUDO:

Make virtualenv

python --no-site-packages venv

venv/include is a symlink to the GLOBAL python header files.
This is bad.

Remember the symlink path.

unlink the symlink.

copy the python2.7 headers FOLDER to the python virtual env folder of the no unlinked symlink.

get files from mercurial:
hg clone http://bitbucket.org/pygame/pygame

python setup.py install  (The header trick allows you to install without sudo.)
