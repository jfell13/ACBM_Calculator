from subprocess import Popen


def load_jupyter_server_extension(nbapp):
    """serve the dash-app directory with flask server"""
    Popen(["python", "./dash-app/main.py"])
