from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from PIL import Image
import requests
from io import BytesIO

def get_average_rgb(rgb_values):
    if not rgb_values:
        return None
    
    total_r, total_g, total_b = 0, 0, 0
    num_pixels = len(rgb_values)
    
    for r, g, b in rgb_values:
        total_r += r
        total_g += g
        total_b += b
    
    avg_r = int(total_r / num_pixels)
    avg_g = int(total_g / num_pixels)
    avg_b = int(total_b / num_pixels)
    
    return (avg_r, avg_g, avg_b)


def get_rgb_values_from_url(image_url):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            width, height = img.size
            rgb_values = []
            for y in range(height):
                for x in range(width):
                    r, g, b = img.getpixel((x, y))
                    rgb_values.append((r, g, b))
        
            return rgb_values
        
        else:
            print(f"Failed to fetch image from URL: {image_url}")
            return None
    
    except Exception as e:
        print(f"Error fetching image from URL: {image_url}, {e}")
        return None

app = Flask(__name__)


@app.route('/')
def index():
    data = [
        {'title' : 'None'}
    ]
    return render_template('index.html', header='Movie Information Lookup', data=data, rgb_val=(255, 255, 255))

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        input_data = request.form['input_data']

        r = requests.get(f'https://www.rottentomatoes.com/search?search={input_data}')

        print(r.url)

        soup = BeautifulSoup(r.text, 'html.parser')

        pos = [link.get('href') for link in (soup.find_all('a', slot='title'))] #if movie_input.lower() in link.get('href').lower()]

        names = {}
        for p in pos:
            x = soup.find('a', href=f'{p}', slot='title').text.strip()
            names[x] = p

        print(names)
        for i, name in enumerate(list(names.keys())):
            print(f'[{i+1}] {name}')

        try:
            num = 1
        except:
            print('Invalid number, please try again.')
        else:   
            pass

        r = requests.get((list(names.values()))[(num-1)])

        soup = BeautifulSoup(r.text, 'html.parser')

        realname = soup.find(slot='titleIntro').text.strip()
        image = soup.find('rt-img', slot='posterImage').get('src')
        rgb_values = get_rgb_values_from_url(image)
        try:
            rating = soup.find('rt-text', slot='ratingsCode').text.strip()
        except:
            rating = 'NR'
        else:
            pass
        releasedate = soup.find('rt-text', slot='releaseDate').text.strip()
        try:
            duration = soup.find('rt-text', slot='duration').text.strip()
        except:
            duration = 'Unspecified'
        else:
            pass
        critics = soup.find('rt-button', slot='criticsScore').text.strip()
        audience = soup.find('rt-button', slot='audienceScore').text.strip()
        countcritics = soup.find('rt-link', slot='criticsReviews').text.strip()
        countaudience = soup.find('rt-link', slot='audienceReviews').text.strip()


        r = requests.get(f'https://www.boxofficemojo.com/search/?q={realname}')

        soup = BeautifulSoup(r.text, 'html.parser')

        test = [link.get('href') for link in (soup.find_all(class_='a-size-medium a-link-normal a-text-bold'))]
        realLink = None
        domestic = 'No information'
        international = 'No information'
        total = 'No information'

        if len(test) > 0:
            realLink = f'https://boxofficemojo.com{test[0]}'
        
        if realLink:
            r = requests.get(realLink)
            soup = BeautifulSoup(r.text, 'html.parser')
            values = [val.text.strip() for val in (soup.find_all(class_='a-size-medium a-text-bold'))]
            domestic = values[0]
            international = values[1]
            total = values[2]


        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
        r = requests.get(f'https://imdb.com/find/?q={realname}', headers=headers)

        soup = BeautifulSoup(r.text, 'html.parser')

        test = [link.get('href') for link in (soup.find_all(class_='ipc-metadata-list-summary-item__t'))]

        r = requests.get(f'https://imdb.com{test[0]}', headers=headers)

        soup = BeautifulSoup(r.text, 'html.parser')

        test = soup.find_all(class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link')

        director = test[0].text.strip()
        writer = test[1].text.strip()
        ac1 = test[2].text.strip()
        ac2 = test[3].text.strip()
        ac3 = test[4].text.strip()


        print(f"""

        Rating: {rating}
        Release Date: {releasedate}
        Duration: {duration}
        Critics RT%: {critics} ({countcritics})
        Audience RT%: {audience} ({countaudience})


        """)

        data = [
                {'title' : 'Rating', 'content': rating},
                {'title' : 'Release Date', 'content': releasedate},
                {'title' : 'Director', 'content': director},
                {'title' : 'Writer', 'content': writer},
                {'title' : 'Actor #1', 'content': ac1},
                {'title' : 'Actor #2', 'content': ac2},
                {'title' : 'Actor #3', 'content': ac3},
                {'title' : 'Duration', 'content': duration},
                {'title' : 'Critics 🍅%', 'content': f'{critics} ({countcritics})'},
                {'title' : 'Audience 🍅%', 'content': f'{audience} ({countaudience})'},
                {'title' : 'Domestic Gross 💵', 'content': f'{domestic}'},
                {'title' : 'International Gross 💶', 'content': f'{international}'},
                {'title' : 'Total Gross 💰', 'content': f'{total}'}
        ]   

        return render_template('index.html', header=realname, data=data, image=image, rgb_val=(get_average_rgb(rgb_values)))

if __name__ == '__main__':
    app.run(debug=True)