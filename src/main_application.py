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

        verify_if_package_are_installed("steam2")
        self.all_packages = []
        self.new_install = []
        self.load_files()
        self.set_default_size(800, 650)
        self.set_title("My Personal Ubuntu Configuration")
        
        self.tab_view = Adw.TabView()
        tab_bar = Adw.TabBar.new()
        tab_bar.set_view(self.tab_view)
        
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        box.append(tab_bar)
        box.append(self.tab_view)
        self.set_child(box)

        self.create_tab("native")
        self.create_tab("flatpak")
        self.create_tab("snap")
        
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        button_box.set_halign(Gtk.Align.CENTER)

        box.append(button_box)

    def on_switch_toggled(self, switch_row, pspec):
        title = switch_row.get_title()
        if switch_row.get_active():
            self.new_install.append(title)
        else:
            self.new_install.remove(title)

    def create_tab(self, source):
        page = Adw.PreferencesPage()
        group = Adw.PreferencesGroup(title="Software")
        page.add(group)

        apps = self.all_packages[source]
        for item in apps:
            switch_row = Adw.SwitchRow(title=item)
            switch_row.connect("notify::active", self.on_switch_toggled)
            group.add(switch_row)

        my_button = Gtk.Button(label="Apply")
        my_button.get_style_context().add_class("suggested-action")
        my_button.get_style_context().add_class("raised")
        my_button.connect("clicked", self.on_click_apply, source)

        btn_upgrade_system = Gtk.Button(label="Upgrade System")
        btn_upgrade_system.connect("clicked", self.on_click_upgrade)
    
        
        group = Adw.PreferencesGroup(title="Actions")
        page.add(group)

        save_action_row = Adw.ActionRow(title="Actions")
        save_action_row.add_suffix(my_button)
        save_action_row.add_suffix(btn_upgrade_system)

        group.add(save_action_row)

        page = self.tab_view.append(page)
        page.set_title(source)

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

    def on_click_apply(self, button, source):
        install_packages(self.new_install, source)
    
    def on_click_upgrade(self, button):
        update_system()


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)    
    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

app = MyApp(application_id="com.github.philmagno.GtkApplication")
app.run(sys.argv)