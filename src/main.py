#!/usr/bin/python3
import tkinter as tk
import clarifai_predict as engine
import config
from PIL import ImageTk, Image
import urllib.request
import io
from clsMySysImage import mysysImages
import json

def search_images():
    print("Search Item: %s." % (e1.get()))
    process_search_image(1)
    print('Completed!')


def process_search_image(posn):
    theConfig = config.getConfig('../resource/config-prd.json')
    results = engine.predictImage(theConfig, e1.get(), posn)
    json_msg = json.loads(results)
    show_result(json_msg)

def show_result(results):
    for record in results:
        try:
            engine.open_result(record)
        except Exception as err:
            print("show_result: {0}".format(err))


def change_start_posn(root):
    # Apparently a common hack to get the window size. Temporarily hide the
    # window to avoid update_idletasks() drawing the window in the wrong
    # position.
    root.withdraw()
    root.update_idletasks()  # Update "requested size" from geometry manager

    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.geometry("+%d+%d" % (x, y))

    # This seems to draw the window frame immediately, so only call deiconify()
    # after setting correct window position
    root.deiconify()

def process_next_page():
    pos = res.get_next_page()
    print('next result: {0}'.format(pos))
    process_search_image(pos)
    print('Completed!')

if __name__ == "__main__":

    res = mysysImages()

    master = tk.Tk()
    font_size = ('Verdana', 20)

    tk.Label(master, text="Search: ", font=font_size).grid(row=0)

    e1 = tk.Entry(master, font=font_size)
    e1.grid(row=0, column=1)


    tk.Button(master, text='Quit', command=master.quit, font=font_size).grid(row=3, column=0, pady=4)
    tk.Button(master, text='Run', command=search_images, fg="Blue",font=font_size).grid(row=3, column=1, pady=4)
    tk.Button(master, text='Next', command=process_next_page, fg="Blue",font=font_size).grid(row=3, column=2, pady=4)

    change_start_posn(root=master)
    tk.mainloop( )