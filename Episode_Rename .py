from tkinter import *
import os
from tkinter import messagebox
from tkinter import filedialog
import re
import  operator

main = Tk()
main.title("Rename Episodes")
main.geometry("300x150")

filepath = StringVar()
series = StringVar()
prog = StringVar()

file_list = []

class files:
  def __init__(self,series,episode_num):
    self.episode_num = episode_num
    self.series = series

position = 0
def sortlist(position):
  file_list.clear()
  List = os.listdir(filepath.get())
  for File in List:
    file = os.path.splitext(File)[0]
    number = re.findall('[0-9]+',file)
    if number:
      try:
        new = files(file,int(number[position]))
        file_list.append(new)
        cont = True
      except IndexError as error:
        print(error)
        cont = False
        break
  sortedFiles = sorted(file_list, key = operator.attrgetter('episode_num'))
  if cont == True:
    increasing(sortedFiles)
  else:
    pass
  return sortedFiles

def increasing(sortedList):
  global position
  current = 0
  for i, j in zip(sortedList, sortedList[1:]):
    if i.episode_num < j.episode_num:
      current += 1
    else:
      current = 0
      break
  if current == len(sortedList[1:]):
    print ("increasing number!")
  else:
    sortedList.clear()
    position += 1
    sortlist(position)

def renameButton():
  try:
    os.chdir(filepath.get())
    sortlist(position)
    print ("Position to call is:", position)
    List = os.listdir(filepath.get())
    for File in List:
      number = re.findall('[0-9]+',File)
      if number:
        try:
          ext = os.path.splitext(File)[1]
          newname = series.get() + " Episode " + number[position] + ext
          os.rename(File, newname)

        except IndexError as error:
          newname = series.get() + " Episode " + number[position - 1] + ext
          os.rename(File, newname)

    messagebox.showinfo("Result", "Successful!")

  except (FileNotFoundError, OSError) as Error:
    messagebox.showwarning("Error", Error)


def clearButton():
    filepath.set('')
    series.set('')

def paste():
    path = filedialog.askdirectory()
    filepath.set(path)


pasteBtn = Button(main, text = "Select Folder", command = paste)
pasteBtn.place(x = 105, y = 10)

fileEntry = Entry(main, width = 40, textvariable = filepath)
fileEntry.place(x = 30, y = 40)

seriesLabel = Label(main, text = "Enter Series Name")
seriesLabel.place(x = 30, y = 70)

seriesEntry = Entry(main, textvariable = series)
seriesEntry.place(x =  130, y = 72)

renameButton = Button(main,padx = 10, text = "Start!", command = renameButton)
renameButton.place(x = 70, y = 100)

clearButton = Button(main,padx = 10, text = "Clear", command = clearButton)
clearButton.place(x = 170, y = 100)

main.mainloop()
