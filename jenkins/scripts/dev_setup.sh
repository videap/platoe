#!/bin/bash

#### Check if there is a python environment, and install if not
echo ""
echo ""
echo ""
echo "Setting up Dev environment for Ubuntu 18+"
echo ""
echo ""
echo ""



echo "Checking Python"
if python3 -V =~ "Python 3" > /dev/null
then
  echo "Python 3 is installed"
else
  echo "Installing Python"
  sudo apt-get update && sudo apt-get install python3 -y
  if python3 -V =~ "Python 3" > /dev/null
    then
      echo "Python 3 was installed"
  fi
fi

echo "Checking git"
if git --version =~ "git" > /dev/null
then
  echo "git is installed"
else
  echo "Installing git "
  sudo apt-get install git
  echo "git installed"
fi

echo "Checking virtualenv"
if virtualenv --version =~ "virtualenv" > /dev/null
then
  echo "virtualenv is installed"
else
  echo "Installing virtualenv with pip3"
  pip3 install virtualenv
  echo "virtualenv installed"
fi


source ~/.profile
virtualenv venv-dev
activate () {
    . $PWD/venv-dev/bin/activate
    echo "virtualenv activated"
}

activate
pip install -r requirements.txt
echo "Required packages installed"
echo ""
echo ""
echo ""
echo "Platoe is deployed in development. You can start your service now."

