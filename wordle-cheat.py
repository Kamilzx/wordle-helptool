import tkinter as tk
from tkinter import filedialog, messagebox, font as tkfont
from collections import Counter

def find_most_popular_letters(words):
    all_letters = [letter for word in words for letter in set(word)]
    most_common = Counter(all_letters).most_common(10)
    return [letter for letter, count in most_common]

def score_word(word, popular_letters):
    return len(set(word) & set(popular_letters))

def sort_words_by_score(words, popular_letters):
    words_scored = [(word, score_word(word, popular_letters)) for word in words]
    # Sort words by their score, then alphabetically
    sorted_words = sorted(words_scored, key=lambda x: (-x[1], x[0]))
    return [word for word, score in sorted_words]

def load_words(file_path):
    with open(file_path, 'r') as file:
        # Filter words to exclude any that contain digits or commas
        return [word.strip() for word in file if len(word.strip()) == 5 and not any(char.isdigit() or char == ',' for char in word)]

def get_letters_from_entries(entries):
    """Collect non-empty letters from entry widgets."""
    return [entry.get().strip().lower() for entry in entries if entry.get().strip()]

def on_entry_change(var, indx, mode):
    """Limit the entry widget to only one character."""
    current_value = var.get()
    if len(current_value) > 1:
        var.set(current_value[:1])

def update_list():
    included_letters = [entry.get().strip().lower() for entry in include_entries]
    included_letters2 = [entry.get().strip().lower() for entry in include_entries2]
    included_letters3 = [entry.get().strip().lower() for entry in include_entries3]
    excluded_letters = set(get_letters_from_entries(exclude_entries))
    certain_letters = [entry.get().strip().lower() for entry in certain_entries]
    
    # Filter words based on excluded letters
    filtered_words = [word for word in words if not any(letter in word for letter in excluded_letters)]
    
    # Filter words based on included letters (anywhere in the word)
    if included_letters:
        filtered_words = [word for word in filtered_words if all(letter in word for letter in included_letters)]
        # Filter words based on included letters (specific positions)
        for index, letter in enumerate(included_letters):
            if letter:  # If a certain letter is specified
                filtered_words = [word for word in filtered_words if not word[index] == letter]

    # Filter words based on included letters (anywhere in the word)
    if included_letters2:
        filtered_words = [word for word in filtered_words if all(letter in word for letter in included_letters2)]
        # Filter words based on included letters (specific positions)
        for index, letter in enumerate(included_letters2):
            if letter:  # If a certain letter is specified
                filtered_words = [word for word in filtered_words if not word[index] == letter]

    # Filter words based on included letters (anywhere in the word)
    if included_letters3:
        filtered_words = [word for word in filtered_words if all(letter in word for letter in included_letters3)]
        # Filter words based on included letters (specific positions)
        for index, letter in enumerate(included_letters3):
            if letter:  # If a certain letter is specified
                filtered_words = [word for word in filtered_words if not word[index] == letter]

    # Filter words based on certain letters (specific positions)
    for index, letter in enumerate(certain_letters):
        if letter:  # If a certain letter is specified
            filtered_words = [word for word in filtered_words if word[index] == letter]

    global current_list
    current_list = filtered_words
    print_list()


def find_top_words_by_popular_letters(words, max_words=10):
    """Find words that contain the most of the most popular letters."""
    popular_letters = find_most_popular_letters(current_list)
    words = sort_words_by_score(current_list, popular_letters)[:max_words]

    return words[:max_words]

def print_list():
    if not current_list:
        messagebox.showinfo("Info", "The list is empty. Apply filters first.")
        return
    top_words = find_top_words_by_popular_letters(current_list.copy(), max_words=10)
    # Clear previous content in all text widgets
    for text in text_displays:
        text.config(state=tk.NORMAL)  # Temporarily enable widget to modify it
        text.delete('1.0', tk.END)
    # Fill the text widgets with top words, up to 10
    for i, word in enumerate(top_words):
        text_displays[i].insert(tk.END, word.upper())
        text_displays[i].config(state=tk.DISABLED)  # Disable widget to prevent user input

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not file_path:
        return
    global words
    words = load_words(file_path)
    load_button.config(foreground='lightgreen')  # Change button color to green
    

