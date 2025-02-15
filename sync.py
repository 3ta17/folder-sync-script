import os
import time
import shutil
import logging
import argparse
from utils import setup_logging, get_hash


def get_args():

    parser = argparse.ArgumentParser(description="Folder Synchronization Program")
    parser.add_argument("-source", help="Path to the source folder")
    parser.add_argument("-replica", help="Path to the replica folder")
    parser.add_argument("-interval", type=int, help="Sync interval in seconds")
    parser.add_argument("-log", default="log.txt", help="Path to the log file (default: log.txt)")

    args = parser.parse_args()

    # If arguments are not provided, ask for user input
    source = args.source if args.source else input("Enter source folder path: ")
    replica = args.replica if args.replica else input("Enter replica folder path: ")
    interval = args.interval if args.interval else 30

    return source, replica, interval, args.log


def check_folders(src, rep):
    # Check if source and replica folders exist
    if not os.path.exists(src):
        print("Error: Source folder missing")
        logging.error("Source folder missing")
        return False
    if not os.path.exists(rep):
        print("Replica folder does not exist, creating...")
        logging.info("Replica folder does not exist, creating...")
        os.makedirs(rep)
    return True


def copy_files(src, rep):
    # Copy new or updated files from source to replica
    for root, _, files in os.walk(src):
        rpath = os.path.relpath(root, src)
        rep_root = os.path.join(rep, rpath)

        if not os.path.exists(rep_root):
            os.makedirs(rep_root)

        for f in files:
            s_file = os.path.join(root, f)
            r_file = os.path.join(rep_root, f)

            # Compare files using hash and copy if necessary
            if not os.path.exists(r_file) or get_hash(s_file) != get_hash(r_file):
                shutil.copy2(s_file, r_file)
                print(f"Copied: {s_file} -> {r_file}")
                logging.info(f"Copied: {s_file} -> {r_file}")


def delete_extra(rep, src):
    # Remove files and folders from replica that do not exist in source
    for root, _, files in os.walk(rep, topdown=False):
        rpath = os.path.relpath(root, rep)
        src_root = os.path.join(src, rpath)

        for f in files:
            r_file = os.path.join(root, f)
            s_file = os.path.join(src_root, f)

            if not os.path.exists(s_file):
                os.remove(r_file)
                print(f"Deleted: {r_file}")
                logging.info(f"Deleted: {r_file}")

        # Skip removing empty folders to avoid permission errors
        if not os.listdir(root):
            print(f"Warning: Empty folder detected in replica (not removed): {root}")
            logging.warning(f"Empty folder detected in replica (not removed): {root}")


def sync(src, rep):
    """ Perform folder synchronization """
    copy_files(src, rep)
    delete_extra(rep, src)

def main():
   # Main process: Run sync in an infinite loop
    source, replica, interval, log_file = get_args()

    print("Setting up logging")
    setup_logging(log_file)

    print("Checking folders")
    if not check_folders(source, replica):
        return

    print("Starting sync process now!\n")

    while True:
        try:
            print("Syncing (this might take some time)")
            sync(source, replica)
            print(f"Done! Next {interval} seconds later\n")
            logging.info(f"Sync completed! Waiting {interval} seconds before next sync.")
            time.sleep(interval)

        except KeyboardInterrupt:
            print("\nSync process stopped by user.")
            break

main()