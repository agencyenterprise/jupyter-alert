# see https://ipython.org/ipython-doc/3/config/custommagics.html
# for more details on the implementation here
import time

from IPython.core.getipython import get_ipython
from IPython.core.magic import line_magic, Magics, magics_class
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
import apprise
import os

apprise_config_path = os.path.join(os.path.dirname(__file__), '../apprise.yml')

# Create an Apprise instance
apobj = apprise.Apprise()
apconfig = apprise.AppriseConfig()
apconfig.add(apprise_config_path)
apobj.add(apconfig)


@magics_class
class JupyterAlert(Magics):
    _events = None, None
    run_start_time = None
    
    def __init__(self, shell, require_interaction=False):
        super(JupyterAlert, self).__init__(shell)
        self.options = {
            "requireInteraction": require_interaction,
            "icon": "/static/base/images/favicon.ico",
        }

    def send_alert(self, title="Great title", body="Awesome body"):
        apobj.notify(
            body=body,
            title=title,
        )

    @magic_arguments()
    @argument(
        "-a", "--after", default=None,
        help="Send notification if cell execution is longer than x seconds"
    )
    @argument(
        "-m",
        "--message",
        default="Cell Execution Has Finished!!",
        help="Custom notification message"
    )
    @argument(
        "-o",
        "--output", action='store_true',
        help="Use last output as message"
    )
    @line_magic
    def autoalert(self, line):
        # Record options
        args = parse_argstring(self.autoalert, line)
        self.options['body'] = args.message.lstrip("\'\"").rstrip("\'\"")
        self.options['autoalert_after'] = args.after
        self.options['autoalert_output'] = args.output

        self._update_events()
    
    def _update_events(self):
        ip = get_ipython()
        ip = self._remove_registered_events(ip)
        ip = self._register_events(ip)
        self._add_events_to_class()
    
    def _remove_registered_events(self, ip):
        # Remove events if they're already registered
        # This is necessary because jupyter makes a new instance everytime
        pre, post = self.__class__._events
        if pre and pre in ip.events.callbacks['pre_run_cell']:
            ip.events.callbacks['pre_run_cell'].remove(pre)
        if post and post in ip.events.callbacks['post_run_cell']:
            ip.events.callbacks['post_run_cell'].remove(post)
        return ip
    
    def _register_events(self, ip):
        # Register new events
        ip.events.register('pre_run_cell', self.pre_run_cell)
        ip.events.register('post_run_cell', self.post_run_cell)
        return ip
    
    def _add_events_to_class(self):
        self.__class__._events = self.pre_run_cell, self.post_run_cell

    def pre_run_cell(self, info):
        self.run_start_time = time.time()

    def post_run_cell(self, result):
        # Set last output as notification message
        # if True:
        #     last_output = None #get_ipython().user_global_ns['_']
        #     try:
        #         if last_output is not None and len(str(last_output)):
        #             print(last_output)
        #             # options['body'] = str(last_output)
        #     except ValueError:
        #         pass # can't convert to string. Use default message

        if elapsed_time:=self.check_after(): 
            body = f"Cell executed in {elapsed_time:.1f} seconds."
            self.send_alert(title="Completed cell execution", body = body)
        else: 
            return

    def check_after(self):
        # Check if the time elapsed is over the specified time.
        now, start = time.time(), self.run_start_time
        threshold = float(self.options.get('autoalert_after', -1))
        if threshold >= 0 and start and (now - start) >= threshold:
            return now-start
        else:
            return False
