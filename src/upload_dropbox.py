import argparse
import dropbox
import multiprocessing
import os
from functools import partial

class Dropbox:

    def login(self):
        # for safety reason, token should not be hard-coded
        token = os.environ["DROPBOX_TOKEN"]
        dbx = dropbox.Dropbox(token)

        return dbx

    def uploaded(self, dbx, dir_output):
        files = dbx.files_list_folder(f"/GitHub/NBER/{dir_output}")
        entries = []
        while files.has_more:
            entries.append([x.name for x in files.entries])
            cursor = files.cursor
            files = dbx.files_list_folder_continue(cursor)

        last = dbx.files_list_folder_get_latest_cursor(f"/GitHub/NBER/{dir_output}")
        last = dbx.files_list_folder_continue(cursor)
        entries.append([x.name for x in last.entries])

        uploaded = []
        for i in entries:
            for j in i:
                uploaded.append(j)

        return uploaded

    def upload_dropbox(self, dbx, dir_input, dir_output, nber_id):
        upload = open(f"{dir_input}/{nber_id}", "rb").read()
        try:
            dbx.files_upload(upload, f"/GitHub/NBER/{dir_output}/{nber_id}", mute=True)
            dbx.close()
            print(f"[{nber_id}]: successfully uploaded to Dropbox")
        except Exception as e:
            # errors should be printed so that could be debugged later
            print(f"[{nber_id}]: failed uploading file to Dropbox due to {e}")
            dbx.close()

if __name__ == "__main__":
    # add argument for command line usage
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("-i", "--input", type=str, choices=["data/nber", "paper"], help="Directory for input data", metavar="")
    PARSER.add_argument("-o", "--output", type=str, choices=["working-paper-json", "working-paper-txt"], help="Dropbox folder", metavar="")
    ARGS = PARSER.parse_args()
    DIR_INPUT = ARGS.input
    DIR_OUTPUT = ARGS.output
    CPU = multiprocessing.cpu_count() - 1
    WORKING_PAPERS = os.listdir(DIR_INPUT)

    # upload multiple files to dropbox using parallelism
    d = Dropbox()
    dbx = d.login()
    uploaded = d.uploaded(dbx, DIR_OUTPUT)
    to_upload = [x for x in WORKING_PAPERS if x not in uploaded]
    pool = multiprocessing.Pool()
    func = partial(d.upload_dropbox, dbx, DIR_INPUT, DIR_OUTPUT)
    pool.map(func, to_upload)
    pool.close()
    pool.join()
    