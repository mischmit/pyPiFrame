import glob

# Scans recursively for .jp?g files and collects
def getFiles():
    return glob.glob("*.jp?g")
