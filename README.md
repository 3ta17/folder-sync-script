# Folder Sync Script

This script synchronizes a `source` folder with a `replica` folder at regular intervals.

## Features
- One-way synchronization (source → replica)
- Periodic sync using a defined interval
- Logging to `log.txt`
- Supports `Ctrl + C` to stop execution

## Usage
### **1. Run with command-line arguments**
```sh
python sync.py -source source/ -replica replica/ -interval 10 -log log.txt
This case will check synchronized per 10 seconds
