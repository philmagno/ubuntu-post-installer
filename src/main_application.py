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
        self.set_default_size(800, 650)
        self.set_title("My Personal Ubuntu Configuration")
        
        self.tab_view = Adw.TabView()
        tab_bar = Adw.TabBar.new()
        tab_bar.set_view(self.tab_view)
        
        # Layout principal
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        box.append(tab_bar)
        box.append(self.tab_view)
        self.set_child(box)

        # Adiciona algumas abas de exemplo
        self.create_tab("native")
        self.create_tab("flatpak")
        self.create_tab("snap")
        
        # Caixa de botões (rodapé)
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        button_box.set_halign(Gtk.Align.CENTER)  # alinhado à direita

        btn_cancelar = Gtk.Button(label="Install")
        btn_cancelar.connect("clicked", lambda b: print("Cancelar clicado"))
        button_box.append(btn_cancelar)

        btn_confirmar = Gtk.Button(label="Upgrade System")
        btn_confirmar.connect("clicked", self.on_click_upgrade)
        button_box.append(btn_confirmar)

        # Adiciona botão ao final da caixa principal
        box.append(button_box)

    def on_switch_toggled(self, switch_row, pspec):
        title = switch_row.get_title()
        if switch_row.get_active():
            print(f"toggle ativado para:{title}")
        else:
            print(f"toggle desativadas para:{title}")

    def create_tab(self, source):
        page = Adw.PreferencesPage()

        # Criar grupo
        group = Adw.PreferencesGroup(title="Software")
        page.add(group)

        apps = self.all_packages[source]
        for item in apps:
            # Criar SwitchRow
            switch_row = Adw.SwitchRow(title=item)
            # Detectar mudança no switch
            switch_row.connect("notify::active", self.on_switch_toggled)
            group.add(switch_row)

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