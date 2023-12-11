import os
import shutil
import glob
import logging
import filecmp
from datetime import datetime
import zipfile


class container_to_save_data:
    def __init__(self, source: str, destination: str, time=100) -> None:
        """constructor
        input:  source of files
                destination(where to save)
                time(how often need to check updates)
        """

        logging.basicConfig(filename='example.log',
                            encoding='utf-8', level=logging.DEBUG)

        # is_exist_src = os.path.exists(source)
        # is_exist_dsc = os.path.exists(destination)

        # if is_exist_src and is_exist_dsc and time > 0:
        #     self.src = source  # need to check all values
        #     self.dst = destination
        #     self.time = time
        #     self.dirs_cmp = filecmp.dircmp(self.src, self.dst)
        #     logging.info("Class copy created")
        # else:
        #     # throw exception
        #     logging.error(
        #         f"Doesn't created because of: is_exist src and str and time - {is_exist_src, is_exist_dsc, (time > 0)}")

    def set_dst(self, dst: str):
        if dst:
            self.dst = dst
            logging.info("dst is upd'ed")

    def set_src(self, src: str):
        if os.path.exists(src):
            self.src = src
            logging.info("dst is upd'ed")

    def set_time(self, time: int):
        if time > 0:
            self.time = time

    def print_text(self):
        print(self)

    def create_name(self, src: str, dst: str):
        now = datetime.now()
        # tmp = os.path.join(dst, os.path.basename(
        #     src)+" backup_" + str(now.strftime("%d.%m.%Y_%Hh%Mm%Ss")))
        tmp = os.path.join(dst, "backup_" + str(now.strftime("%d.%m.%Y_%Hh%Mm%Ss")))
        tmp = os.path.join(tmp, os.path.basename(src))
        return tmp

    def ziping(self, src) -> str:
        """
        @path - path to folder you want to archive
        this function destroy existing path and return zip
        return path to new archive or if path already leads to archive or doesn't exist return itself
        """
        if not os.path.exists(src) or zipfile.is_zipfile(src):
            return src
        new_path = src
        try:
            # new_path = shutil.make_archive(os.path.join(path, f"{folder_name} zipped"), 'zip', src)
            new_path = shutil.make_archive(src, "zip", src)           
        except Exception as e:
            print(f"exeption: {e}")
            new_path = src
        try:
            shutil.rmtree(src)            
        except Exception as e:
            print(f"exeption: {e}")
        return new_path

    def rename_folder(self, new: str, old: str) -> bool:
        try:
            shutil.move(old, new)
            return True
        except Exception as e:
            print(f"exeption: {e}")
            return False

    def make_folder(self, path: str) -> bool:
        """
        Create new folder of new record
        input:  dst: string
                n: int - order number
                time: ? - time when record was created
        return: bool    
        """
        if not os.path.exists(path):
            return False

        try:
            os.mkdir(path)
            return True
        except Exception as e:
            print(f"exeption: {e}")
            return False

    def is_exist(self, path) -> bool:
        """
        Check is folder or file exist
        input:  src: string
        return: bool
        """
        return os.path.exists(path)
    
    def recover(self, src:str, dst:str) -> str:
        if not os.path.exists(src) and not os.path.exists(dst):
            raise f"Error: {dst} or {src} doesn't exists"
        tmp = ""
        if zipfile.is_zipfile(src):
            try:
                tmp = src.replace(".zip", "")
                shutil.unpack_archive(src, tmp)
            except Exception as e:
                print(f"error {e}")    
            try:
                os.remove(src)
            except Exception as e:  
                print(f"error {e}")    
        self.full_backup(tmp, dst)
        return tmp


    def full_backup(self, src: str, dst: str, ignore=[]) -> bool:
        """
        Create a copy of scr into dst
        input:  @src:     string
                @dst:     string
                @ingnore: list of ignored files
        return: bool
        """
        if not os.path.exists(src):
            return False
        try:
            if ignore:
                shutil.copytree(src, dst, ignore=shutil.ignore_patterns(
                    *ignore), dirs_exist_ok=True)
            else:
                shutil.copytree(src, dst, dirs_exist_ok=True)
            return True
        except Exception as e:
            print(f"error {e}")
            return False

    def cmp_folder(self, src: str, dst: str, ignore=[]) -> bool:
        """
        Compare two directories recursively. Files in each directory are
        assumed to be equal if their names and contents are equal.

        @param src: First directory path
        @param dst: Second directory path
        @param ignore: list of patter to ignore
        @return: True if the directory trees are the same and 
            there were no errors while accessing the directories or files, 
            False otherwise.
        """
        if not os.path.exists(src) or not os.path.exists(dst):
            return False
        ignore_list = []
        if not ignore:
            for pattern in ignore:
                ignore_left = [os.path.split(expanded)[1] for expanded in glob.glob(
                    os.path.join(src, pattern))]
                ignore_right = [os.path.split(expanded)[1] for expanded in glob.glob(
                    os.path.join(dst, pattern))]
                ignore_list.extend(ignore_left)
                ignore_list.extend(ignore_right)
            self.dirs_cmp = filecmp.dircmp(src, dst, ignore=ignore_list)
        else:
            self.dirs_cmp = filecmp.dircmp(src, dst)
        if len(self.dirs_cmp.left_only) > 0 or len(self.dirs_cmp.right_only) > 0 or \
                len(self.dirs_cmp.funny_files) > 0:
            return False
        (_, mismatch, errors) = filecmp.cmpfiles(
            src, dst, self.dirs_cmp.common_files, shallow=False)
        if len(mismatch) > 0 or len(errors) > 0:
            return False
        for common_dir in self.dirs_cmp.common_dirs:
            new_dir1 = os.path.join(src, common_dir)
            new_dir2 = os.path.join(dst, common_dir)
            if not self.cmp_folder(new_dir1, new_dir2):
                return False
        return True
    # need to add full backup, differential backup(copy only changed files)
    # add pattent of backuping: full -> dif -> dif -> dif -> full


if __name__ == '__main__':
    a = container_to_save_data(
        "D:/test\save_test\dst", "D:/test\save_test\dst", -1)
