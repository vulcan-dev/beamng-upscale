from os import path, rename, listdir, remove
from wand import image
import sys

_DDSFileDir = './dds_files'
_UpscaledDir = './upscaled'
_OutputDir = './output'

files_no_convert = []

def CopyAndRename(src_directory, dst_directory, extension, s2=False):
    file_count = 0
    f = None
    if s2:
        f = open('avoid.txt', 'r')

    try:
        for file in listdir(src_directory):
            try:
                if file.endswith('.png'): files_no_convert.append(file) # If the original file is a png, append that to a list which will exclude the files from being renamed in step2
                with image.Image(filename=f'{src_directory}/{file}') as i:
                    try:
                        file_count += 1

                        # Setup 2 (Rename files back to original)
                        if s2:
                            # before renaming, check if the name is in avoid.txt and if it is, skip that file because it's a png and we don't want to convert that
                            file_to_ignore = f.readline().strip()
                            if file != file_to_ignore:
                                i.save(filename=f'{dst_directory}/{file[:-4]}.{extension}')
                                remove(f'{dst_directory}/{file}')
                            # if file != f.read(file_count):

                            #print(f'Deleted file: {file}')

                        elif not s2: # Setup 1 (Rename files to .png)
                            if file.endswith('.dds'):
                                # Rename file
                                i.save(filename=f'{dst_directory}/{file[:-4]}.{extension}')
                            else:
                                # If the orignal file end with .png, keep that same extension
                                i.save(filename=f'{dst_directory}/{file[:-4]}.png')

                        print(f'[{file_count}] Copied "{file}" from "{src_directory}/" to "{dst_directory}/"')
                    except Exception as e:
                        pass
                        print(f'Unable to copy file "{file}" from {src_directory}/ to {dst_directory}/ [{e}]')
            except:
                print(f'{file} is not an image')

    except KeyboardInterrupt:
        exit()

    print(f'Copied and renamed {file_count} files from "{src_directory}/" to "{dst_directory}/"')

    # Loop through files_no_convert and store all values into avoid.txt
    if not s2:
        f = open('avoid.txt', 'a')
        for line in files_no_convert:
            f.write(f'{line}\n')
        
    f.close()

if __name__ == '__main__':
    try:
        for i, arg in enumerate(sys.argv): # Get cmd arguments
            if arg == '-s1': # Copy all files from "dds_files" to "output" with the extension .png
                file_count = 0
                CopyAndRename(_DDSFileDir, _OutputDir, 'png')

            elif arg == '-s2':
                CopyAndRename(_UpscaledDir, _UpscaledDir, 'dds', s2=True)
    except KeyboardInterrupt:
        pass

# Steps
# 1. Put all dds files in the directory "dds_files" (can also do other formats such as png, jpg, etc...)
# 2. Run this script with arg "-s1" (This will convert all images to png and move them to the output directory)
# 3. Open Gigapixel and upscale all, then save to the upscaled directory
# 4. Run script again with arg "-s2" (This will rename all files to the original ones and then convert them back to dds (if their orignal extension wasn't .png))