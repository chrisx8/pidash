# Raspberry Pi Dashboard

A dashboard for Raspberry Pi devices running Raspbian. Built with Flask on Python 3.

**ONLY Raspbian on Raspberry Pi is supported! You'll get errors if you run it another distro!**

## Run with a virtual environment

Run the following on your Raspberry Pi

```bash
# Clone project source from Git
git clone https://github.com/chrisx8/raspberrypi-dashboard.git
cd raspberrypi-dashboard

# Install pip before continuing
# Install virtualenv
pip install --user virtualenv

# Create a virtual environment
virtualenv venv

# Activate environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
# Change 0.0.0.0:58000 to something else if you don't want the server on port 58000, or you don't want the server to be accessible from everywhere.
gunicorn wsgi:app -b 0.0.0.0:58000
```

## Run directly

This method is NOT RECOMMENDED, because running directly can make removing installed packages VERY difficult.

```bash
# Clone project source from Git
git clone https://github.com/chrisx8/raspberrypi-dashboard.git
cd raspberrypi-dashboard

# Install pip before continuing
# Install dependencies
pip install --user -r requirements.txt

# Run server
# Change 0.0.0.0:58000 to something else if you don't want the server on port 58000, or you don't want the server to be accessible from everywhere.
gunicorn wsgi:app -b 0.0.0.0:58000
```
