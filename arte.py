#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
from gi.repository import Gtk
import feedparser as fp
from os import system


class FenetreArte:
    """Class permettant d'importer les émissions d'arte"""

    def __init__(self):
        self.window = Gtk.Window()
        self.window.set_default_size(1200, 600)
        self.window.set_title("Téléchargement d'émission Arte+7")
        self.createWidgets()
        self.connectSignals()

    def run(self):
        self.window.show_all()
        Gtk.main()

    def on_app_exit(self, widget, event=None):
        Gtk.main_quit()

    def on_treeview_selection_changed(self, selection):
        (model, treeiter) = selection.get_selected()
        if treeiter is not None:
            self.emission = model[treeiter][3]

    def on_boutonArte_clicked(self, widget):
        print self.emission
        system('youtube-dl -f HTTP_MP4_HQ_1 -o \'/home/jciavaldini/Vidéos/%(title)s-%(playlist)s-%(id)s.%(ext)s\' '+self.emission)

    def createWidgets(self):

        # La liste des émissions
        self.liststore = Gtk.ListStore(str, str, str, str)
        renderer_text = Gtk.CellRendererText()
        renderer_text.props.wrap_width = 300
        # renderer_text.props.wrap_mode = Gtk.WRAP_WORD
        try:
            programme = fp.parse('http://www.arte.tv/papi/tvguide-flow/feeds/videos/fr.xml?type=ARTE_PLUS_SEVEN')
        except:
            print "erreur chargement du flux"
        # print programme
        t = [[i.arte_channel, i.title, i.summary, i.link] for i in programme.entries]
        for emission in t:
            self.liststore.append([emission[0], emission[1], emission[2], emission[3]])
        self.treeview = Gtk.TreeView(self.liststore)
        names = ["Arte_channel", "Titre", "Résumé", "Lien"]
        for i in xrange(len(names)):
            column = Gtk.TreeViewColumn(names[i], renderer_text, text=i)
            column.set_sort_column_id(i)
            column.set_expand(True)
            if i == 0 or i == 1:
                column.set_max_width(80)
            elif i == 2:
                column.set_min_width(350)
            else:
                column.set_visible(False)
            self.treeview.append_column(column)

        # bouton pour télécharger
        self.boutonArte = Gtk.Button(label="Télécharger")
        self.boutonArte = Gtk.Button(label="Télécharger")

        # ajout des listes à la fenetre scrollable
        self.scrolledwindow = Gtk.ScrolledWindow()
        self.scrolledwindow.add(self.treeview)
        self.scrolledwindow.set_min_content_height(350)

        # boite générale
        self.contourBoite = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.contourBoite.set_homogeneous(False)
        self.contourBoite.pack_start(self.scrolledwindow, True, True, 0)
        self.contourBoite.pack_start(self.boutonArte, False, True, 0)

        self.window.add(self.contourBoite)

    def connectSignals(self):
        self.window.connect('delete-event', self.on_app_exit)
        self.select = self.treeview.get_selection().connect("changed", self.on_treeview_selection_changed)
        self.boutonArte.connect("clicked", self.on_boutonArte_clicked)

if __name__ == '__main__':
    programme = FenetreArte()
    programme.run()
