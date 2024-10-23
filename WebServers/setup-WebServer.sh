#!/bin/bash

PYTHON_BIN=python3

BaseWebServerDirectory_Default=WebServer
PostFixDirectory_Default=AP1

BaseWebServerDirectory=
PostFixDirectory=

Directory_PythonEnv=.env

if [ "${1}" = "" ] ; then
  echo -ne "Type Web Server Directory name [${BaseWebServerDirectory_Default}]: "
  read BaseWebServerDirectory
  if [ "${BaseWebServerDirectory}" = "" ] ; then
    BaseWebServerDirectory=${BaseWebServerDirectory_Default}
  fi
else
  BaseWebServerDirectory=${1}
fi

if [ "${2}" = "" ] ; then
  echo -ne "Type service lookup port [${PostFixDirectory_Default}]: "
  read PostFixDirectory
  if [ "${PostFixDirectory}" = "" ] ; then
    PostFixDirectory=${PostFixDirectory_Default}
  fi
else
  PostFixDirectory=${2}
fi

Directory_WebServer=${BaseWebServerDirectory}-${PostFixDirectory}

echo "Creating Web Server examples directory..."
mkdir ${Directory_WebServer}

echo "Copying template files..."
cp -r _template/* ${Directory_WebServer}

echo "Changing to Web Server directory..."
cd ${Directory_WebServer}

echo "Creating Python environment..."
${PYTHON_BIN} -m venv ${Directory_PythonEnv}

echo "Activating the Python environment..."
${Directory_PythonEnv}/bin/pip install Flask
