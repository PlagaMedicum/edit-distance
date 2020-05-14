from text_grabber import *
import numpy as np

from tkinter import *

def find_edit_distance(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix[x, y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1)
            else:
                matrix[x, y] = min(
                    matrix[x-1, y] + 1,     # delete
                    matrix[x-1, y-1] + 1,   # replace
                    matrix[x, y-1] + 1)     # insert
    return matrix[size_x - 1, size_y - 1]

sourcewords = []

def update_source_texts():
    for word in grab_text(url.get()):
        sourcewords.append(word)

root = Tk()

url = StringVar()
inputword = StringVar()
maxeditdist = IntVar()
res = StringVar()


def update_result():
    edistmap = {word: find_edit_distance(inputword.get(), word) for word in sourcewords}

    filteredmap = dict(filter(lambda elem: elem[1] <= maxeditdist.get(), edistmap.items()))
    sortedlist = [key for key, value in sorted(filteredmap.items(), key=lambda item: item[1])]

    res.set("\n".join(list(set(sortedlist))))

    result_window()

def help_window():
    children = Toplevel(root)
    children.title('Help')

    helpmsg = """
1. Enter the URL with source texts in arabic and press button "fetch data" to update sources
2. Enter the word to check
3. Enter the maximal edit distance
4. See a list of all possible words
    """

    text = Text(children, height=20, width=100)
    scroll = Scrollbar(children)
    scroll.pack(side=RIGHT, fill=Y)
    text.pack(side=LEFT, fill=Y)
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)
    text.insert(END, helpmsg)

def result_window():
    children = Toplevel(root)
    children.title('Result')

    text = Text(children, height=20, width=100)
    scroll = Scrollbar(children)
    scroll.pack(side=RIGHT, fill=Y)
    text.pack(side=LEFT, fill=Y)
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)
    text.insert(END, res.get())

root.title("Edit distance analyser")
root.geometry("900x400")

urllabel = Label(text="URL with source texts")
urllabel.place(relx=.2, rely=.1, anchor="c")
urlentry = Entry(width=40, textvariable=url)
urlentry.place(relx=.5, rely=.1, anchor="c")
urlbutton = Button(text="Fetch data", command=update_source_texts)
urlbutton.place(relx=.8, rely=.1, anchor="c")

textlabel = Label(text="Word to check")
textlabel.place(relx=.2, rely=.2, anchor="c")
textentry = Entry(width=40, textvariable=inputword)
textentry.place(relx=.5, rely=.2, anchor="c")
urlbutton = Button(text="Find edit distance", command=update_result)
urlbutton.place(relx=.8, rely=.2, anchor="c")

medlabel = Label(text="Maximal edit distance")
medlabel.place(relx=.2, rely=.25, anchor="c")
medentry = Entry(width=40, textvariable=maxeditdist)
medentry.place(relx=.5, rely=.25, anchor="c")

help = Button(text="Help", command=help_window)
help.place(relx=.5, rely=.8, anchor="c")

root.mainloop()
