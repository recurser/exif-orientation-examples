#!/usr/bin/env python

from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color
import os
import sys

def get_transformation_lst():
    transformation_lst = [
        {
            'exif_tag':         0,
            'rotation_degrees': 0,
            'flop':             False,
        },
        {
            'exif_tag':         1,
            'rotation_degrees': 0,
            'flop':             False,
        },
        {
            'exif_tag':         2,
            'rotation_degrees': 0,
            'flop':             True,
        },

        {
            'exif_tag':         3,
            'rotation_degrees': 180,
            'flop':             False,
        },
        {
            'exif_tag':         4,
            'rotation_degrees': 180,
            'flop':             True,
        },
        {
            'exif_tag':         5,
            'rotation_degrees': -90,
            'flop':             True,
        },
        {
            'exif_tag':         6,
            'rotation_degrees': -90,
            'flop':             False,
        },
        {
            'exif_tag':         7,
            'rotation_degrees': 90,
            'flop':             True,
        },
        {
            'exif_tag':         8,
            'rotation_degrees': 90,
            'flop':             False,
        },
    ]

    return transformation_lst


def generate_exif_orientation_images(image_path):
    """
    Load image that with EXIF but without orientation.
    Then add EXIF orientation by applying flip/rotate transformations.
    Finally save as image files.
    
    wand library is an easy-to-use wrapper for ImageMagic.
    ImageMagic load and save image with EXIF contained.
    """
    transformation_lst = get_transformation_lst()
    for transformation in transformation_lst:
        image = Image(filename=image_path)
        exif_flag = transformation['exif_tag']

        # draw text, optional
        with Drawing() as draw:
            dimension = max(image.height, image.width)
            font_size = dimension / 20

            draw.stroke_width = 1
            draw.stroke_color = Color('black')
            draw.fill_color = Color('white')
            draw.font = 'wandtests/assets/Helvetica.otf'
            draw.font_size = font_size

            # center
            x = (int)(image.width / 2)
            y = (int)(image.height / 2)
            draw.text(x, y, str(exif_flag))

            # top
            draw.gravity = 'north'
            draw.text(0, 0, 'top')

            # bottom
            draw.gravity = 'south'
            draw.text(0, 0, 'bottom')

            # right
            draw.gravity = 'east'
            draw.text(0, 0, 'right')

            draw.gravity = 'west'
            draw.text(0, 0, 'left')
            draw(image)

        # flop (horizontal flip)
        do_flop = transformation['flop']
        if (do_flop):
            image.flop()

        # rotate
        rotate_degree = transformation['rotation_degrees']
        if (rotate_degree==90):
            image.rotate(90)
        elif (rotate_degree==180):
            image.rotate(180)
        elif (rotate_degree==-90):
            image.rotate(270)

        # save as file
        im_name = os.path.split(image_path)[-1]
        im_head = '.'.join(im_name.split('.')[:-1])
        im_ext = im_name.split('.')[-1]
        save_name = im_head + '_' + str(exif_flag) + '.jpg'
        image.save(filename=save_name)

        # use exiftool for EXIF convert
        cmd = 'exiftool -overwrite_original -orientation={:d} -n {:s}'.format(
            exif_flag, save_name
        )
        stream = os.popen(cmd)
        output = stream.read().strip()
        print('executing command: {:s}'.format(cmd))
        print('    {:s}'.format(output))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: {:s} /path/to/image'.format(sys.argv[0]))
        exit()

    generate_exif_orientation_images(sys.argv[1])