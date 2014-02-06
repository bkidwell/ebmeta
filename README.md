ebmeta
======

(In progress, unfinished.) Edit metadata in an epub, mobi, or pdf file.

This is a Python 3 port of the unfinished project at https://github.com/bkidwell/ebmeta-old . The overall goal of this project is to deliver a desktop/server application that can edit the metadata in your ebook collection, in the way that [EasyTag](https://wiki.gnome.org/Apps/EasyTAG) edits your audio files' metadata in place. You should be able to sync your ebook files across different hosts using tools like ownCloud or DropBox, simply by comparing file dates and propagating changes; you shouldn't have to worry about extra metadata in a database that can't be synced, the way Calibre works.

``ebmeta`` will maintain a local (not to be synced across different hosts) passive index of all metadata in your collection in an SQLite database. Whenever you operate on a folder or one of its files, all the files in that folder will be checked to see if the index needs updating. (There will also be a global refresh command.) The index will be used to generate an ``index.html`` file in each folder of your collection, for easy browsing in a web browser.

Initially ``ebmeta`` will have a command-line-only interface, but in a future release we will add GUI dialog boxes that can be invoked directly from your favorite file manager. (For example, right-click an ebook file and select "Tag with ebmeta".)
