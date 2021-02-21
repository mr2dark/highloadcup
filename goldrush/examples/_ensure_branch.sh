#!/bin/bash
set -euo pipefail

ENSURE_BRANCH=$1
BRANCH_NAME=$(git symbolic-ref -q HEAD)
BRANCH_NAME="${BRANCH_NAME##refs/heads/}"
git checkout "${ENSURE_BRANCH}"
[ "${BRANCH_NAME}" = "${ENSURE_BRANCH}" ] || { echo "ERROR: This following code must operate within '${ENSURE_BRANCH}' branch. The '${BRANCH_NAME}' branch is currently checked out." 1>&2; exit 1; }
git diff --cached --exit-code > /dev/null || { echo "ERROR: There are staged changes which will be included in the commit. Please commit those or remove from stage before proceeding with code generation." 1>&2; exit 1; }
