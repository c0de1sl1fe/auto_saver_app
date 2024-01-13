import os
import shutil
import glob
import logging
import filecmp
from datetime import datetime
import zipfile
import hashlib

from github import Github
import logging


class InterfaceFileOperation:
    def __init__(self) -> None:
        """constructor
        input:  source of files
                destination(where to save)
                time(how often need to check updates)
        """
        self.name = "c0de1sl1fe"
        self.hash = ""
        self.chaging_list = []
        self.logger = self.setup_logging()

    def setup_logging(self) -> None:
        """setup logging"""
        logger = logging.getLogger("logger")
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            file_handler = logging.FileHandler("autosaver.log")
            file_handler.setLevel(logging.WARNING)
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        return logger

    def load_login(self):
        """fucntion for load hash from file on github"""
        try:
            g = Github()
            user = g.get_user(self.name)
            for content in user.get_repo("auto_saver_app").get_contents("Passwords"):
                if content.path.endswith(".txt"):
                    self.hash = content.decoded_content.decode("utf-8")
        except Exception as e:
            self.logger.warning(f"Raised exception: {e} while load login")

    def check_user(self, login: str, password: str) -> bool:
        """Function to check users loging and password
        @login: your login
        @Password: your password
        inside this function app requests file with hashed password
        and then compart it with users password
        """
        my_hash = hashlib.md5((login+password).encode('utf-8')).hexdigest()
        if self.hash:
            return my_hash == self.hash
        try:
            g = Github()
            user = g.get_user(self.name)
            hash = ""
            for content in user.get_repo("auto_saver_app").get_contents("Passwords"):
                if content.path.endswith(".txt"):
                    hash = content.decoded_content.decode("utf-8")
            return my_hash == hash
        except Exception as e:
            self.logger.warning(f"Raised exception: {e} login")
            return False

    def create_name(self, src: str, dst: str, upd=False) -> str:
        """create name with time of backup
            @param src - is source of folder
            @param dst - is destination for folder
            return dst + name of folder src + str(backup_ + time)
        """
        now = datetime.now()
        tmp = ""
        if upd:
            tmp = os.path.join(
                dst, "backup_upd_" + str(now.strftime("%d.%m.%Y_%Hh%Mm%Ss")))
        else:
            tmp = os.path.join(
                dst, "backup_" + str(now.strftime("%d.%m.%Y_%Hh%Mm%Ss")))
        tmp = os.path.join(tmp, os.path.basename(src))
        self.logger.info(f"New name was created [{tmp}]")
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
            self.logger.info(f"Create archive - {new_path}")
        except Exception as e:
            self.logger.warning(f"Raised exception: {e} while archive")
            new_path = src
        try:
            shutil.rmtree(src)
            self.logger.info(f"Complete removing tree - {src}")

        except Exception as e:
            self.logger.warning(f"Raised exception: {e} while removing dir")
        return new_path

    def rename_folder(self, new: str, old: str) -> bool:
        try:
            shutil.move(old, new)
            self.logger.info(f"Folder {old} renamed to {new}")
        except Exception as e:
            self.logger.warning(f"Raised exception: {e} while rename")
            return False

        if os.path.exists(os.path.split(old)[0]):
            try:
                shutil.rmtree(os.path.split(old)[0])
                return True
            except Exception as e:
                self.logger.warning(f"Raised exception: {e} while rename")
                return False
        return True

    def is_dir(self, path) -> bool:
        """
        Check is folder or file exist
        input:  src: string
        return: bool
        """
        tmp = os.path.isdir(path)
        self.logger.info(f"Complete is_dir({tmp}) for {path}")
        return tmp

    def recover(self, src: str, dst: str) -> str:
        if not os.path.exists(src) and not os.path.exists(dst):
            self.logger.info(f"Raised exception because of src: {
                             src} or dst: {dst} doesn't exist")
            return ""
        tmp = src
        if zipfile.is_zipfile(src):
            try:
                tmp = src.replace(".zip", "")
                shutil.unpack_archive(src, tmp)
                self.logger.info(f"Complete unpack archive {src} for recover")
            except Exception as e:
                self.logger.warning(f"Raised exception: {
                                    e} while unpack archive {src} in recover")
            try:
                os.remove(src)
                self.logger.info(f"complete remove {src} for recover")
            except Exception as e:
                self.logger.warning(f"Raised exception: {
                                    e} while remove {src}")
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
            self.logger.warning(f"{src} doesn't exist while full_backup")
            return False
        try:
            if ignore:
                shutil.copytree(src, dst, ignore=shutil.ignore_patterns(
                    *ignore), dirs_exist_ok=True)
                self.logger.info(f"complete copy {src} to {
                                 dst} with ignore_pattern")
            else:
                shutil.copytree(src, dst, dirs_exist_ok=True)
                self.logger.info(f"complete copy {src} to {
                                 dst} without ignore_pattern")
            return True
        except Exception as e:
            self.logger.warning(f"Raised exeption: {
                                e} while copy {src} to {dst}")
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
            self.logger.warning(f"cmp_folder for {src} and {
                                dst} doens't complete")
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
            print(1)
            return False
        (_, mismatch, errors) = filecmp.cmpfiles(
            src, dst, self.dirs_cmp.common_files, shallow=False)
        if len(mismatch) > 0 or len(errors) > 0:
            self.chaging_list.append(mismatch)
            return False
        for common_dir in self.dirs_cmp.common_dirs:
            new_dir1 = os.path.join(src, common_dir)
            new_dir2 = os.path.join(dst, common_dir)
            if not self.cmp_folder(new_dir1, new_dir2):
                return False
        return True

    def stats(self):
        """ returns changing_list """
        return self.chaging_list

    def clear_stats(self):
        """ clear changing_list """
        self.chaging_list.clear()


if __name__ == '__main__':
    a = InterfaceFileOperation()
