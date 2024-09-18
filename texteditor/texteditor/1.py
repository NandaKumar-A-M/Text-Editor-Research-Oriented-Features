import wikipediaapi
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, font, simpledialog, ttk
import re
import requests
from PIL import Image, ImageTk
from get_language_code import Language
from transformers import pipeline

# x = Language().get_language_code("Kannada")
# print(x)
def open_file(event=None):
    filepath = filedialog.askopenfilename(
        filetypes=[("Text Files", ".txt"), ("All Files", ".*")]
    )
    if not filepath:
        return
    text.delete(1.0, tk.END)
    with open(filepath, "r") as input_file:
        content = input_file.read()
        text.insert(tk.END, content)
    window.title(f"SE7EN - {filepath}")


def save_file(event=None):
    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", ".txt"), ("All Files", ".*")]
    )
    if not filepath:
        return
    with open(filepath, "w") as output_file:
        text_content = text.get(1.0, tk.END)
        output_file.write(text_content)
    window.title(f"SE7EN - {filepath}")


def new_file(event=None):
    text.delete(1.0, tk.END)
    window.title("SE7EN - Untitled")

def cut_text():
    text.event_generate("<<Cut>>")

def copy_text():
    text.event_generate("<<Copy>>")


def paste_text():
    text.event_generate("<<Paste>>")

def undo_action():
    text.event_generate("<<Undo>>")


def redo_action():
    text.event_generate("<<Redo>>")


def change_text_color():
    color = colorchooser.askcolor()[1]
    if color:
        text.config(fg=color)


def change_font_style(event=None):
    current_tags = text.tag_names("sel.first")
    if "bold" in current_tags:
        text.tag_remove("bold", "sel.first", "sel.last")
    else:
        text.tag_add("bold", "sel.first", "sel.last")
        bold_font = font.Font(text, text.cget("font"))
        bold_font.config(weight="bold")
        text.tag_configure("bold", font=bold_font)

def text_statistics():
    content = text.get(1.0, tk.END)
    word_count = len(re.findall(r'\b\w+\b', content))
    char_count = len(content) - content.count('\n')
    sentence_count = len(re.findall(r'[.!?]+', content))
    
    messagebox.showinfo("Text Statistics", f"Word Count: {word_count}\nCharacter Count: {char_count}\nSentence Count: {sentence_count}")


def find_text(event=None):
    target = simpledialog.askstring("Find", "Enter text to find:")
    if target:
        start_pos = "1.0"
        while True:
            start_pos = text.search(target, start_pos, stopindex=tk.END)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(target)}c"
            text.tag_add("highlight", start_pos, end_pos)
            start_pos = end_pos
        text.tag_configure("highlight", background="yellow")


def replace_text(event=None):
    find = simpledialog.askstring("Replace", "Enter text to find:")
    replace = simpledialog.askstring("Replace", "Enter replacement text:")
    if find and replace:
        content = text.get(1.0, tk.END)
        new_content = re.sub(rf'\b{re.escape(find)}\b', replace, content)
        text.delete(1.0, tk.END)
        text.insert(tk.END, new_content)

def hide_right_pane():
    paned_window.forget(right_pane)
    

        
