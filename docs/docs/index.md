# synch_de documentation!

## Description

Investigating Distance Learning

## Commands

The Makefile contains the central entry points for common tasks related to this project.

### Syncing data to cloud storage

* `make sync_data_up` will use `az storage blob upload-batch -d` to recursively sync files in `data/` up to `placeholder_container/data/`.
* `make sync_data_down` will use `az storage blob upload-batch -d` to recursively sync files from `placeholder_container/data/` to `data/`.


