import glob
filetypes = "/Users/brianlibgober/Box Sync/Backup/Justia/2000/*.txt"
for i in glob.iglob(filetypes):
    print i