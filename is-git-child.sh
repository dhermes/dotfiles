#!/bin/bash
set -e

if [[ "${#}" != 2 ]]; then
  echo "Usage: is-git-child.sh <child-guess> <parent-guess>."
  exit 1
fi

CHILD="${1}"
PARENT="${2}"
PARENT_TIP=$(git log "${PARENT}" -1 --pretty=%H)
MERGE_BASE=$(git merge-base "${PARENT}" "${CHILD}")
if [[ "${PARENT_TIP}" == "${MERGE_BASE}" ]]; then
  echo "Yes: ${PARENT_TIP}."
else
  echo "No. ${PARENT} ends in"
  echo "    ${PARENT_TIP}"
  echo "while the merge base is"
  echo "    ${MERGE_BASE}."
fi
