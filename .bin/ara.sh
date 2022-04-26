#!/bin/bash

if echo "$1" | grep -o -q -P "\p{Arabic}"; then
	S="$1"
	S="${S/)/(}"
	S="${S/(/)}"
	echo "${S}" | ara
else
	echo "$1"
fi