def show_split_functionality(command):

    for widget in right_pane.winfo_children():
        widget.destroy()
    
    close_button = tk.Button(right_pane, text="X", command=hide_right_pane, font=("Arial", 12, "bold"), bg="red", fg="white")
    close_button.place(relx=1.0, rely=0.0, anchor="ne")

    if not paned_window.panes() or paned_window.panes()[-1] != str(right_pane):
        paned_window.add(right_pane, minsize=50)
        paned_window.paneconfig(left_pane,minsize=900)

    
    if command == "Data Visualization":
        label = tk.Label(right_pane, text="Data Visualization Pane", font=("Arial", 14))
        label.pack(pady=10)
    elif command == "APA Citation Generator":
        label = tk.Label(right_pane, text="APA Citation Generator Pane", font=("Arial", 14))
        label.pack(pady=10)
    elif command == "Data Summarization":
        label = tk.Label(right_pane, text="Data Summarization Pane", font=("Arial", 14))
        label.pack(pady=10)

        result_widget = tk.Text(right_pane, wrap=tk.WORD, font=("Arial", 12), height=20, width=50)
        result_widget.pack(pady=5)
        result_widget.config(state=tk.DISABLED) 

        
        def summarizer1():
            # Initialize the summarization pipeline
            summarizer = pipeline('summarization')
            result_widget.config(state=tk.NORMAL)
            result_widget.delete(1.0, tk.END)

            # The article to summarize
            article = text.get(1.0 , tk.END)
            # Summarize the article
            summary = summarizer(article, max_length=200, min_length=60, do_sample=False)

            # Print the summary
            result_widget.insert(tk.END, summary[0]['summary_text'])


        
        search = tk.Button(right_pane , text="summarize" , command=summarizer1 , font=('Arial' , 12))
        search.pack()





    elif command == "Keyword Based Search":
        label = tk.Label(right_pane, text="Keyword Based Search Pane", font=("Arial", 14))
        label.pack(pady=10)
        
        label = tk.Label(right_pane , text="Enter the Keyword" , font=('Arial' , 12))
        label.pack()
        entry = tk.Entry(right_pane , font=('Arial',12))
        entry.pack()
        
        result_widget = tk.Text(right_pane, wrap=tk.WORD, font=("Arial", 12), height=20, width=50)
        result_widget.pack(pady=5)
        result_widget.config(state=tk.DISABLED) 

        def search_keyword():
            keyword = entry.get()
            wiki_wiki = wikipediaapi.Wikipedia('MyProjectName (merlin@example.com)', 'en')
            page = wiki_wiki.page(keyword)
            result_widget.config(state=tk.NORMAL)
            result_widget.delete(1.0, tk.END)
            if page.exists():
                text = page.title + page.summary + page.text
                result_text = text[:1000]
                result_widget.insert(tk.END, result_text)
            else:
                result_widget.insert(tk.END, "Page doesn't exist.")
            result_widget.config(state=tk.DISABLED)



        search = tk.Button(right_pane , text="search" , command=search_keyword , font=('Arial' , 12))
        search.pack()

    elif command == "Synonyms and Antonyms":
        label = tk.Label(right_pane, text="Synonyms and Antonyms Pane", font=("Arial", 14))
        label.pack(pady=10)
    elif command == "Translation":
        label = tk.Label(right_pane, text="Translation Pane", font=("Arial", 14))
        label.pack(pady=10)
        
        text_label = tk.Label(right_pane , text="enter the text to translate" , font=('Arial',12))
        text_label.pack()

        text_entry = tk.Entry(right_pane , font=('Arial',12))
        text_entry.pack()

        from_label = tk.Label(right_pane , text="from" , font=('Arial',10))
        from_label.pack()

        from_entry = tk.Entry(right_pane, font=('Arial' , 12))
        from_entry.pack()
        to_label = tk.Label(right_pane , text="to" , font=('Arial',10))
        to_label.pack()
        to_entry = tk.Entry(right_pane, font=('Arial' , 12))
        to_entry.pack()

        def translate():
            result_widget.config(state=tk.NORMAL)
            result_widget.delete(1.0, tk.END)

            url = "https://google-translate1.p.rapidapi.com/language/translate/v2/"
        
            payload = {
                "q": text_entry.get(),
                "source": Language().get_language_code(from_entry.get().capitalize()),
                "target": Language().get_language_code(to_entry.get().capitalize())
            }

            headers = {
                "x-rapidapi-key": "fd973dc78emshd18080919ee0aeap179d6bjsn2ed44a835c1f",
                "x-rapidapi-host": "google-translate1.p.rapidapi.com",
                "Content-Type": "application/x-www-form-urlencoded"
            }

            response = requests.post(url, data=payload, headers=headers)

            if response.status_code == 200:
                # response.encoding = 'utf-8'

                translation = response.json().get('data', {}).get('translations', [])[0].get('translatedText', '')
                result_widget.insert(tk.END , translation)


                # with open("translation.txt", "w", encoding="utf-8") as file:
                #     file.write(translation)

                print("Translation written to translation.txt")
                # print(translation)
            else:
               result_widget.insert(tk.END,  response.text)
            result_widget.config(state=tk.DISABLED)
            
        
        translate = tk.Button(right_pane , text="translate" , command=translate , font=('Arial' , 12))
        translate.pack()

        result_widget = tk.Text(right_pane, wrap=tk.WORD, font=("Arial", 12), height=20, width=50)
        result_widget.pack(pady=5)
        result_widget.config(state=tk.DISABLED)

        

    elif command == "Mathematical Calculation":
        label = tk.Label(right_pane, text="Mathematical Calculation Pane", font=("Arial", 14))
        label.pack(pady=10)
    
    


def change_background_color():
    color = colorchooser.askcolor()[1]
    if color:
        text.config(bg=color)