def create_letter_entry(parent, label_text):
    """Create a frame with a label and entry widgets for single letters."""
    frame = tk.Frame(parent)
    label = tk.Label(frame, text=label_text, font=('Helvetica', 10, 'bold'))
    label.pack(side=tk.TOP)
    entries = []
    for _ in range(5):
        var = tk.StringVar()
        # Attach the trace method to the StringVar
        var.trace_add('write', lambda name, index, mode, var=var: on_entry_change(var, index, mode))
        entry = tk.Entry(frame, width=2, font=('Helvetica', 14), textvariable=var)
        entry.pack(side=tk.LEFT, padx=2)
        entries.append(entry)
    frame.pack(pady=2)
    return entries

def create_letter_entry_inc(parent):
    """Create a frame with a label and entry widgets for single letters."""
    frame = tk.Frame(parent)
    #label = tk.Label(frame, font=('Helvetica', 10, 'bold'))
    #label.pack(side=tk.TOP)
    entries = []
    for _ in range(5):
        var = tk.StringVar()
        # Attach the trace method to the StringVar
        var.trace_add('write', lambda name, index, mode, var=var: on_entry_change(var, index, mode))
        entry = tk.Entry(frame, width=2, font=('Helvetica', 14), textvariable=var)
        entry.pack(side=tk.LEFT, padx=2)
        entries.append(entry)
    frame.pack(pady=2)
    return entries

def create_letter_entry_exc(parent, label_text):
    """Create a frame with a label and entry widgets for single letters."""
    frame = tk.Frame(parent)
    label = tk.Label(frame, text=label_text, font=('Helvetica', 10, 'bold'))
    label.pack(side=tk.TOP)
    entries = []
    for _ in range(8):
        var = tk.StringVar()
        # Attach the trace method to the StringVar
        var.trace_add('write', lambda name, index, mode, var=var: on_entry_change(var, index, mode))
        entry = tk.Entry(frame, width=2, font=('Helvetica', 14), textvariable=var)
        entry.pack(side=tk.LEFT, padx=2)
        entries.append(entry)
    frame.pack(pady=4)
    return entries


words = []
current_list = []

root = tk.Tk()
root.title("Wordle Cheat")
root.geometry("500x470")  # Width x Height
root.resizable(False, False)
root.config(bg='#4d6160')
root.option_add('*Foreground', 'white')
root.option_add('*Background', '#4d6160')

# Main frame for input controls
input_frame = tk.Frame(root)
input_frame.pack(side=tk.LEFT, padx=20, pady=20)

# Main frame for the word list
word_list_frame = tk.Frame(root)
word_list_frame.pack(side=tk.RIGHT, padx=20, pady=20)

# Create entries for certain letters with a label
# Creating entries for "Certain Letters" as an example
certain_entries = create_letter_entry(input_frame, "Certain Letters")

# Create entries for include and exclude letters with labels
include_entries = create_letter_entry(input_frame, "Letters to Include")
include_entries2 = create_letter_entry_inc(input_frame)
include_entries3 = create_letter_entry_inc(input_frame)
exclude_entries = create_letter_entry_exc(input_frame, "Letters to Exclude")

large_font = tkfont.Font(family="Helvetica", size=14, weight="bold")

load_button = tk.Button(input_frame, text="Load Words File", command=load_file, font=large_font, width=20, height=2, relief="flat", foreground="white", background="#4d6160")
load_button.pack(pady=10)

# Create frames for include and exclude entries
frame_include = tk.Frame(root)
frame_include.pack(pady=5)
frame_exclude = tk.Frame(root)
frame_exclude.pack(pady=5)

filter_button = tk.Button(input_frame, text="Apply Filters", command=update_list, font=large_font, width=20, height=2, relief="flat", foreground="white", background="#4d6160")
filter_button.pack(pady=10)

# Assuming 'root' is your Tk window instance
text_displays = []  # List to store the text widgets
for i in range(1, 11):
    frame = tk.Frame(word_list_frame)
    # Set label width sufficiently to accommodate "10." with some padding.
    label = tk.Label(frame, text=f"{i}.", font=('Helvetica', 10, 'bold'), width=4, background="#4d6160")
    label.pack(side=tk.LEFT)
    text = tk.Text(frame, width=8, height=1, font=('Helvetica', 14), state="disabled")
    text.pack(side=tk.LEFT, padx=5)
    frame.pack(pady=4)
    text_displays.append(text)



root.mainloop()

