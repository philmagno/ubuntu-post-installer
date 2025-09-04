from gettext import install
import sys
import gi
import yaml
from post_utils import *
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.all_packages = []
        self.installed = []
        self.load_files()
        self.set_default_size(800, 300)
        self.set_title("My Personal Ubuntu Configuration")

        header = Gtk.HeaderBar()
        header.pack_start(Gtk.Label(label="My Personal Installer"))
        self.set_titlebar(header)

        self.page_native_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.page_native_content.append(Gtk.Label(label="Native/APT packages"))

        self.page_native = self.create_configured_flowbox()
        self.page_native_content.append(self.page_native)

        self.page_flatpak_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.page_flatpak_content.append(Gtk.Label(label="Flatpacks packages"))

        self.page_flatpak = self.create_configured_flowbox()
        self.page_flatpak_content.append(self.page_flatpak)

        self.page_snap_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.page_snap_content.append(Gtk.Label(label="Snap packages"))

        self.page_snap = self.create_configured_flowbox()
        self.page_snap_content.append(self.page_snap)

        self.create_pages("native", self.page_native, self.page_native_content)
        self.create_pages("flatpak", self.page_flatpak, self.page_flatpak_content)
        self.create_pages("snap", self.page_snap, self.page_snap_content)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(500)

        stack.add_titled(self.page_native_content, "page_native", "Native")
        stack.add_titled(self.page_flatpak_content, "page_flatpak", "Flatpak")
        stack.add_titled(self.page_snap_content, "page_snap", "Snap")

        stack_switcher = Gtk.StackSwitcher(orientation=Gtk.Orientation.HORIZONTAL)
        stack_switcher.set_stack(stack)

        #add stack in main
        self.set_child(stack)

        header.set_title_widget(stack_switcher)

    def create_configured_flowbox(self):
        flowbox = Gtk.FlowBox()
        flowbox.set_valign(Gtk.Align.START)
        flowbox.set_row_spacing(5)
        flowbox.set_max_children_per_line(3)
        flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        return flowbox

    def load_files(self):
        with open('packages.yaml', 'r') as file:
            self.all_packages = yaml.safe_load(file)

    def create_pages(self, source, page, page_parent):
        apps = self.all_packages[source]
        for item in apps:
            box = Gtk.CheckButton(label=item)
            box.connect("toggled", self.on_checkbox_toggled)
            page.append(box)

        box_button = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        button = Gtk.Button(label="Apply")
        button.connect("clicked", self.on_click_native, source)
        box_button.append(button)

        button_upgrade = Gtk.Button(label="Upgrade System")
        button_upgrade.connect("clicked", self.on_click_upgrade)
        box_button.append(button_upgrade)
        page_parent.append(box_button)

    def on_click_native(self, button, source):
        install_packages(self.installed, source)
    
    def on_click_upgrade(self, button):
        update_system()
        
    def on_checkbox_toggled(self, button):
        if button.get_active():
            self.installed.append(button.get_label())

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)    
    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

app = MyApp(application_id="com.github.philmagno.GtkApplication")
app.run(sys.argv)