def change_font_family(family):
    current_font = font.nametofont(text.cget("font"))
    current_font.config(family=family)
    text.config(font=current_font)

def change_font_size(size):
    current_font = font.nametofont(text.cget("font"))
    current_font.config(size=size)
    text.config(font=current_font)

# Setting up the main window
window = tk.Tk()
window.title("SE7EN")
window.geometry("1200x600")

menu_font = font.Font(family="Arial", size=10)

# Setting up the PanedWindow
paned_window = tk.PanedWindow(window, orient=tk.HORIZONTAL)
paned_window.pack(fill=tk.BOTH, expand=1)

# Setting up the Text widget
left_pane = tk.Frame(paned_window)
text = tk.Text(left_pane, undo=True, wrap="word")
text.pack(expand=True, fill='both', padx=10, pady=10)
paned_window.add(left_pane)

# Right pane for functionality
right_pane = tk.Frame(paned_window,width=200)

# Setting up the Menu
menu = tk.Menu(window, font=menu_font)
window.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0, font=menu_font)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=lambda: [new_file(), hide_right_pane()], accelerator="Ctrl+N")
file_menu.add_command(label="Open", command=lambda: [open_file(), hide_right_pane()], accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.quit)

edit_menu = tk.Menu(menu, tearoff=0 , font=menu_font)
menu.add_cascade(label="Edit", menu=edit_menu , font=('Arial' , 20))
edit_menu.add_command(label="Undo", command=undo_action)
edit_menu.add_command(label="Redo", command=redo_action)
edit_menu.add_separator()
edit_menu.add_command(label="Cut", command=cut_text, accelerator="Ctrl+X")
edit_menu.add_command(label="Copy", command=copy_text, accelerator="Ctrl+C")
edit_menu.add_command(label="Paste", command=paste_text, accelerator="Ctrl+V")

format_menu = tk.Menu(menu, tearoff=0 , font=menu_font)
menu.add_cascade(label="Format", menu=format_menu,font=('Arial' , 20))
format_menu.add_command(label="Text Color", command=lambda: [change_text_color(), hide_right_pane()])
format_menu.add_command(label="Bold", command=change_font_style, accelerator="Ctrl+B")

research_menu = tk.Menu(menu, tearoff=0, font=menu_font)
menu.add_cascade(label="Research", menu=research_menu,font=('Arial' , 20))
research_menu.add_command(label="Data Visualization", command=lambda: show_split_functionality("Data Visualization"))
research_menu.add_command(label="APA Citation Generator", command=lambda: show_split_functionality("APA Citation Generator"))
research_menu.add_command(label="Data Summarization", command=lambda: show_split_functionality("Data Summarization"))
research_menu.add_command(label="Keyword Based Search", command=lambda: show_split_functionality("Keyword Based Search"))
research_menu.add_command(label="Synonyms and Antonyms", command=lambda: show_split_functionality("Synonyms and Antonyms"))
research_menu.add_command(label="Translation", command=lambda: show_split_functionality("Translation"))
research_menu.add_command(label="Mathematical Calculation", command=lambda: show_split_functionality("Mathematical Calculation"))

font_family_menu = tk.Menu(menu, tearoff=0, font=menu_font)
menu.add_cascade(label="Font Family", menu=font_family_menu,font=('Arial' , 20))


font_size_menu = tk.Menu(menu, tearoff=0,font=menu_font)
menu.add_cascade(label="Font Size", menu=font_size_menu,font=('Arial' , 20))

bg_menu = tk.Menu(menu , tearoff=0 ,font=menu_font)
menu.add_cascade(label="BG" , menu = bg_menu,font=('Arial' , 20) )
bg_menu.add_command(label="Background color" , command=change_background_color)


font_families = list(font.families())
font_families.sort()

for family in font_families:
    font_family_menu.add_command(label=family, command=lambda f=family: [change_font_family(f), hide_right_pane()])


for size in range(8, 73, 2):
    font_size_menu.add_command(label=str(size), command=lambda s=size: [change_font_size(s), hide_right_pane()])

# Binding keyboard shortcuts
window.bind("<Control-b>", change_font_style)
window.bind("<Control-s>", save_file)
window.bind("<Control-o>", open_file)
window.bind("<Control-n>", new_file)
window.bind("<Control-x>", cut_text)
window.bind("<Control-c>", copy_text)
window.bind("<Control-v>", paste_text)
window.bind("<Control-f>", find_text)
window.bind("<Control-r>", replace_text)


window.mainloop()