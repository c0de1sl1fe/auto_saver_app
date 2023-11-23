import os
import shutil
import logging
import filecmp


class container_to_save_data:
    def __init__(self, source: str, destination: str, time: int) -> None:
        """constructor
        input:  source of files
                destination(where to save)
                time(how often need to check updates)
        """

        logging.basicConfig(filename='example.log',
                            encoding='utf-8', level=logging.DEBUG)

        is_exist_src = os.path.exists(source)
        is_exist_dsc = os.path.exists(destination)

        if is_exist_src and is_exist_dsc and time > 0:
            self.src = source  # need to check all values
            self.dst = destination
            self.time = time
            logging.info("Class copy created")
        else:
            # throw exception
            logging.error(
                f"Doesn't created because of: is_exist src and str and time - {is_exist_src, is_exist_dsc, (time>0)}")
        self.dirs_cmp_structure = filecmp.dircmp(self.src, self.dst)

    def print_text(self):
        print(self)

    # def is_exist(self, path) -> bool:
    #     """
    #     Check is folder or file exist
    #     input:  src: string
    #     return: bool
    #     """

    #     os.path.exists
    #     print

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

    def copy_folder(self, src: str, dst: str) -> bool:
        """
        Create a copy of scr into dst
        input:  src: string
                dst: string
        return: bool
        """
        if not os.path.exists(src) or not os.path.exists(dst):
            return False
        try:
            shutil.copytree(src, dst)
            return True
        except Exception as e:
            print(f"error {e}")
            return False

    def cmp_folder(self, dir1: str, dir2: str) -> bool:
        """
        Compare two directories recursively. Files in each directory are
        assumed to be equal if their names and contents are equal.

        @param dir1: First directory path
        @param dir2: Second directory path

        @return: True if the directory trees are the same and 
            there were no errors while accessing the directories or files, 
            False otherwise.
    """

        dirs_cmp = filecmp.dircmp(dir1, dir2)
        if len(dirs_cmp.left_only) > 0 or len(dirs_cmp.right_only) > 0 or \
                len(dirs_cmp.funny_files) > 0:
            return False
        (_, mismatch, errors) = filecmp.cmpfiles(
            dir1, dir2, dirs_cmp.common_files, shallow=False)
        if len(mismatch) > 0 or len(errors) > 0:
            return False
        for common_dir in dirs_cmp.common_dirs:
            new_dir1 = os.path.join(dir1, common_dir)
            new_dir2 = os.path.join(dir2, common_dir)
            if not self.cmp_folder(new_dir1, new_dir2):
                return False
        return True


if __name__ == '__main__':
    a = container_to_save_data(
        "D:/test\save_test\dst", "D:/test\save_test\dst", -1)
