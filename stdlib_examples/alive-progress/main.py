import alive_progress as ap
import time

from alive_progress import alive_bar

long_range = range(10000)

'''
change spinner to see other bar styles, here are some options:
- classic
- stars
- arrow

you may see more with 
    alive_progress.show_bars()
'''

with alive_bar(len(long_range), title="example 1", spinner = 'pulse') as bar:
    for el in long_range:
        # make some output every 1000 loops
        if 0 == el % 1000:
            # this will output propertly, 
            # clean the whole screan, 
            # bar goes to next line.
            print(f"{el} processed.")

            # let's change the bar text, which shows on right end of the bar
            bar.text(f"{el}")

        # sleep for a short while
        time.sleep(0.01)

        # update bar count
        bar()
