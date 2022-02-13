#!/bin/sh -eu
if [ -z "${URL:-}" ]; then
    URL_JSON=undefined
else
    URL_JSON=$(jq -n --arg url '$URL' '$url')
fi

cat <<EOF
REACT_APP_URL=$BRAND_JSON;
EOF