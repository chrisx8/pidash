# PiDash

A simple, lightweight system monitoring dashboard for Raspberry Pi.

**ONLY Raspbian on Raspberry Pi is supported! You'll get errors if you run it on another distro!**

![Screenshot](screenshot.png)

## Table of Contents
<!-- MarkdownTOC -->

- [Features](#features)
- [Set up](#set-up)
    - [Edit the config file](#edit-the-config-file)
    - [Add your current user to `video` group](#add-your-current-user-to-video-group)
    - [Run with a virtual environment](#run-with-a-virtual-environment)
- [Advanced configuration](#advanced-configuration)
    - [Automatically launch on startup with `supervisor`](#automatically-launch-on-startup-with-supervisor)
    - [Set up behind a Nginx reverse proxy](#set-up-behind-a-nginx-reverse-proxy)

<!-- /MarkdownTOC -->

## Features

- Simple and lightweight: less than 100KB and installs in less than a minute
- Easily customizable: quickly add features and customize webpages (pull requests are always welcome!)
- Monitor system resources (CPU, RAM, uptime, etc.)
- View network information and running processes

## Set up

### Edit the config file

Definitely change the default username, password, and secret key in `config.py` !

### Add your current user to `video` group

```bash
sudo usermod -aG video $USER
```

### Run with a virtual environment

Run the following on your Raspberry Pi

```bash
# Clone project source from Git
git clone https://github.com/chrisx8/raspberrypi-dashboard.git
cd raspberrypi-dashboard

# Install pip before continuing
sudo apt-get install python3-pip

# Install virtualenv
pip install --user virtualenv

# Create a virtual environment
virtualenv venv

# Activate environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
# Change 0.0.0.0:58000 to whereever you want PiDash to listen at
gunicorn wsgi:app -b 0.0.0.0:58000
```

## Advanced configuration

### Automatically launch on startup with `supervisor`

- Step 1: Install supervisor
    ```bash
    sudo apt-get update
    sudo apt-get install supervisor
    ```
- Step 2: Configure

    Edit `/etc/supervisor/conf.d/raspberrypi-dashboard.conf` with your favorite text editor (such as `nano` or `vi`)

    Paste the following into the file:
    ```
    [program:raspberrypi-dashboard]
    command=/path/to/raspberrypi-dashboard/venv/bin/gunicorn wsgi:app -b 0.0.0.0:58000
    directory=/path/to/raspberrypi-dashboard
    autostart=true
    autorestart=true
    startretries=3
    user=<YOUR USERNAME>
    group=<YOUR USERNAME>
    stdout_logfile=NONE
    stderr_logfile=NONE
    ```
- Step 3: Restart supervisor
    ```bash
    sudo supervisorctl reload
    ```

### Set up behind a Nginx reverse proxy

- Step 1: Complete [supervisor setup](#automatically-launch-on-startup-with-supervisor)
- Step 2: Make sure PiDash is listening at 127.0.0.1
- Step 3: Install Nginx
    ```bash
    sudo apt-get update
    sudo apt-get install nginx
    ```
- Step 4: Configure Nginx

    Add the following into your Nginx server config:
    ```
    # Change the path to whatever you like
    location /dashboard/ {
        proxy_set_header        X-Real-IP $remote_addr;
        proxy_set_header        X-Forwarded-For $remote_addr;
        proxy_set_header        X-Forwarded-Proto $scheme;
        # This needs to match the path defined earlier!
        proxy_set_header        Host $host/dashboard/;
        proxy_intercept_errors  on;
        proxy_pass http://127.0.0.1:58000/;  # Change 58000 to the port set in supervisor config
    }
    ```
- Step 3: Restart supervisor and Nginx
    ```bash
    sudo supervisorctl reload
    sudo systemctl restart nginx
    ```
