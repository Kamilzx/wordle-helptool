import customtkinter as ctk
import tkinter
from collections import Counter
from functools import partial

class Wordle(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        self.title("Wordle Helptool")
        self.geometry("700x640")
        self.resizable(False, False)

        self.background_color      = "#2b2b2b"
        self.neutral_letter_color = "#4d6160"  # 'Neutral' (grayish)
        self.yellow_letter_color  = "#e1b12c"
        self.green_letter_color   = "#10ac84"
        self.text_color           = "white"

        self.entry_colors = {}

        self.words = []
        self.current_list = []

        self.include_entries = []

        self.text_displays = []

        self.setup_ui()

    # ---------- UI Creation ----------
    def setup_ui(self):
        """Create and place all frames, labels, buttons, and text boxes."""
        self.input_frame = ctk.CTkFrame(self, fg_color=self.background_color)
        self.input_frame.pack(side="left", padx=20, pady=20)

        self.word_list_frame = ctk.CTkFrame(self, fg_color=self.background_color)
        self.word_list_frame.pack(side="right", padx=20, pady=20)

        label = ctk.CTkLabel(
            self.input_frame, 
            text="Enter your word guesses",
            text_color="white",
            font=("Helvetica", 14, "bold")
        )
        label.pack(side="top", pady=5)

        for _ in range(6):
            row_entries = self.create_letter_entry(self.input_frame)
            self.include_entries.append(row_entries)

        large_font = ctk.CTkFont(family="Helvetica", size=14, weight="bold")
        small_font = ctk.CTkFont(family="Helvetica", size=10, weight="bold")

        self.load_button = ctk.CTkButton(
            self.input_frame, 
            text="Load Words File",
            command=self.load_file,
            text_color="white",
            fg_color="#3b3b3b",
            font=large_font,
            width=160,
            height=40
        )
        self.load_button.pack(pady=5)

        clear_button = ctk.CTkButton(
            self.input_frame,
            text="Clear",
            command=self.clear_entries,
            text_color="white",
            fg_color="#3b3b3b",
            font=small_font,
            width=100,
            height=30
        )
        clear_button.pack(pady=10)

        for i in range(1, 11):
            row_frame = ctk.CTkFrame(self.word_list_frame, fg_color=self.background_color)
            row_frame.pack(pady=3, fill="x")

            label_num = ctk.CTkLabel(row_frame, text=f"{i}.", width=20,
                                     text_color="white", font=("Helvetica", 17, "bold"))
            label_num.pack(side="left", padx=5)

            tbox = ctk.CTkTextbox(
                row_frame,
                width=150,
                height=40,
                fg_color="#3b3b3b",
                text_color="white",
                font=("Helvetica", 25),
                corner_radius=6
            )
            tbox.pack(side="left", padx=5)
            tbox.configure(state="disabled")
            self.text_displays.append(tbox)

        self.bind("<Button-1>", self.remove_focus)

    def create_letter_entry(self, parent):
        frame = ctk.CTkFrame(parent)
        frame.pack(pady=2)

        entries = []
        
        def handle_trace(var, row_entries, index, *trace_args):
            var.set(var.get().upper())
            self.on_entry_change(var, row_entries, index)

        for i in range(5):
            var = ctk.StringVar()

            cb = partial(handle_trace, var, entries, i)
            var.trace_add("write", cb)

            entry = ctk.CTkEntry(
                frame,
                width=70,
                height=70,
                fg_color=self.neutral_letter_color,
                text_color=self.text_color,
                textvariable=var,
                font=("Helvetica", 30),
                corner_radius=6,
                justify=ctk.CENTER,
                state="disabled"
            )
            self.entry_colors[id(entry)] = self.neutral_letter_color

            entry.bind("<Button-1>",  partial(self.on_entry_click, entry))
            entry.bind("<Up>",  partial(self.on_entry_click, entry))
            entry.bind("<Down>",  partial(self.on_entry_click, entry))
            entry.bind("<space>",  partial(self.on_entry_click, entry))
            entry.bind("<BackSpace>", partial(self.on_backspace, entry))
            entry.bind("<Left>", partial(self.on_left_arrow, entries, i))
            entry.bind("<Right>", partial(self.on_right_arrow, entries, i))
            
            entry.pack(side="left", padx=2)
            entries.append(entry)

        return entries

    def on_entry_change(self, var, row_entries, index):
        """Limit each entry to 1 character; auto-focus next entry."""
        current_value = var.get()
        if len(current_value) > 1:
            if current_value[0].isspace():
                var.set(current_value[1].upper())
            else:
                var.set(current_value[0].upper())
            row_entries[index].configure(textvariable=var)

        if len(var.get()) == 1:
            if index < (len(row_entries) - 1):
                row_entries[index + 1].configure(state="normal")
                row_entries[index + 1].focus()

        self.update_list()

    def on_backspace(self, var, row_entries, index, event):
        """Backspace → jump to previous entry if this one becomes empty."""
        if index > 0 and var.get() == "":
            row_entries[index - 1].focus()
            row_entries[index - 1].configure(state="normal")
        self.update_list()

    def on_left_arrow(self, row_entries, index, event):
        """Left arrow → focus previous entry."""
        if index > 0:
            row_entries[index - 1].focus()

    def on_right_arrow(self, row_entries, index, event):
        """Right arrow → focus next entry."""
        if index < len(row_entries) - 1:
            row_entries[index + 1].focus()

    def on_entry_click(self, entry, event):
        """
        Cycle the fg_color of the CTkEntry among:
          neutral -> yellow -> green -> neutral
        only if there's a character in the entry.
        """
        #entry = event.widget
        text_val = entry.get()

        current_color = self.entry_colors.get(id(entry), self.neutral_letter_color)
        if text_val:
            if current_color == self.neutral_letter_color:
                new_color = self.yellow_letter_color
            elif current_color == self.yellow_letter_color:
                new_color = self.green_letter_color
            elif current_color == self.green_letter_color:
                new_color = self.neutral_letter_color
            else:
                new_color = self.neutral_letter_color

            entry.configure(state="normal")
            entry.configure(fg_color=new_color)
            self.entry_colors[id(entry)] = new_color

        self.update_list()

    def remove_focus(self, event):
        """Remove focus if user clicks outside CTkEntry widgets."""
        if not isinstance(event.widget, tkinter.Entry):
            self.focus_set()

    def load_file(self):
        file_path = ctk.filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not file_path:
            return
        self.words = self.load_words(file_path)
        self.load_button.configure(text_color="lightgreen", text="File Loaded")

        for row in self.include_entries:
            for ent in row:
                ent.configure(state="normal")

        self.update_list()

    def load_words(self, file_path):
        with open(file_path, 'r') as file:
            return [
                w.strip() for w in file
                if len(w.strip()) == 5
                and not any(c.isdigit() or c == ',' for c in w)
            ]

    def clear_entries(self):
        """Clear all entry widgets and reset their fg_color. Also clear text boxes."""
        for row in self.include_entries:
            for ent in row:
                ent.delete(0, "end")
                ent.configure(fg_color=self.neutral_letter_color)
                self.entry_colors[id(ent)] = self.neutral_letter_color

        for tbox in self.text_displays:
            tbox.configure(state="normal")
            tbox.delete("0.0", "end")
            tbox.configure(state="disabled")

        self.update_list()

    def get_letters_from_entries(self, row_entries):
        """Collect non-empty letters from row entries that have the 'neutral' fg_color."""
        letters = []
        for entry in row_entries:
            val = entry.get().strip().lower()
            if val and self.entry_colors.get(id(entry)) == self.neutral_letter_color:
                letters.append(val)
        return letters

    def find_most_popular_letters(self, words):
        all_letters = [letter for word in words for letter in set(word)]
        most_common = Counter(all_letters).most_common(10)
        return [letter for letter, _ in most_common]

    def score_word(self, word, popular_letters):
        return len(set(word) & set(popular_letters))

    def sort_words_by_score(self, words, popular_letters):
        words_scored = [(w, self.score_word(w, popular_letters)) for w in words]
        sorted_words = sorted(words_scored, key=lambda x: (-x[1], x[0]))
        return [w for w, _ in sorted_words]

    def find_top_words_by_popular_letters(self, word_list, max_words=10):
        popular_letters = self.find_most_popular_letters(word_list)
        sorted_list = self.sort_words_by_score(word_list, popular_letters)
        return sorted_list[:max_words]

    def update_list(self):
        global current_list
        green_yellow1, green_yellow2, green_yellow3, green_yellow4, green_yellow5, green_yellow6 = [], [], [], [], [], []
        filtered_words = []
        true_excluded = []

        included_letters1 = [entry.get().strip().lower() for entry in self.include_entries[0]]
        included_letters2 = [entry.get().strip().lower() for entry in self.include_entries[1]]
        included_letters3 = [entry.get().strip().lower() for entry in self.include_entries[2]]
        included_letters4 = [entry.get().strip().lower() for entry in self.include_entries[3]]
        included_letters5 = [entry.get().strip().lower() for entry in self.include_entries[4]]
        included_letters6 = [entry.get().strip().lower() for entry in self.include_entries[5]]

        excluded_letters1 = set(self.get_letters_from_entries(self.include_entries[0]))
        excluded_letters2 = set(self.get_letters_from_entries(self.include_entries[1]))
        excluded_letters3 = set(self.get_letters_from_entries(self.include_entries[2]))
        excluded_letters4 = set(self.get_letters_from_entries(self.include_entries[3]))
        excluded_letters5 = set(self.get_letters_from_entries(self.include_entries[4]))
        excluded_letters6 = set(self.get_letters_from_entries(self.include_entries[5]))

        # Get all Green and Yellow letters
        for (include_entries, included_letters, green_yellow) in zip((self.include_entries[0], self.include_entries[1], self.include_entries[2], self.include_entries[3], self.include_entries[4], self.include_entries[5]),
                                                    (included_letters1, included_letters2, included_letters3, included_letters4, included_letters5, included_letters6),
                                                    (green_yellow1, green_yellow2, green_yellow3, green_yellow4, green_yellow5, green_yellow6)):
            for index, letter in enumerate(included_letters):
                if self.entry_colors[id(include_entries[index])] == self.green_letter_color or self.entry_colors[id(include_entries[index])] == self.yellow_letter_color:
                    green_yellow.append(letter)

        # Filter words based on excluded letters
        for excluded_letters in (excluded_letters1, excluded_letters2, excluded_letters3, excluded_letters4, excluded_letters5, excluded_letters6):
            for letter in excluded_letters:
                if letter not in green_yellow1 and letter not in green_yellow2 and letter not in green_yellow3 and letter not in green_yellow4 and letter not in green_yellow5 and letter not in green_yellow6:
                    true_excluded.append(letter)
        filtered_words = [word for word in self.words if not any(letter in word for letter in true_excluded)]

        # Filter words based on included letters (specific positions)
        for (include_entries, included_letters) in zip((self.include_entries[0], self.include_entries[1], self.include_entries[2], self.include_entries[3], self.include_entries[4], self.include_entries[5]),
                                                    (included_letters1, included_letters2, included_letters3, included_letters4, included_letters5, included_letters6)):
            for index, letter in enumerate(included_letters):
                if self.entry_colors[id(include_entries[index])] == self.yellow_letter_color:
                    if letter:  # If a certain letter is specified and is yellow
                        count = max(green_yellow1.count(letter), green_yellow2.count(letter), green_yellow3.count(letter), green_yellow4.count(letter), green_yellow5.count(letter), green_yellow6.count(letter))
                        filtered_words = [word for word in filtered_words if letter in word and (word.count(letter) >= count)]
                        filtered_words = [word for word in filtered_words if not word[index] == letter]
                if self.entry_colors[id(include_entries[index])] == self.green_letter_color:
                    if letter:
                        filtered_words = [word for word in filtered_words if word[index] == letter]

        self.current_list = filtered_words
        self.print_list()

    def print_list(self):
        """Print top 10 candidate words in the text boxes on the right."""
        for tbox in self.text_displays:
            tbox.configure(state="normal")
            tbox.delete("0.0", "end")
            tbox.configure(state="disabled")

        if not self.current_list:
            return

        top_words = self.find_top_words_by_popular_letters(self.current_list.copy(), max_words=10)

        for i, word in enumerate(top_words):
            if i >= len(self.text_displays):
                break
            tbox = self.text_displays[i]
            tbox.configure(state="normal")
            tbox.delete("0.0", "end")
            tbox.insert("end", word.upper())
            tbox.configure(state="disabled")

if __name__ == "__main__":
    app = Wordle()
    app.mainloop()
