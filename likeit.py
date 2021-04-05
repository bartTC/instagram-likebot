#!/usr/bin/env python3
import sys
from random import choice
from time import sleep

from progressbar import AbsoluteETA, Bar, progressbar
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# Wait extra long after each 'n' image
WAIT_EXTRALONG_EACH_IMAGE = 5

# Wait between the next image
WAIT_RANGE = [10, 40]  # 10 to 40s between each image

# Wait extra long between each `WAIT_EXTRALONG_EACH_IMAGE` image
WAIT_RANGE_EXTRALONG = [10 * 60, 20 * 60]  # 5 and 15min


# Wait before next click
WAIT_BEFORE_NEXT_CLICK = 3

driver = webdriver.Firefox()
driver.get("http://www.instagram.com")

sys.stdout.write(
    """
██╗     ██╗██╗  ██╗███████╗██████╗  ██████╗ ████████╗
██║     ██║██║ ██╔╝██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝
██║     ██║█████╔╝ █████╗  ██████╔╝██║   ██║   ██║   
██║     ██║██╔═██╗ ██╔══╝  ██╔══██╗██║   ██║   ██║   
███████╗██║██║  ██╗███████╗██████╔╝╚██████╔╝   ██║   
╚══════╝╚═╝╚═╝  ╚═╝╚══════╝╚═════╝  ╚═════╝    ╚═╝   
                                                     
OK. Next steps:

1) Login into your instagram account you want to like with.
2) Go to the user you want to like all photos and select 
   the first photo. That and all earlier pictures of that
   will be liked.
   
Hit Enter to contine: """
)

input1 = input()
i = 0
fails = 0

while True:
    i += 1

    try:
        try:
            like_button = driver.find_element_by_css_selector(
                'article[role=presentation] section [aria-label="Gefällt mir"]'
            )
            like_button.click()
            sys.stdout.write("❤️  Liked!\n")
        except NoSuchElementException:
            sys.stderr.write("❤️  Already liked.\n")
            pass

        sleep(WAIT_BEFORE_NEXT_CLICK)

        try:
            next_button = driver.find_element_by_class_name(
                "coreSpriteRightPaginationArrow"
            )
            next_button.click()
        except NoSuchElementException:
            sys.stderr.write("Next button not found (are we done?)\n")
            fails += 1

            if fails == 3:
                sys.stdout.write("Stopping here... 🏁")
                sys.exit()
            pass

        # Wait time between next image. We may multiple that time
        # every 'n' image.
        if i % WAIT_EXTRALONG_EACH_IMAGE == 0:
            wait = choice(range(*WAIT_RANGE_EXTRALONG))
            sys.stdout.write(f"Waiting {wait}s (extra long)\n")
        else:
            wait = choice(range(*WAIT_RANGE))
            sys.stdout.write(f"Waiting {wait}s\n")

        # Split wait time by 100 and display its progress
        for j in progressbar(range(100), widgets=[Bar(), AbsoluteETA()]):
            sleep(wait / 100)

        sys.stdout.write("\n")

    except Exception as e:
        import ipdb, os

        os.system("stty sane")
        ipdb.set_trace()
