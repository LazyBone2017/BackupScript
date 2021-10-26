#!/bin/python

import os
import shutil
import sys
import datetime
import tarfile

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
        for dir in backups[:max_versions + 1]:
            print("Delete: " + dir)
            abs_path = backup_dir + "/" + dir
            if os.path.isfile(abs_path):
                os.remove(abs_path)
            else:
                shutil.rmtree(abs_path)

def create_backup(src, dst, type):
    date = datetime.datetime.now().isoformat()[0:10]
    if type == 'archive':
        archive(src, dst + "/" + date)
    else:
        os.mkdir(dst + "/" + date)
        copy(src, dst + "/" + date)

if __name__ == "__main__":
    src = sys.argv[1]
    dst = sys.argv[2]
    max_versions = int(sys.argv[3])
    backup_type = "copy" if len(sys.argv) <= 4 else sys.argv[4]
    if src[-1:] == "/":
        src = src[:-1]
    if dst[-1:] == "/":
        dst = dst[:-1]

    check_versions(dst, max_versions)
    create_backup(src, dst, backup_type)
