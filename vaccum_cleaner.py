import tkinter as tk
import random

class VacuumAgentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vacuum Agent Simulation")

        # Room coordinates on canvas
        self.rooms = {
            'A': (50, 50),
            'B': (200, 50),
            'C': (50, 200),
            'D': (200, 200),
        }

        self.room_size = 100
        self.status = {room: random.choice(['clean', 'dirty']) for room in self.rooms}
        self.current_location = 'A'

        self.canvas = tk.Canvas(root, width=350, height=350)
        self.canvas.pack()

        self.draw_rooms()
        self.vacuum = None
        self.running = True

        self.root.after(1000, self.step)  # Start after 1 sec

    def draw_rooms(self):
        self.canvas.delete("all")
        for room, (x, y) in self.rooms.items():
            color = "sienna" if self.status[room] == "dirty" else "white"
            self.canvas.create_rectangle(x, y, x+self.room_size, y+self.room_size, fill=color, outline="black")
            self.canvas.create_text(x + self.room_size//2, y + self.room_size//2, text=room, font=("Arial", 20))

        # Draw vacuum as a blue circle in current room
        x, y = self.rooms[self.current_location]
        r = 20
        self.vacuum = self.canvas.create_oval(
            x + self.room_size//2 - r, y + self.room_size//2 - r,
            x + self.room_size//2 + r, y + self.room_size//2 + r,
            fill="blue"
        )

    def move_vacuum(self, new_location):
        self.current_location = new_location
        # Animate vacuum moving to new location
        x, y = self.rooms[new_location]
        r = 20
        # Update vacuum position directly for simplicity
        self.canvas.coords(
            self.vacuum,
            x + self.room_size//2 - r, y + self.room_size//2 - r,
            x + self.room_size//2 + r, y + self.room_size//2 + r,
        )

    def perceive_and_act(self):
        current = self.current_location
        # Perceive status
        if self.status[current] == "dirty":
            # Clean current room
            self.status[current] = "clean"
            print(f"Cleaning room {current}")
        else:
            # Follow movement rules
            if current == 'A':
                if self.status['B'] == 'dirty':
                    self.move_vacuum('B')
                elif self.status['C'] == 'dirty':
                    self.move_vacuum('C')
                else:
                    self.move_vacuum('B')
            elif current == 'B':
                if self.status['D'] == 'dirty':
                    self.move_vacuum('D')
                elif self.status['A'] == 'dirty':
                    self.move_vacuum('A')
                else:
                    self.move_vacuum('D')
            elif current == 'C':
                if self.status['D'] == 'dirty':
                    self.move_vacuum('D')
                elif self.status['A'] == 'dirty':
                    self.move_vacuum('A')
                else:
                    self.move_vacuum('D')
            elif current == 'D':
                if self.status['B'] == 'dirty':
                    self.move_vacuum('B')
                elif self.status['C'] == 'dirty':
                    self.move_vacuum('C')
                else:
                    self.move_vacuum('B')

    def step(self):
        if not self.running:
            return

        self.perceive_and_act()
        self.draw_rooms()  # redraw rooms with updated clean/dirty state

        # Continue after delay
        self.root.after(1000, self.step)

    def stop(self):
        self.running = False


if __name__ == "__main__":
    root = tk.Tk()
    app = VacuumAgentApp(root)
    root.mainloop()
