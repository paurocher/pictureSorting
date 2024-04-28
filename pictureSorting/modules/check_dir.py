import os

"""These were useful after I restored the data from the disc with deleted 
pictures. All this data was saved in folders with 1000 files in them. Folders
were named ŕecup_dir0, recup_dir1, ...

"list_extensions" lists the extensions from all files in folders.
"clean_dirs_by_ext" deletes files if their xtension is in the suffix_kill list.
"""

root_dir = "/media/fuku/T7/recup2/"

start = 00
end = 1000

sufix_kill = [".plist", ".txt", ".wav", ".mp3", ".gz", ".m4p",
".json", ".DS_Store", ".sqlite", ".zip", ".sh", ".html", ".h",
".swc", ".xml", ".rtf", ".ics", ".woff", ".ini", ".doc", ".ai",
".xmp", ".c", '.sxw', '.fcp', '.class', '.mp4', '.xar', '.exe', '.par2',
".xpi", '.ttf', '.jsonlz4', '.kmz', '.pfx', '.aif', '.au', '.jar', 
'.3gp', '.m3u', '.odt', '.svg', '.wma', '.icns', '.swf', '.apple', 
'.aep', '.pdf', '.xls', '.pm', '.asp', '.ifo', '.m2ts', '.rar', '.pyc',
'.ods', '.flac', '.vcf', '.iso', '.xlsx', '.cab', '.c4d', '.xpt', '.flv', '.torrent', '.pptx', '.prproj', '.bmp', '.ppt', '.pap', '.acb', '.sit', 
'.mat', '.mbox', '.bz2', '.tar', '.ps', '.mkv', '.f', '.dll', '.tz', 
'.epub', '.csv', '.mid', '.icc', '.msf', '.url', 
'.fuse_hidden0000026500000004', '.fuse_hidden0000026500000005', '.elf', '.ico', '.bat', '.php', '.jsp', '.ogg', '.indd', '.cdr', '.7z', '.abr', '.eps', '.docx', '.pl', '.db', 
'.MYI', '.caf', '.inf', '.dv', '.py', '.amr','.deb', '.java']

def clean_dirs_by_ext():
    """For all folders in a directory, it will DELETE any file if its extension
    is in the śuffux_kill' extensions list. If the folder is empty it will
    DELETE it as well.
    """
    for i in range(start, end+1):
        path = "{}recup_dir.{}".format(root_dir, i)
        if os.path.exists(path):
            files = os.listdir(path)
            if not files:
                os.rmdir(path)
            for file in files:
                for suf in sufix_kill:
                    if file.endswith(suf):
                        delete = "{}/{}".format(path, file)
                        print(delete)
                        os.remove(delete)

clean_dirs_by_ext()

def list_extensions():
    exts = set()
    for i in range(start, end+1):
        path = "{}recup_dir.{}".format(root_dir, i)
        if os.path.exists(path):
            files = os.listdir(path)
            if not files:
                continue
            for file in files:
                try:
                    exts.add(file.split(".")[1])
                except:
                    print(file)
    print(exts)
#list_extensions()
