from .JupyterAlert import JupyterAlert


def load_ipython_extension(ipython):
    ipython.register_magics(JupyterAlert)