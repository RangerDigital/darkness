#!/bin/bash
# WARNING: REQUIRES /bin/bash

# URL for darkness.py
URL="https://raw.githubusercontent.com/RangerDigital/darkness/master/darkness-cli/darkness.py"

# Exits with error message.
crit_error(){
  printf "Critical Error!"
  printf "$1"
  exit 1
}

# Checks if command exists.
exists() {
  if command -v "$1" >/dev/null 2>"&1"
  then
    return 0
  else
    return 1
  fi
}

# Downloads file to directory. URL FILENAME
do_curl() {
  curl -o "$2" --retry 5 "$1" || return 1
  return 0
}

printf "1. Checking user permissions..."
if [ "$EUID" -ne 0 ]; then
  crit_error "Aborting! Must be run with sudo."
fi

printf "2. Checking platform..."
if [[ $(uname) != "Linux" ]]; then
  crit_error "Aborting! Currently supports only Linux."
fi

printf "3. Downloading darkness.py..."
if exists curl; then
  do_curl $URL "/usr/bin/darkness" || crit_error "Aborting! Couldn't download darkness.py file."
else
  crit_error "Aborting! Check if have Curl installed."
fi

printf "4. Setting permisions..."
chmod +x /usr/bin/darkness || crit_error "Aborting! Couldn't set file permissions."

printf "5. Installing Python dependencies..."
if exists python3; then
  python3 -m pip install click requests spectra || crit_error "Aborting! Error while installing dependencies."

elif exists python; then
  python -m pip install click requests spectra || crit_error "Aborting! Error while installing dependencies."

else
  crit_error "Aborting! Check if have Python installed."
fi

if exists apt; then
  printf "6. Check for missing libs for numpy..."
  apt install libatlas3-base
fi

echo "Success! Try it: darkness --help"
