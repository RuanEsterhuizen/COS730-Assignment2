import time
import tkinter as tk

class UI:
    def __init__(self, submissionController):
        self.sc = submissionController

        self.window = tk.Tk()
        self.window.geometry("600x400")
        self.window.title("COS730 - Assignment 2")

        tk.Label(self.window, text="Intelligent Submission and Review System").pack(pady=15)

        self.data_entry = tk.Entry(self.window, text="Research output in JSON format goes here")
        self.data_entry.pack(pady=15)

        self.output_box = tk.Text(
            self.window,
            height=10,
            width=70
        )
        self.output_box.pack(pady=20)

        tk.Button(self.window, text="Submit for Review", command=self.submit_data).pack(pady=15)

    def run(self):
        self.window.mainloop()

    def submit_data(self):
        from SubmissionController import SubmissionController

        path = "data/" + self.data_entry.get() + ".json"
        try:
            file = open(path, "r")
            data = file.read()
            print("Data: ", data, "\n")

            self.output_box.insert(tk.END, f"Submitted:\n{data}\n\n")

            print("UI: Submitting Data to SubmissionController")

            start = time.time()
            self.sc.submit(data)
            runtime = time.time() - start

            print(f"Runtime: {runtime:.4}s")

        except Exception as e:
            tk.messagebox.showinfo("Error", e)
            print(f"UI: An error occurred: {e}")