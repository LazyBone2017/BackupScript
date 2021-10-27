#!/bin/python

import os
import shutil
import datetime
import tarfile
import argparse

def copy(src, dst):
    for item in os.listdir(src):
        src_path = src + "/" + item
        dst_path = dst + "/" + item
        if os.path.isdir(src_path):
            os.mkdir(dst_path)
            copy(src_path, dst_path)
        else:
            shutil.copyfile(src_path, dst_path)

def archive(src, dst):
    dst = dst + ".tar"
    archive = tarfile.TarFile(name=dst, mode="w")
    archive.add(src)
    archive.close()

def check_versions(backup_dir, max_versions):
    backups = os.listdir(backup_dir)
    if len(backups) >= max_versions: #deletion
        backups.sort()
        for dir in backups:
            print(dir)
        for dir in backups[:len(backups) - max_versions + 1]:
            print("Delete: " + dir)
            abs_path = backup_dir + "/" + dir
            if os.path.isfile(abs_path):
                os.remove(abs_path)
            else:
                shutil.rmtree(abs_path)

def create_backup(src, dst, type):
    date = datetime.datetime.now().isoformat()[0:10]
    backups = os.listdir(dst)
    filepath = dst + "/" + date
    today_backups = list(filter(lambda bak: bak.startswith(date), backups))
    if len(today_backups) > 0:
        today_backups.sort()
        latest_backup = today_backups[-1]
        filenr_string = latest_backup.split('_')[-1]
        try:
            filenr = int(filenr_string)
        except:
            filenr = 0
        filepath += '_' + str(filenr + 1)

    if type == 'archive':
        archive(src, filepath)
    else:
        os.mkdir(filepath)
        copy(src, filepath)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A simple backup script intended to be called periodically, e.g. using cron')
    parser.add_argument('source', help='directory to be backed up')
    parser.add_argument('destination', help='directory where the backups are placed into')
    parser.add_argument('-b', '--backups', dest='backups', type=int, required=True, metavar='amount', help='how many backups to keep')
    parser.add_argument('-t', '--type', dest='type', type=str, choices=[ 'copy', 'archive' ], default='copy', help='store the backup as a copy or a tar file')
    args = parser.parse_args()

    if args.source[-1:] == '/':
        args.source = args.source[:-1]
    if args.destination[-1:] == '/':
        args.destination = args.destination[:-1]

    check_versions(args.destination, args.backups)
    create_backup(args.source, args.destination, args.type)
