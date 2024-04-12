import tkinter as tk
from tkinter import filedialog, font as tkfont
from collections import Counter

background_color = "#4d6160"
foreground_color = "white"
green_letter_color = "#10ac84"
yellow_letter_color = "#e1b12c"

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
    return [entry.get().strip().lower() for entry in entries if entry.get().strip() and entry.cget("bg") == background_color]

def on_entry_change(var, entries, index):
    """Limit the entry widget to only one character and handle focus change."""
    current_value = var.get()
    # Ensure only the first character is kept, discarding any additional input
    if len(current_value) > 1:
        if current_value[0] == " ":
            var.set(current_value[1])
        else:
            var.set(current_value[0])
    # Check if the textbox was previously empty before the current input was registered
    # This prevents refocusing when editing the existing character
    if len(current_value) == 1:
        if index < (len(entries) - 1):  # Make sure this is not the last textbox
            entries[index + 1].config(state=tk.NORMAL)
            entries[index + 1].focus()
    update_list()

def on_backspace(var, entries, index):
    """Handle the backspace key event to shift focus to the previous entry if current is empty."""
    current_value = var.get()
    if index > 0 and current_value == "":  # Check if current entry is empty
        entries[index - 1].focus()  # Focus the previous entry
        entries[index - 1].config(state=tk.NORMAL)
    update_list()

def on_left_arrow(entries, index):
    """Handle the left arrow key event to shift focus to the previous entry."""
    if index > 0:
        entries[index - 1].focus()

def on_right_arrow(entries, index):
    """Handle the right arrow key event to shift focus to the next entry."""
    if index < len(entries) - 1:
        entries[index + 1].focus()

def update_list():
    global current_list
    green_yellow1, green_yellow2, green_yellow3, green_yellow4, green_yellow5, green_yellow6 = [], [], [], [], [], []
    filtered_words = []
    true_excluded = []

    included_letters1 = [entry.get().strip().lower() for entry in include_entries1]
    included_letters2 = [entry.get().strip().lower() for entry in include_entries2]
    included_letters3 = [entry.get().strip().lower() for entry in include_entries3]
    included_letters4 = [entry.get().strip().lower() for entry in include_entries4]
    included_letters5 = [entry.get().strip().lower() for entry in include_entries5]
    included_letters6 = [entry.get().strip().lower() for entry in include_entries6]

    excluded_letters1 = set(get_letters_from_entries(include_entries1))
    excluded_letters2 = set(get_letters_from_entries(include_entries2))
    excluded_letters3 = set(get_letters_from_entries(include_entries3))
    excluded_letters4 = set(get_letters_from_entries(include_entries4))
    excluded_letters5 = set(get_letters_from_entries(include_entries5))
    excluded_letters6 = set(get_letters_from_entries(include_entries6))

    # Get all Green and Yellow letters
    for (include_entries, included_letters, green_yellow) in zip((include_entries1, include_entries2, include_entries3, include_entries4, include_entries5, include_entries6),
                                                   (included_letters1, included_letters2, included_letters3, included_letters4, included_letters5, included_letters6),
                                                   (green_yellow1, green_yellow2, green_yellow3, green_yellow4, green_yellow5, green_yellow6)):
        for index, letter in enumerate(included_letters):
            if include_entries[index].cget("bg") == green_letter_color or include_entries[index].cget("bg") == yellow_letter_color:
                green_yellow.append(letter)

    # Filter words based on excluded letters
    for excluded_letters in (excluded_letters1, excluded_letters2, excluded_letters3, excluded_letters4, excluded_letters5, excluded_letters6):
        for letter in excluded_letters:
            if letter not in green_yellow1 and letter not in green_yellow2 and letter not in green_yellow3 and letter not in green_yellow4 and letter not in green_yellow5 and letter not in green_yellow6:
                true_excluded.append(letter)
    filtered_words = [word for word in words if not any(letter in word for letter in true_excluded)]

    # Filter words based on included letters (specific positions)
    for (include_entries, included_letters) in zip((include_entries1, include_entries2, include_entries3, include_entries4, include_entries5, include_entries6),
                                                   (included_letters1, included_letters2, included_letters3, included_letters4, included_letters5, included_letters6)):
        for index, letter in enumerate(included_letters):
            if include_entries[index].cget("bg") == yellow_letter_color:
                if letter:  # If a certain letter is specified and is yellow
                    count = max(green_yellow1.count(letter), green_yellow2.count(letter), green_yellow3.count(letter), green_yellow4.count(letter), green_yellow5.count(letter), green_yellow6.count(letter))
                    filtered_words = [word for word in filtered_words if letter in word and (word.count(letter) >= count)]
                    filtered_words = [word for word in filtered_words if not word[index] == letter]
            if include_entries[index].cget("bg") == green_letter_color:
                if letter:
                    filtered_words = [word for word in filtered_words if word[index] == letter]

    current_list = filtered_words
    print_list()


def find_top_words_by_popular_letters(words, max_words=10):
    """Find words that contain the most of the most popular letters."""
    popular_letters = find_most_popular_letters(current_list)
    words = sort_words_by_score(current_list, popular_letters)[:max_words]

    return words[:max_words]

def print_list():
    if not current_list:
        print("The list is empty. Apply filters first.")
    top_words = find_top_words_by_popular_letters(current_list.copy(), max_words=10)
    # Clear previous content in all text widgets
    for text in text_displays:
        text.config(state=tk.NORMAL)  # Temporarily enable widget to modify it
        text.delete('1.0', tk.END)
    # Fill the text widgets with top words, up to 10
    for i, word in enumerate(top_words):
        text_displays[i].insert(tk.END, word.upper())
        text_displays[i].config(state=tk.DISABLED)  # Disable widget to prevent user input

