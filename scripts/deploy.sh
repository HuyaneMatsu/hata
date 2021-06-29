#!/bin/bash
set -e

LIBRARY_NAME="hata"

# Get correct folder

folder_name=${PWD##*/}

if [ "$folder_name" = "scripts" ]
then
    echo "Script called from the scripts folder moving to outer directory."
    cd ..
    folder_name=${PWD##*/}
fi

if [[ "$folder_name" != *$LIBRARY_NAME* ]]
then
    echo "Upper folder is probably not a $LIBRARY_NAME folder, since it has no $LIBRARY_NAME in it's name; Exiting"
    return 0 2>/dev/null || exit 0
fi

# Check environmnetal variables

function get_and_set_env {
    local env_var_name=$1
    local env_var_value
    
    if [ -z ${!env_var_name+x} ] || [ -z ${!env_var_name} ]
    then
        echo "${env_var_name} environmnetal variable is empty or missing."
        echo "Please define your ${env_var_name} environmental variable:"
        
        read -r env_var_value
        export "${env_var_name}=${env_var_value}"
    fi
}

# get_and_set_env "GITHUB_TOKEN"
get_and_set_env "TWINE_USERNAME"
get_and_set_env "TWINE_PASSWORD"

# Install dependencies

python3 -m pip install setuptools twine

# Upload

echo "Deploying"
python3 setup.py sdist bdist_wheel

set +e
python3 -m twine upload --disable-progress-bar --skip-existing --non-interactive --repository pypi dist/*

# Remove temporary files

echo "Removing temporary files"

rm -r build
rm -r dist
rm -r "$LIBRARY_NAME.egg-info"

return 0 2>/dev/null || exit 0

