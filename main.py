import tkinter as tk

from client.app import Frame, menu_bar

def main():
    root = tk.Tk()
    root.title('FortiMail filter')
    
    menu_bar(root)

    app = Frame(root=root)

    app.mainloop()

if __name__ == '__main__':
    main()