
---

# Smart Movie Recommendation System

An intelligent, error-tolerant movie recommendation platform that bridges content-based filtering with dynamic metadata retrieval. Unlike basic recommendation scripts that crash on user typos, this engine uses fuzzy string matching and multi-layered fallback paths to ensure a smooth, production-ready user experience.

---

## The Problem

Most portfolio recommendation systems rely on **exact string matching**. If a user makes a simple typo (e.g., typing `"Toy Sory"` instead of `"Toy Story"`), or searches for a movie outside the dataset, the application throws a jarring `IndexError` or returns blank results.

In the real world, rigid search fields frustrate users, reduce engagement metrics, and lead to platform abandonment.

## The Business Solution

This project addresses that exact product friction by treating user error as a core design parameter. By implementing a multi-stage fallback pipeline, the **Smart Movie Recommendation System** safeguards the user experience:

* **Keeps Users Engaged:** Instead of a dead-end error screen, users are gently guided back on track with active suggestions.
* **Provides Value Automatically:** If a specific product (movie) isn't available, the engine instantly pivots to recommend high-quality alternatives within the same category (genre).

---

## System Architecture & Logic

The system processes movie metadata and handles user inputs through a defined four-tier decision tree:

1. **Text Vectorization (TF-IDF):** Converts raw text genre strings into a numerical grid matrix, isolating meaningful terms and stripping out unhelpful filler words (like "the" or "and").
2. **Cosine Similarity Mapping:** Measures the mathematical angles between the numerical genre vectors. Movies with overlapping genre distributions score closer to `1`, establishing a permanent connection map.
3. **Fuzzy String Matching:** When a user searches for a movie, the system utilizes string sequence matching. If a title is misspelled by a few characters, it catches the mistake, asks *"Did you mean X?"*, and runs the math on the corrected title.
4. **Genre & Deep Fallback Layers:** If the title is completely missing, the engine checks for an optional genre hint. If no hint exists but the user accidentally typed a genre into the title box (e.g., searching for `"Sci-Fi"` as a title), it recognizes the intent and displays top-tier films from that category.

---

##  How to Run This Project Locally

Follow these two steps to set up and run the interactive web application on your computer.
Make sure you have **Python 3.10+** installed on your system.

---
## STEP A


### Generate the Model File (.pkl)

The final trained model file is large; it's not stored on GitHub. Instead, you will generate it on your own machine using the included dataset:

1. Open your terminal in the project folder and start Jupyter Notebook:
```bash
jupyter notebook

```

2. Open `Recommendation_System.ipynb`.
3. Add the dataset (**`movie.csv`**) to your coding environment. Run all the cells sequentially. This script will automatically read the dataset, clean the movie genres, build the mathematical similarity map, and save the `smart_movies_recommendation.pkl` file directly into your project folder.

---

## STEP B
### 1. Clone the Repository

Open your terminal or command prompt and clone this project:

```bash
git clone https://github.com/qudus-o/smart_movie_recommendation.git
cd smart_movie_recommendation

```

### 2. Set Up a Virtual Environment (Recommended)

Keep your project dependencies isolated and clean:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

```

### 3. Install Dependencies

Install all the required third-party libraries using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt

```

### 4. Configure Your Environment Variables

The application pulls live movie posters from The Movie Database (TMDB) API.

1. Create a file named `.env` in the root folder of the project.
2. Add your secret TMDB API key inside it like this:

```text
TMDB_API_KEY=your_actual_api_key_here

```

### 5. Launch the Web Application
Note: Make sure the `.pkl` file is in your file directory.

Run the Streamlit frontend script to spin up the local server:

```bash
streamlit run app.py

```

Your browser will automatically open a new tab at `http://localhost:....` showing the interactive user interface!

---

## Tech Stack

* **Data Science & ML:** Python, Pandas, NumPy, Scikit-Learn (`TfidfVectorizer`, `cosine_similarity`)
* **Frontend UI:** Streamlit
* **Fuzzy Matching & String Processing:** Python Built-in `difflib`
* **APIs & Storage:** REST APIs (`requests`), Environment Security (`python-dotenv`), Serialization (`pickle`)
