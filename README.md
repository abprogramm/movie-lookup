# movie-lookup
The movie lookup tool is a web application built using Python and HTML, utilizing the Flask framework to provide a seamless user experience. This application allows users to search for movies and fetches detailed information from various movie review websites, aggregating the data for easy viewing.

# Features
Web Scraping: Automatically retrieves movie details from multiple sources, including popular movie review websites, ensuring comprehensive coverage of each title.
Search Functionality: Users can search for any movie by title, and the application will display all relevant information, including plot summaries, ratings, reviews, and release dates.
User-Friendly Interface: Built with a clean and intuitive HTML front-end that makes it easy for users to interact with the application and find the information they need.
Flask Integration: Utilizes Flask for routing and handling HTTP requests, allowing for efficient data processing and dynamic content rendering.
Data Aggregation: Combines data from multiple sources to present users with a well-rounded view of each movie, making it easier to make informed viewing decisions.

# Technology Stack
Python: The primary programming language for backend logic and web scraping.
Flask: A web framework used to handle routing, requests, and rendering of HTML templates.
Beautiful Soup & Requests: Libraries used for web scraping to extract data from various movie websites.
HTML/CSS: For front-end design and creating a responsive user interface.

# Required Packages
To run this application, the following Python packages are required:

Flask: To handle HTTP requests and render HTML templates.
Requests: To send HTTP requests and fetch data from the web.
BeautifulSoup4: To parse the HTML content of movie review websites.
lxml: (optional) Used by Beautiful Soup as a parser for faster performance.

# You can install these packages using the following command:
```bash
pip install Flask requests beautifulsoup4 lxml
```
# Installation
1. Clone the repository:
```bash
git clone https://github.com/abprogramm/movie-lookup.git
```
2. Navigate to the project directory:
```bash
cd movie-lookup
```
3. Run the Flask application:
```bash
python app.py
```
# Usage
Once the application is running, navigate to http://localhost:5000 in your web browser. Enter a movie title in the search bar, and the application will display detailed information sourced from multiple review websites.
