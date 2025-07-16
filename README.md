# LoL Item Quiz

A League of Legends item knowledge quiz application built with Flask.

## 🎮 Live Demo

**🌐 [https://lol-item-quiz.com](https://lol-item-quiz.com)**

## 🚀 Features

- **Quiz A**: Item Component Quiz - Identify which items are used to build the given item
- **Quiz B**: Price Guessing Quiz - Guess the correct gold cost of items
- **Consecutive Score Tracking**: Track your streak of correct answers
- **Latest Patch Support**: Currently supports Patch 15.13.1

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML/CSS/JavaScript
- **Deployment**: Gunicorn + Nginx
- **Infrastructure**: Ubuntu VPS

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/53b29461/lol-item-quiz.git
cd lol-item-quiz
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and visit `http://localhost:5000`

## 🎯 Game Rules

### Quiz A (Item Components)
- You'll be shown a final item
- Select all the component items that are used to build it
- Earn points for consecutive correct answers

### Quiz B (Price Guessing)
- You'll be shown an item
- Guess its exact gold cost
- Test your knowledge of the in-game economy

## 🔧 Configuration

- Item data is fetched from Riot Games' Data Dragon API
- Patch version can be updated in `app.py`
- Filtering logic removes consumables, boots, and jungle-specific items

## 📈 Development

This project demonstrates:
- RESTful API integration (Riot Games Data Dragon)
- Session management
- Data filtering and processing
- Responsive web design
- Production deployment practices

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is for educational purposes. League of Legends is a trademark of Riot Games, Inc.

---

*Built with ❤️ for the League of Legends community*
