# Welcome to Jupyter Alert
![Alt text](assets/logo.png?raw=true "logo")


Jupyter Alert is a Jupyter magic that alerts you when you jupyter cell finishes running.

Using the power of [Apprise](https://github.com/caronc/apprise), we can send alerts to almost all popular notification services, including Slack, Telegram, SMS, email, and many many more.

Here is an example of it working with Slack:

![Alt text](assets/example.gif?raw=true "example with slack")

## Installation
Clone this repo, and within the root folder:
```
pip install -e .
```
## Adding alert channels

To add your alert channels, create a file `apprise.yml` file at the root of the codebase following [Apprise's documentation](https://github.com/caronc/apprise/wiki/config_yaml).
For each alert channel of interest, look at how they should be setup following [Apprise's instructions](https://github.com/caronc/apprise#supported-notifications).


## Automatically run jupyter alert in every notebook:
Add the following lines to your ipython startup file:
```
c.InteractiveShellApp.extensions = [
    'jupyter_alert'
]
```

Also add the following line to define how long, in seconds, you'd like the minimum elapsed (from start to end of a cell) time to be for you to get a notification:
```
c.InteractiveShellApp.code_to_run = '%autoalert -a 2'
```

The .ipython startup file can be generated with ipython profile create [profilename] and will create a configuration file at ~/.ipython/profile_[profilename]/ipython_config.py'. Leaving [profilename] blank will create a default profile (see this for more info).

## Roadmap
* Include results in alerts
* Ideally, include figures as well
* Create configuration commands:
 * Enable and disable alerts
 * Change minimum elapsed time for alert


## Acknowledgements
Thank you ShopRunner to making available the [jupyter notify](https://github.com/ShopRunner/jupyter-notify) project, which was used as a base for this work.