def remove_focus(event):
    """Remove focus from Entry widgets."""
    if not isinstance(event.widget, tk.Entry):
        root.focus_set()

def create_letter_entry(parent):
    """Create a frame with a label and entry widgets for single letters."""
    frame = tk.Frame(parent)
    entries = []
    for i in range(5):
        var = tk.StringVar()
        # Attach the trace method to the StringVar
        var.trace_add('write', lambda name, index, mode, var=var, i=i: on_entry_change(var, entries, i))
        var.trace_add('write', lambda name, index, mode, var=var, i=i: var.set(var.get().upper()))  # Convert text to uppercase
        entry = tk.Entry(frame, width=2, font=('Helvetica', 24), textvariable=var, state=tk.DISABLED, justify=tk.CENTER)
        entry.bind("<Button-1>", on_entry_click)  # Left mouse color change
        entry.bind("<Up>", on_entry_click)  # Up arrow color change
        entry.bind("<Down>", on_entry_click)  # Down arrow color change
        entry.bind("<space>", on_entry_click)  # Space color change
        entry.bind("<BackSpace>", lambda e, entries=entries, i=i, var=var: on_backspace(var, entries, i))  # Bind backspace event
        entry.bind("<Left>", lambda e, entries=entries, i=i: on_left_arrow(entries, i))  # Left arrow
        entry.bind("<Right>", lambda e, entries=entries, i=i: on_right_arrow(entries, i))  # Right arrow
        entry.pack(side=tk.LEFT, padx=2)
        entries.append(entry)
    frame.pack(pady=2)
    return entries

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not file_path:
        return
    global words
    words = load_words(file_path)
    load_button.config(foreground='lightgreen')  # Change button color to green
    for include_entries in (include_entries1, include_entries2, include_entries3, include_entries4, include_entries5, include_entries6):
        for entry in include_entries:
            entry.config(state=tk.NORMAL)
    load_button.configure(text="File Loaded")
    update_list()

def on_entry_click(event):
    """Change background color of the Entry widget."""
    entry = event.widget
    current_color = entry.cget("bg")
    text = entry.get()
    if text:  # Check if there is text in the Entry widget
        if current_color == background_color:
            event.widget.config(bg=yellow_letter_color)
    if current_color == yellow_letter_color:
        event.widget.config(bg=green_letter_color)
    elif current_color == green_letter_color:
        event.widget.config(bg=background_color)
    update_list()
        

def clear_entries():
    """Function to clear the contents of the entry widgets."""
    for include_entries in (include_entries1, include_entries2, include_entries3, include_entries4, include_entries5, include_entries6):
        for entry in include_entries:
            entry.delete(0, tk.END)
            entry.config(bg=background_color)
    for text in text_displays:
        text.config(state=tk.NORMAL)  # Temporarily enable widget to modify it
        text.delete('1.0', tk.END)
        text.config(state=tk.DISABLED)
    update_list()

words = []
current_list = []

root = tk.Tk()
root.title("Wordle Cheat")
root.geometry("500x420")  # Width x Height
root.resizable(False, False)
root.config(bg=background_color)
root.option_add('*Foreground', foreground_color)
root.option_add('*Background', background_color)

# Main frame for input controls
input_frame = tk.Frame(root)
input_frame.pack(side=tk.LEFT, padx=20, pady=20)

# Main frame for the word list
word_list_frame = tk.Frame(root)
word_list_frame.pack(side=tk.RIGHT, padx=20, pady=20)

# Create entries for include and exclude letters with labels
label = tk.Label(input_frame, text="Enter your word", font=('Helvetica', 10, 'bold'))
label.pack(side=tk.TOP)
include_entries1 = create_letter_entry(input_frame)
include_entries2 = create_letter_entry(input_frame)
include_entries3 = create_letter_entry(input_frame)
include_entries4 = create_letter_entry(input_frame)
include_entries5 = create_letter_entry(input_frame)
include_entries6 = create_letter_entry(input_frame)

large_font = tkfont.Font(family="Helvetica", size=14, weight="bold")
small_font = tkfont.Font(family="Helvetica", size=10, weight="bold")

load_button = tk.Button(input_frame, text="Load Words File", command=load_file, font=large_font, width=20, height=2, relief="flat", foreground=foreground_color, background=background_color)
load_button.pack(pady=2)

# Create frames for include and exclude entries
frame_include = tk.Frame(root)
frame_include.pack(pady=5)
frame_exclude = tk.Frame(root)
frame_exclude.pack(pady=5)

clear_button = tk.Button(input_frame, text="Clear", command=clear_entries, font=small_font, width=10, height=2, relief="flat", foreground=foreground_color, background=background_color)
clear_button.pack(pady=5)

# Assuming 'root' is your Tk window instance
text_displays = []  # List to store the text widgets
for i in range(1, 11):
    frame = tk.Frame(word_list_frame)
    # Set label width sufficiently to accommodate "10." with some padding.
    label = tk.Label(frame, text=f"{i}.", font=('Helvetica', 10, 'bold'), width=4, background=background_color)
    label.pack(side=tk.LEFT)
    text = tk.Text(frame, width=8, height=1, font=('Helvetica', 14), state="disabled")
    text.pack(side=tk.LEFT, padx=5)
    frame.pack(pady=4)
    text_displays.append(text)

# Bind click event to remove focus from Entry widgets
root.bind("<Button-1>", remove_focus)

root.mainloop()

