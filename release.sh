#!/bin/bash

set -e

# make sure origin/master is what we expect
ORIGIN=$(git config --get remote.origin.url)
EXPECTED_ORIGIN="git@github.com:authy/authy-python.git"

if [ "$ORIGIN" != "$EXPECTED_ORIGIN" ]
then
  echo "Unexpected remote $ORIGIN. Please make sure your remote origin is $EXPECTED_ORIGIN"
  exit
else
  echo "Remote origin verified. Proceeding to get the latest from master."
fi

# make sure you have the bumpversion dependency
command -v bumpversion >/dev/null 2>&1 || { echo "Activate your virtualenv for 'bumpversion' dependency" >&2; exit 1; }

# this will fail if there are local changes. that's ok.
git checkout master
git fetch && git rebase

########################
# UPDATE RELEASE NOTES #
########################

echo "Updating release notes"

bash notes.sh

################
# BUMP VERSION #
################

# https://github.com/peritus/bumpversion
# This command does several things!
#    * updates patch versions in .bumpversion.cfg and authy/__init__.py
#    * Adds+commits to Git .bumpversion.cfg and authy/__init__.py files
#    * Adds Git tag with new version

echo 'Bumping patch version'

bumpversion patch

##################
# DEPLOY CHANGES #
##################

echo 'Commiting changes and pushing to master'

# commit changes to master
# this will kick off the Travis CI build which auto-deploys to PyPI
git push origin master --tags
