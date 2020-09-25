import os
import idautils
import idaapi
import idc
import thread
import traceback

from binkit.viewer import *
from binkit.service import *

class BinkitPlugin(idaapi.plugin_t):
    wanted_name = "Binkit"    
    wanted_hotkey = "Alt-F12"
    comment = "Binkit Plugin For IDA"
    help = "Use this plugin to load diffing result files (*.json)..."
    flags = idaapi.PLUGIN_KEEP

    def init(self):
        self.viewer_sequence = 0
        self.get_connection_filename()
        thread.start_new_thread(start_binkit_server, (self.connection_filename,))  
        return idaapi.PLUGIN_KEEP

    def get_connection_filename(self):
        binkit_profile = os.path.join(os.environ['USERPROFILE'], '.binkit')
        if not os.path.isdir(binkit_profile):
            try:
                print("Creating %s" % binkit_profile)
                os.makedirs(binkit_profile)
            except:
                traceback.print_exc()
            
        md5 = idc.GetInputMD5().lower()
        self.connection_filename = os.path.join(binkit_profile, "%s-%d.port" % (md5, os.getpid()))

    def run(self, arg):
        filename = get_filename()
        if filename and os.path.isfile(filename):
            viewer = Viewer()
            form_name = "Function Matches-%d" % self.viewer_sequence
            self.viewer_sequence += 1
            viewer.show_functions_match_viewer(form_name)
            idaapi.set_dock_pos(form_name, "Functions window", idaapi.DP_TAB)

    def term(self):
        if os.path.isfile(self.connection_filename):
            try:
                print("Removing %s" % self.connection_filename)
                os.remove(self.connection_filename)
            except:
                traceback.print_exc()

def PLUGIN_ENTRY():
    return BinkitPlugin()
