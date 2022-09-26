
from tkinter import*
from tkinter.filedialog import askopenfilename
from tkinter import ttk
import pandas as pd
top=Tk()
frame=Frame(top)
frame.pack(pady=20)
tree=ttk.Treeview(frame)
def click():
    fn = askopenfilename()
    df = pd.read_csv (r''+fn)
    clear_tree()
    tree['column']=list(df.columns)
    tree['show']='headings'
    for column in tree['column']:
        tree.heading(column, text=column)
    df_rows=df.to_numpy().tolist()
    for row in df_rows:
        tree.insert("",'end',values=row)
    tree.pack()
def clear_tree():
    pass
myButton= Button(top, text='IMPORT', command=click)
myButton.pack()
top.mainloop()