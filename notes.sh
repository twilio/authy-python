#!/bin/bash

REPOSITORY_URL="https://github.com/authy/authy-python"

PREVIOUS_TAG=$(git describe --abbrev=0 --tags)
NEW_VERSION=$(bumpversion --dry-run --list patch | grep new_version | sed s,"^.*=",,)
LATEST_TAG="v$NEW_VERSION"

# Get a log of commits that occured between two tags
# We only get the commit hash so we don't have to deal with a bunch of ugly parsing
# See Pretty format placeholders at https://git-scm.com/docs/pretty-formats
echo "Grabbing all commits since $PREVIOUS_TAG"
COMMITS=($(git log $PREVIOUS_TAG..HEAD --pretty=format:"%H"))

# Store our changelog in a variable to be saved to a file at the end
MARKDOWN="\nVersion $NEW_VERSION\n"
MARKDOWN+="--------------------\n"
MARKDOWN+="[Full Changelog]($REPOSITORY_URL/compare/$PREVIOUS_TAG...$LATEST_TAG)\n"

echo "Looking through ${#COMMITS[@]} commits for merged PRs"

# Loop over each commit and look for merged pull requests
for COMMIT in "${COMMITS[@]}"; do
	# Get the subject of the current commit
	SUBJECT=$(git log -1 ${COMMIT} --pretty=format:"%s")

	# If the subject contains "Merge pull request #xxxxx" then it is deemed a pull request
	PULL_REQUEST=$( grep -Eo "Merge pull request #[[:digit:]]+" <<< "$SUBJECT" )
  echo $PULL_REQUEST
	if [[ $PULL_REQUEST ]]; then
		# Perform a substring operation so we're left with just the digits of the pull request
		PULL_NUM=${PULL_REQUEST#"Merge pull request #"}

		# Get the body of the commit
		BODY=$(git log -1 ${COMMIT} --pretty=format:"%b")
		MARKDOWN+="\n - [#$PULL_NUM]($REPOSITORY_URL/pull/$PULL_NUM): $BODY"
  fi
done

echo "Updating CHANGES with merged PRs"

# Insert our new changes into the Changelog
awk -v n=5 -v s="$MARKDOWN" 'NR == n {print s} {print}' CHANGES > CHANGES.new

head CHANGES.new

mv CHANGES.new CHANGES

git commit -am "Log CHANGES for release $LATEST_TAG"
