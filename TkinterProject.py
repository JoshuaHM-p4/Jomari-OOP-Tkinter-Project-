import datetime
import pickle
from tkinter import *

class Booking:
    """
    A class representing a booking for a cab.

    Attributes:
    - root: The root Tkinter window for the booking application.
    - records: A list to store the booking records.
    - input_fields: A list to store the input fields for booking details.
    - canvas: The canvas widget to display the booking log.

    Methods:
    - __init__(self, root): Initializes the Booking object.
    - load_data(self): Loads the booking data by reading from a file.
    - save_data(self): Saves the booking data by writing to a file.
    - get_max_text_width(self, entries): Calculates the maximum width of the text in the booking log.
    - add_booking(self): Adds a new booking to the log.
    - modify_booking(self, record_id): Modifies the status of a booking in the log.
    - cancel_booking(self, record_id): Cancels a booking in the log.
    - delete_booking(self, record_id): Deletes a booking from the log.
    - display_log(self, event=None): Displays the booking log on the canvas.
    - create_widgets(self): Creates the GUI widgets for the booking application.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Booking a Cab")

        self.records = self.load_data()
        self.input_fields = []

        self.create_widgets()

    def load_data(self):
        try:
            with open("booking_data.dat", "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return []

    def save_data(self):
        with open("booking_data.dat", "wb") as file:
            pickle.dump(self.records, file)

    def get_max_text_width(self, entries):
        max_width = 0
        for entry in entries:
            temp_text = self.canvas.create_text(0, 0, anchor="nw", text=entry, font=("Arial", 10), fill="black")
            text_width = self.canvas.bbox(temp_text)[2]
            max_width = max(max_width, text_width)
            self.canvas.delete(temp_text)
        return max_width

    def add_booking(self):
        set_year, set_month, set_day = map(int, [self.input_fields[0].get(), self.input_fields[1].get(), self.input_fields[2].get()])
        date = datetime.date(set_year, set_month, set_day)

        set_hour, set_minute = map(int, [self.input_fields[3].get(), self.input_fields[4].get()])
        time = datetime.time(set_hour, set_minute)

        pick_up_location, destination = map(str, [self.input_fields[5].get(), self.input_fields[6].get()])

        # Update booking number based on the length of the current records
        booking_number = len(self.records) + 1

        booking = (booking_number, "Pending", date, time, pick_up_location, destination)
        self.records.append(booking)

        self.save_data()
        self.display_records()


    def modify_booking(self, record_id):
        if self.records[record_id][1] == "Pending":
            self.records[record_id] = (self.records[record_id][0], "Booked", *self.records[record_id][2:])
        elif self.records[record_id][1] == "Booked":
            self.records[record_id] = (self.records[record_id][0], "Pending", *self.records[record_id][2:])
        self.save_data()
        self.display_records()

    def cancel_booking(self, record_id):
        self.records[record_id] = (self.records[record_id][0], "Cancelled", *self.records[record_id][2:])
        self.save_data()
        self.display_records()


    def delete_booking(self, record_id):
        del self.records[record_id]

        # Update booking numbers
        for i in range(record_id, len(self.records)):
            self.records[i] = (self.records[i][0] - 1, *self.records[i][1:])

        self.save_data()
        self.display_records()

    def display_records(self, event=None):
        """
        Display the records on the canvas.

        Args:
            event (Event, optional): The event that triggered the method. Defaults to None.
        """
        self.canvas.delete("all")

        for record_id, entry in enumerate(self.records):
            date_str = entry[2].strftime("%d/%m/%Y")
            time_str = entry[3].strftime("%H:%M")
            text = f"Booking {entry[0]}: Status: {entry[1]} - Date: {date_str} - Time: {time_str} - Pick-up: {entry[4]} - Destination: {entry[5]}"

            max_width = self.get_max_text_width([text])
            button_width = 100
            text_width_padding = 20
            button_padding = 20
            canvas_width = max_width + 4 * button_width + 4 * text_width_padding + 3 * button_padding

            self.canvas.config(width=(self.frame.winfo_width() - canvas_width) // 2)
            self.canvas.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")
            self.frame.grid_columnconfigure(0, weight=1)
            self.frame.grid_rowconfigure(8, weight=1)

            y_coordinate = record_id * 50 + 10 + 20
            self.canvas.create_text(10, y_coordinate, anchor="w", text=text, font=("Arial", 10), fill="black")

            detail_frame = Frame(self.canvas, bg="white")
            self.canvas.create_window(10, y_coordinate, anchor="w", window=detail_frame)

            detail_label = Label(detail_frame, text=text, font=("Arial", 10), anchor="w", justify="left")
            detail_label.pack(side=LEFT)

            button_frame = Frame(self.canvas, bg="white")
            self.canvas.create_window(max_width + 2 * text_width_padding + 2 * button_width + button_padding, y_coordinate, anchor="e", window=button_frame)

            action_button = Button(button_frame, text="Book", command=lambda i=record_id: self.modify_booking(i), width=8)
            action_button.pack(side=LEFT, padx=5)

            cancel_button = Button(button_frame, text="Cancel", command=lambda i=record_id: self.cancel_booking(i), width=8)
            cancel_button.pack(side=LEFT, padx=5)

            delete_button = Button(button_frame, text="Delete", command=lambda i=record_id: self.delete_booking(i), width=8)
            delete_button.pack(side=LEFT, padx=5)

    def create_widgets(self):
        self.frame = Frame(self.root)
        self.frame.pack(expand=True, fill="both")

        input_labels = ["Year:", "Month:", "Day:", "Hour:", "Minute:", "Pick-up Location:", "Destination:"]
        for i, label_text in enumerate(input_labels):
            Label(self.frame, text=label_text).grid(row=i, column=0, padx=5, pady=5)
            field = Entry(self.frame)
            field.grid(row=i, column=1, padx=5, pady=5)
            self.input_fields.append(field)

        add_booking_button = Button(self.frame, text="Add Booking", command=self.add_booking)
        add_booking_button.grid(row=len(input_labels) + 3, column=0, columnspan=2, padx=5, pady=5)

        print(add_booking_button.bind())  # Check for additional event bindings

        self.canvas = Canvas(self.frame, bg="white", scrollregion=(0, 0, 1000, 1000), highlightthickness=0)
        self.canvas.grid(row=8, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        xscrollbar = Scrollbar(self.frame, orient=HORIZONTAL, command=self.canvas.xview)
        xscrollbar.grid(row=9, column=0, columnspan=3, sticky="ew")
        self.canvas.config(xscrollcommand=xscrollbar.set)

        yscrollbar = Scrollbar(self.frame, orient=VERTICAL, command=self.canvas.yview)
        yscrollbar.grid(row=8, column=2, sticky="ns")
        self.canvas.config(yscrollcommand=yscrollbar.set)

        self.canvas.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(-1 * int(event.delta / 120), "units"))
        self.canvas.bind("<Configure>", lambda event: self.canvas.config(scrollregion=self.canvas.bbox("all")))

if __name__ == "__main__":
    root = Tk()
    app = Booking(root)
    app.display_records()
    root.mainloop()