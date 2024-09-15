import os
import datetime
import subprocess
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import util

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title("Face Recognition System")
        self.main_window.geometry("1200x600+350+100")
        self.main_window.configure(bg="#f0f0f0")

        # Title Label
        self.title_label = tk.Label(self.main_window, text="Face Recognition System", font=("Arial", 24), bg="#f0f0f0")
        self.title_label.pack(pady=20)

        # Webcam Display
        self.webcam_frame = tk.Frame(self.main_window, bg="#ffffff", borderwidth=2, relief="solid")
        self.webcam_frame.place(x=10, y=60, width=700, height=500)
        self.webcam_label = util.get_image_label(self.webcam_frame)
        self.webcam_label.pack(fill="both", expand=True)

        self.add_webcam(self.webcam_label)

        # Buttons
        button_frame = tk.Frame(self.main_window, bg="#f0f0f0")
        button_frame.place(x=750, y=60, width=400, height=500)

        self.login_button = util.get_button(button_frame, 'Login', 'green', self.login)
        self.login_button.pack(pady=10, fill='x')

        self.register_button = util.get_button(button_frame, 'Register New User', 'gray', self.register_new_user, fg='black')
        self.register_button.pack(pady=10, fill='x')

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        self._label.after(20, self.process_webcam)

    def login(self):
        unknown_img_path = './.tmp.jpg'
        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)

        try:
            output = subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path])
            name = output.decode().split(',')[1].strip()
            if name in ['unknown_person', 'no_person_found']:
                util.msg_box('Oops...', 'Unknown user. Please register or try again.')
            else:
                util.msg_box('Welcome back', f'Welcome, {name}.')
                with open(self.log_path, 'a') as f:
                    f.write(f'{name},{datetime.datetime.now()}\n')
        except subprocess.CalledProcessError:
            util.msg_box('Error', 'Face recognition failed. Please try again.')

        os.remove(unknown_img_path)

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.title("Register New User")
        self.register_new_user_window.geometry("600x400+400+200")
        self.register_new_user_window.configure(bg="#f0f0f0")

        # Register Title Label
        self.register_title_label = tk.Label(self.register_new_user_window, text="Register New User", font=("Arial", 18), bg="#f0f0f0")
        self.register_title_label.pack(pady=10)

        # Capture Display
        self.capture_frame = tk.Frame(self.register_new_user_window, bg="#ffffff", borderwidth=2, relief="solid")
        self.capture_frame.pack(pady=10, padx=10, fill='both', expand=True)
        self.capture_label = util.get_image_label(self.capture_frame)
        self.capture_label.pack(fill="both", expand=True)

        self.add_img_to_label(self.capture_label)

        # User Entry
        entry_frame = tk.Frame(self.register_new_user_window, bg="#f0f0f0")
        entry_frame.pack(pady=10)

        self.text_label_register_new_user = util.get_text_label(entry_frame, "Please enter username:")
        self.text_label_register_new_user.pack(pady=5)

        self.entry_text_new_user = util.get_entry_text(entry_frame)
        self.entry_text_new_user.pack(pady=5)

        # Buttons
        button_frame = tk.Frame(self.register_new_user_window, bg="#f0f0f0")
        button_frame.pack(pady=10)

        self.accept_button_register_new_user_window = util.get_button(button_frame, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.pack(side='left', padx=10)

        self.try_again_button_register_new_user_window = util.get_button(button_frame, 'Try Again', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.pack(side='right', padx=10)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def accept_register_new_user(self):
        name = self.entry_text_new_user.get().strip()
        if not name:
            util.msg_box("Error", "Username cannot be empty!")
            return

        file_path = os.path.join(self.db_dir, f'{name}.jpg')
        if os.path.exists(file_path):
            util.msg_box("Error", "This user is already registered.")
            return

        success = cv2.imwrite(file_path, self.register_new_user_capture)

        if success:
            util.msg_box("Done", "User was registered successfully!")
        else:
            util.msg_box("Error", "Failed to save user image.")

        self.register_new_user_window.destroy()

    def start(self):
        self.main_window.mainloop()

if __name__ == "__main__":
    app = App()
    app.start()
