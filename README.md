# Rome: Republic Legacy

**Revive the Ancient Rome in a Strategic Card Game**

Rome: Republic Legacy is an online card game blending role-playing, turn-based strategy, and historical immersion. Play as legendary Roman figures such as Julius Caesar, Lucinius Crassus, and Pompeius Magnus—or as Rome's greatest nemeses, including Hannibal Barca and Vercingetorix. Outwit your opponent with unique abilities, cards, and tactics inspired by real history.

---

## Features
- **Role-Playing & Strategy**: Choose from a roster of historical characters, each with unique abilities and quotes.
- **Turn-Based Card Battles**: Deploy units, play political and military cards, and manage resources to achieve victory.
- **Online Multiplayer**: Play against friends or other players online.
- **Rich Historical Theme**: Experience the drama of the late Roman Republic through gameplay and character design.

---

## Media
- UI and card assets are located in `main/GameUI/assets/sources.zip` and `UI.zip`.
- Game snips 
![Diagram](example/Media/caesar_vs_verc.png)


---

## Installation
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd rome_card_game
   ```
2. **Install dependencies:**
   ```bash
   pip install -r main/requirements.txt
   ```
3. **Run the server:**
   ```bash
   cd main
   python wsgi_server.py
   ```

---

## How to Play
- **Rulebook**: See [Rulebook.docx](./Rulebook.docx) for detailed rules and gameplay instructions.
- **Quick Start**:
  1. Start the server as above.
  2. Connect two clients to the server.
  3. Choose your character and begin playing cards according to the prompts.

---

## Project Structure
- `main/Game/` — Core game logic, including cards, characters, and units.
- `main/GameUI/` — UI logic and assets for the game interface.
- `main/wsgi_server.py` — Main server entry point (Flask + SocketIO).
- `main/transmitter.py` — Example client for connecting to the server.
- `main/Utils.py` — Utility classes and helpers.
- `example/` — Example client and server scripts for testing or development.
- `Rulebook.docx` — Complete game rules and instructions.

---

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a clear description of your changes.

For major changes, please open an issue first to discuss what you would like to change.

---
