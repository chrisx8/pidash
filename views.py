import os

from flask import flash, make_response, redirect, render_template, request, session

from config import PASSWORD, URL_PREFIX, USERNAME
from wsgi import app

with open("/etc/hostname", "r") as f:
    HOSTNAME = f.read()


def logged_in():
    try:
        return session["logged_in"]
    except KeyError:
        return False


def to_login():
    flash("Please log in", "info")
    return redirect(URL_PREFIX + "/login/")


# Login
@app.route("/")
def dashboard():
    # check login status
    if not logged_in():
        return to_login()
    # cpu percentage
    cpu_percent = round(
        float(
            os.popen(
                "/bin/grep 'cpu ' /proc/stat | /usr/bin/awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'"
            ).read()
        )
    )
    # current cpu frequency
    cpu_freq = round(
        float(
            os.popen(
                "/bin/cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"
            ).read()
        )
        / 1000000,
        2,
    )
    # cpu max frequency
    cpu_max = round(
        float(
            os.popen(
                "/bin/cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq"
            ).read()
        )
        / 1000000,
        2,
    )
    # cpu temperature
    cpu_temp = round(
        float(os.popen("/bin/cat /sys/class/thermal/thermal_zone0/temp").read()) / 1000
    )
    # total/free/used memory
    ram_total = round(
        int(
            os.popen(
                "/bin/grep 'MemTotal: ' /proc/meminfo | /usr/bin/awk '{total=$2} END {print total}'"
            ).read()
        )
        / 1000
    )
    ram_free = round(
        int(
            os.popen(
                "/bin/grep 'MemAvailable: ' /proc/meminfo | /usr/bin/awk '{free=$2} END {print free}'"
            ).read()
        )
        / 1000
    )
    ram_used = ram_total - ram_free
    ram_percent = round(ram_used / ram_total * 100)
    # uptime
    up_since = os.popen("/usr/bin/uptime -s").read()
    up_for = os.popen("/usr/bin/uptime -p").read()
    info = {
        "cpu_percent": cpu_percent,
        "cpu_freq": cpu_freq,
        "cpu_max": cpu_max,
        "ram_percent": ram_percent,
        "ram_used": ram_used,
        "ram_total": ram_total,
        "up_since": up_since,
        "up_for": up_for,
        "cpu_temp": cpu_temp,
    }
    return render_template(
        "dashboard.html",
        HOSTNAME=HOSTNAME,
        info=info,
        URL_PREFIX=URL_PREFIX,
        logged_in=logged_in(),
    )


# Login
@app.route("/networking/nic-status/")
def ifconfig():
    # check login status
    if not logged_in():
        return to_login()
    result = os.popen("/sbin/ifconfig")
    response = make_response(result.read())
    response.headers["content-type"] = "text/plain"
    return response


# Login
@app.route("/system/ps/")
def ps_list():
    # check login status
    if not logged_in():
        return to_login()
    result = os.popen("/bin/ps -aux")
    response = make_response(result.read())
    response.headers["content-type"] = "text/plain"
    return response


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # credentials correct
        if (
            request.form["username"] == USERNAME
            and request.form["password"] == PASSWORD
        ):
            session["logged_in"] = True
            return redirect(URL_PREFIX + "/")
        # bad credentials
        flash("Invalid credentials!", "danger")
    return render_template(
        "login.html", HOSTNAME=HOSTNAME, URL_PREFIX=URL_PREFIX, logged_in=logged_in()
    )


@app.route("/logout/")
def logout():
    session["logged_in"] = False
    return to_login()
