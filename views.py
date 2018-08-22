from flask import flash, render_template, session, redirect, request, make_response, url_for
from wsgi import app
from config import *
import os

# SET HOSTNAME
if not isinstance(CUSTOM_HOSTNAME, str) or len(CUSTOM_HOSTNAME) == 0:
    HOSTNAME = os.popen('cat /etc/hostname').read()
else:
    HOSTNAME = CUSTOM_HOSTNAME


def logged_in():
    try:
        return session['logged_in']
    except KeyError:
        return False


def to_login():
    flash('Please log in', 'info')
    return redirect(URL_PREFIX+'/login/')


# Login
@app.route('/')
def dashboard():
    # check login status
    if not logged_in():
        return to_login()
    # cpu percentage
    cpu_percent = round(float(os.popen("grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'").read()))
    # current cpu frequency
    cpu_freq = round(float(os.popen("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq").read())/1000000, 2)
    # cpu max frequency
    cpu_max = round(float(os.popen("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq").read())/1000000, 2)
    # cpu temperature
    cpu_temp = float(os.popen("vcgencmd measure_temp | grep -o \"[^=]*[^'C]\" | awk '{temp=$1} END {print temp}'").read())
    # total/free/used memory
    ram_total = round(int(os.popen("grep 'MemTotal: ' /proc/meminfo | awk '{total=$2} END {print total}'").read())/1000)
    ram_free = round(int(os.popen("grep 'MemFree: ' /proc/meminfo | awk '{free=$2} END {print free}'").read())/1000)
    ram_used = ram_total - ram_free
    ram_percent = round(ram_used / ram_total * 100)
    # uptime
    up_since = os.popen("uptime -s").read()
    up_for = os.popen("uptime -p").read()
    info = {'cpu_percent': cpu_percent,
            'cpu_freq': cpu_freq,
            'cpu_max': cpu_max,
            'ram_percent': ram_percent,
            'ram_used': ram_used,
            'ram_total': ram_total,
            'up_since': up_since,
            'up_for': up_for,
            'cpu_temp': cpu_temp,
            }
    return render_template('dashboard.html', HOSTNAME=HOSTNAME, info=info, URL_PREFIX=URL_PREFIX, logged_in=logged_in())


# Login
@app.route('/networking/nic-status/')
def ifconfig():
    # check login status
    if not logged_in():
        return to_login()
    result = os.popen('ifconfig')
    response = make_response(result.read())
    response.headers["content-type"] = "text/plain"
    return response


# Login
@app.route('/system/ps/')
def ps_list():
    # check login status
    if not logged_in():
        return to_login()
    result = os.popen('ps -aux')
    response = make_response(result.read())
    response.headers["content-type"] = "text/plain"
    return response


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session['logged_in'] = True
            flash('Welcome, '+USERNAME, 'success')
            return redirect(URL_PREFIX+'/')
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('login.html', HOSTNAME=HOSTNAME, URL_PREFIX=URL_PREFIX, logged_in=logged_in())


@app.route('/logout/')
def logout():
    if not logged_in():
        return to_login()
    session['logged_in'] = False
    return render_template('logout.html', HOSTNAME=HOSTNAME, URL_PREFIX=URL_PREFIX, logged_in=logged_in())
