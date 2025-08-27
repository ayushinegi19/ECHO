import tkinter as tk
from tkinter import scrolledtext, ttk, PhotoImage
import threading
import time
import speech_recognition as sr
import datetime
from speech_utils import speak, set_language
from commands import process_command
from PIL import Image, ImageTk
import os

class EchoAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Echo Voice Assistant")
        self.root.geometry("900x700")  # Increased window size
        self.root.configure(bg="#f0f2f5")  # Lighter background like WhatsApp

        # Set theme and styling
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Arial', 13), background='#128C7E', foreground='white', padding=10)  # WhatsApp green
        self.style.configure('TLabel', font=('Arial', 14), background='#f0f2f5', foreground='#075E54')  # WhatsApp dark green
        self.style.configure('TFrame', background='#f0f2f5')
        self.style.configure('Header.TFrame', background='#075E54')  # WhatsApp header green

        # Variables
        self.current_status = tk.StringVar(value="Idle")
        self.current_language = tk.StringVar(value="English")
        self.listening_active = False
        self.recognizer = sr.Recognizer()

        # Create main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # Create frames
        self.create_header_frame(main_container)
        self.create_chat_frame(main_container)
        self.create_control_frame(main_container)

        # Start time update
        self.update_time()

        # Welcome message
        self.add_assistant_message("Hello! I'm Echo, your voice assistant. Click 'Start Listening' to begin.")
        # Print welcome message to console
        print("Echo: Hello! I'm Echo, your voice assistant. Click 'Start Listening' to begin.")

    def create_header_frame(self, parent):
        header_frame = ttk.Frame(parent, style='Header.TFrame')
        header_frame.pack(fill=tk.X, padx=0, pady=0)

        # Try to load logo
        try:
            # Check if logo exists, otherwise use a colored block
            if os.path.exists("echo_logo.png"):
                logo_img = Image.open("echo_logo.png")
                logo_img = logo_img.resize((60, 60))
                self.logo = ImageTk.PhotoImage(logo_img)
                logo_label = ttk.Label(header_frame, image=self.logo, background='#075E54')
                logo_label.pack(side=tk.LEFT, padx=15, pady=10)
            else:
                # Create a colored circle as placeholder
                logo_label = tk.Canvas(header_frame, width=60, height=60, bg="#075E54", highlightthickness=0)
                logo_label.create_oval(5, 5, 55, 55, fill="#128C7E", outline="")
                logo_label.create_text(30, 30, text="E", fill="white", font=('Arial', 22, 'bold'))
                logo_label.pack(side=tk.LEFT, padx=15, pady=10)

        except Exception as e:
            print(f"Logo error: {e}")
            # Text-based logo fallback
            logo_label = ttk.Label(header_frame, text="ECHO", font=('Arial', 32, 'bold'), foreground='white', background='#075E54')
            logo_label.pack(side=tk.LEFT, padx=15, pady=10)

        # Title and status
        title_frame = ttk.Frame(header_frame, style='Header.TFrame')
        title_frame.pack(side=tk.LEFT, padx=10, pady=10)

        title_label = ttk.Label(title_frame, text="Echo Assistant", font=('Arial', 20, 'bold'), foreground='white', background='#075E54')
        title_label.pack(anchor='w')

        status_frame = ttk.Frame(title_frame, style='Header.TFrame')
        status_frame.pack(fill=tk.X, pady=5, anchor='w')

        status_label = ttk.Label(status_frame, text="Status:", foreground='#dcf8c6', background='#075E54', font=('Arial', 12))
        status_label.pack(side=tk.LEFT)

        status_value = ttk.Label(status_frame, textvariable=self.current_status, foreground='white', background='#075E54', font=('Arial', 12))
        status_value.pack(side=tk.LEFT, padx=5)

        # Language selector and time
        info_frame = ttk.Frame(header_frame, style='Header.TFrame')
        info_frame.pack(side=tk.RIGHT, padx=20, pady=10)

        # Language dropdown
        lang_frame = ttk.Frame(info_frame, style='Header.TFrame')
        lang_frame.pack(anchor='e', pady=2)

        lang_label = ttk.Label(lang_frame, text="Language:", foreground='#dcf8c6', background='#075E54', font=('Arial', 12))
        lang_label.pack(side=tk.LEFT)

        lang_options = ["English", "Hindi", "French"]
        self.lang_dropdown = ttk.Combobox(lang_frame, textvariable=self.current_language, values=lang_options, width=10, font=('Arial', 12))
        self.lang_dropdown.pack(side=tk.LEFT, padx=5)
        self.lang_dropdown.bind("<<ComboboxSelected>>", self.change_language)

        # Time display
        self.time_label = ttk.Label(info_frame, text="", foreground='white', background='#075E54', font=('Arial', 12))
        self.time_label.pack(anchor='e', pady=2)

    def create_chat_frame(self, parent):
        chat_container = ttk.Frame(parent)
        chat_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(chat_container, width=80, height=20,
                                                        font=('Arial', 14), wrap=tk.WORD,
                                                        bg="#ffffff", fg="#000000",
                                                        insertbackground="#128C7E",
                                                        selectbackground="#128C7E",
                                                        padx=15, pady=15)
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)

        # Custom scrollbar styling
        self.chat_display.vbar.config(width=16)

        # Entry frame
        input_frame = ttk.Frame(chat_container)
        input_frame.pack(fill=tk.X, pady=(10, 0))

        self.user_input = ttk.Entry(input_frame, font=('Arial', 14), width=50)
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=8)
        self.user_input.bind("<Return>", self.send_text_input)

        # Styled send button
        send_button = tk.Button(input_frame, text="Send", font=('Arial', 13, 'bold'),
                                    bg="#128C7E", fg="white", relief=tk.FLAT,
                                    command=self.send_text_input, padx=20, pady=8)
        send_button.pack(side=tk.RIGHT)

    def create_control_frame(self, parent):
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=15, pady=(5, 15))

        # Control buttons - increased size and spacing
        listen_button = tk.Button(control_frame, text="Start Listening", font=('Arial', 13, 'bold'),
                                     bg="#128C7E", fg="white", relief=tk.FLAT,
                                     command=self.toggle_listening, padx=20, pady=12)
        listen_button.pack(side=tk.LEFT, padx=10)

        self.listen_button = listen_button

        stop_button = tk.Button(control_frame, text="Stop", font=('Arial', 13, 'bold'),
                                  bg="#e74c3c", fg="white", relief=tk.FLAT,
                                  command=self.stop_listening, padx=20, pady=12)
        stop_button.pack(side=tk.LEFT, padx=10)

        clear_button = tk.Button(control_frame, text="Clear Chat", font=('Arial', 13, 'bold'),
                                   bg="#3498db", fg="white", relief=tk.FLAT,
                                   command=self.clear_chat, padx=20, pady=12)
        clear_button.pack(side=tk.LEFT, padx=10)

        exit_button = tk.Button(control_frame, text="Exit", font=('Arial', 13, 'bold'),
                                 bg="#95a5a6", fg="white", relief=tk.FLAT,
                                 command=self.root.destroy, padx=20, pady=12)
        exit_button.pack(side=tk.RIGHT, padx=10)

    def update_time(self):
        current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
        current_date = datetime.datetime.now().strftime("%a, %b %d, %Y")
        self.time_label.config(text=f"{current_date}\n{current_time}")
        self.root.after(1000, self.update_time)

    def format_message_bubble(self, message, sender):
        """Format a message in a chat bubble style"""
        if sender == "user":
            return f"  {message}  "
        else:
            return f"  {message}  "

    def add_user_message(self, message):
        self.chat_display.config(state=tk.NORMAL)

        # Create user bubble tag
        self.chat_display.tag_configure("user_bubble",
                                        background="#dcf8c6",  # Light green bubble
                                        foreground="#000000",
                                        font=('Arial', 14),
                                        lmargin1=300,  # Indent from left to right-align
                                        lmargin2=300,
                                        rmargin=15,
                                        spacing1=10,  # Space above paragraph
                                        spacing3=10)  # Space below paragraph

        # Create user name tag
        self.chat_display.tag_configure("user_name",
                                        foreground="#075E54",
                                        font=('Arial', 12, 'bold'))

        # Insert the message
        self.chat_display.insert(tk.END, "\n", "spacing")
        self.chat_display.insert(tk.END, "You:", "user_name")
        self.chat_display.insert(tk.END, "\n", "spacing")
        self.chat_display.insert(tk.END, self.format_message_bubble(message, "user"), "user_bubble")
        self.chat_display.insert(tk.END, "\n", "spacing")

        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

        # Print user message to console
        print(f"You: {message}")

    def add_assistant_message(self, message):
        """Add an assistant message to the chat display with WhatsApp style"""
        # Ensure this runs on the main thread
        if threading.current_thread() != threading.main_thread():
            self.root.after(0, lambda: self.add_assistant_message(message))
            return

        # Now we're on the main thread
        self.chat_display.config(state=tk.NORMAL)

        # Create assistant bubble tag
        self.chat_display.tag_configure("assistant_bubble",
                                        background="#ffffff",  # White bubble
                                        foreground="#000000",
                                        font=('Arial', 14),
                                        lmargin1=15,  # Left-aligned
                                        lmargin2=15,
                                        rmargin=300,  # Limit right side
                                        spacing1=10,  # Space above paragraph
                                        spacing3=10)  # Space below paragraph

        # Create assistant name tag
        self.chat_display.tag_configure("assistant_name",
                                        foreground="#128C7E",
                                        font=('Arial', 12, 'bold'))

        # Insert the message
        self.chat_display.insert(tk.END, "\n", "spacing")
        self.chat_display.insert(tk.END, "Echo:", "assistant_name")
        self.chat_display.insert(tk.END, "\n", "spacing")
        self.chat_display.insert(tk.END, self.format_message_bubble(message, "assistant"), "assistant_bubble")
        self.chat_display.insert(tk.END, "\n", "spacing")

        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

        # Print assistant message to console
        print(f"Echo: {message}")

    def add_system_message(self, message):
        """Add a system message to the chat display"""
        # Ensure this runs on the main thread
        if threading.current_thread() != threading.main_thread():
            self.root.after(0, lambda: self.add_system_message(message))
            return

        self.chat_display.config(state=tk.NORMAL)

        # Create system message tag
        self.chat_display.tag_configure("system_message",
                                        foreground="#7F8C8D",
                                        font=('Arial', 12, 'italic'),
                                        justify='center')

        # Insert with center alignment
        self.chat_display.insert(tk.END, "\n", "spacing")
        self.chat_display.insert(tk.END, f"  {message}  ", "system_message")
        self.chat_display.insert(tk.END, "\n", "spacing")

        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

        # Print system message to console
        print(f"System: {message}")

    def send_text_input(self, event=None):
        """Process text input from the entry widget"""
        message = self.user_input.get().strip()
        if message:
            self.add_user_message(message)
            self.user_input.delete(0, tk.END)

            # Process command in a separate thread
            threading.Thread(target=self.process_command_thread, args=(message,), daemon=True).start()

    def process_command_thread(self, command):
        """Process command in a separate thread"""
        # Update status
        self.current_status.set("Processing...")
        print(f"Status: Processing...")
        response = process_command(command)
        if response:
            self.add_assistant_message(response)

        try:
            # Process the command - responses will be shown via our patched speak function
            pass  # process_command(command) is already called above
        except Exception as e:
            error_msg = f"Error: {e}"
            self.add_system_message(error_msg)
            print(error_msg)
        finally:
            # Update status
            self.current_status.set("Idle")
            print(f"Status: Idle")

    def toggle_listening(self):
        """Toggle the listening state"""
        if not self.listening_active:
            self.listening_active = True
            self.current_status.set("Listening...")
            print(f"Status: Listening...")
            self.listen_button.config(text="Stop Listening", bg="#e74c3c")  # Red when active

            # Start listening in a separate thread
            threading.Thread(target=self.listen_for_commands, daemon=True).start()
        else:
            self.stop_listening()

    def stop_listening(self):
        """Stop the listening process"""
        self.listening_active = False
        self.current_status.set("Idle")
        print(f"Status: Idle")
        self.listen_button.config(text="Start Listening", bg="#128C7E")  # Back to green

    def listen_for_commands(self):
        """Listen for voice commands"""
        self.add_system_message("Listening for commands... Say something!")

        with sr.Microphone() as source:
            while self.listening_active:
                try:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=5)

                    # Update status
                    self.current_status.set("Processing speech...")
                    print(f"Status: Processing speech...")
                    self.add_system_message("Processing speech...")

                    # Recognize speech
                    command = self.recognizer.recognize_google(audio).lower()

                    # Display what was heard
                    self.add_user_message(command)

                    # Process command in a separate thread
                    threading.Thread(target=self.process_command_thread, args=(command,), daemon=True).start()

                    # Small pause between listening cycles
                    time.sleep(1)

                except sr.WaitTimeoutError:
                    pass
                except sr.UnknownValueError:
                    error_msg = "Sorry, I didn't catch that."
                    self.add_system_message(error_msg)
                    print(f"System: {error_msg}")
                except sr.RequestError:
                    error_msg = "Speech recognition service unavailable."
                    self.add_system_message(error_msg)
                    print(f"System: {error_msg}")
                except Exception as e:
                    error_msg = f"Error: {e}"
                    self.add_system_message(error_msg)
                    print(f"System: {error_msg}")

                # Update status if still active
                if self.listening_active:
                    self.current_status.set("Listening...")
                    print(f"Status: Listening...")

    def change_language(self, event):
        """Change the language based on the dropdown selection"""
        language = self.current_language.get()

        if language == "English":
            set_language("en")
        elif language == "Hindi":
            set_language("hi")
        elif language == "French":
            set_language("fr")

        message = f"Language changed to {language}"
        self.add_system_message(message)
        print(f"System: {message}")

    def clear_chat(self):
        """Clear the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.add_assistant_message("Chat cleared. How can I help you?")
        print("System: Chat cleared")
        print("Echo: Chat cleared. How can I help you?")


if __name__ == "__main__":
    root = tk.Tk()
    app = EchoAssistantGUI(root)
    root.mainloop()