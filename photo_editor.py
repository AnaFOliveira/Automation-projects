import os
from PIL import Image, ImageFilter


def edit_photo(path, path_out):

    if not os.path.exists(path):
        return -1

    if not os.path.exists(path_out):
        os.makedirs(path_out)

    for photo_dir in os.listdir(path):
        img = Image.open(f"{path}/{photo_dir}")
        edit = img.filter(ImageFilter.DETAIL)

        name_pic = os.path.splitext(photo_dir)[0]
        full_dir_out = os.path.join(path_out, f"{name_pic}_edited.jpg")
        print("dir: ",full_dir_out)
        edit.save(full_dir_out)
        print("finish")


if __name__ == '__main__':
    in_dir = "./photos/"
    out_dir = "./edited/"
    edit_photo(in_dir, out_dir)
