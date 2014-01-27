# Metadata Index

A list of `libraries` will be kept in `~/.config/ebmeta/libraries.json` as a sorted list of (name, path) pairs.

Each library will have a `~/.local/share/data/ebmeta/NAME.sqlite` file.

During a file display/edit operation, if a `library` isn't defined for the current folder, then no index will be used.

## Tables

### files

  * id
  * mtime (unix milliseconds timestamp)
  * folder_id
  * file_name
  * title
  * title_sort
  * author_sort
  * publication_date
  * publisher
  * book_producer
  * isbn
  * language
  * rating
  * series_id
  * series_index
  * description (html snippet)

### folders

  * id
  * relative_path (empty string or parent folder, relative from root, with slashes)
  * name

### authors

  * id
  * name
  * sort

### files_authors

  * file_id
  * author_id

### tags

  * id
  * name

### files_tags

  * file_id
  * tag_id

### series

  * id
  * name

## Index HMTL Files

An `index.html` file will be kept in each directory showing files and folders in that directory. External CSS and JavaScript resources for this file will be kept in `.index/` under the library root.

## Behavior

When an individual file is edited, then any changes to that file are written to the index file. Additionally, the parent folder of that file is scanned for new, changed, or delete files with respect to the data in the index file, and any necessary index updates are made.

A `refresh_db` command will scan the entire collection that the current folder belongs to and process any changes from the files to the index.
