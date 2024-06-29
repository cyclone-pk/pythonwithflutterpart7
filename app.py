from flask import Flask, jsonify
from selenium import webdriver
from bs4 import BeautifulSoup

app = Flask(__name__)

# Path to the chromedriver executable. Replace with your actual path.
chromedriver_path = '/Users/zakriakhan/Downloads/chromedriver-mac-arm64/chromedriver'

@app.route('/youtube/<query>')
def youtube_search(query):
    try:
        # Construct the YouTube search URL based on the query parameter
        url = f'https://www.youtube.com/results?search_query={query}'
        
        # Set up Chrome options to run in headless mode (without GUI)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        
        # Initialize Chrome webdriver with path to chromedriver executable
        driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        
        # Open the URL in Chrome browser
        driver.get(url)
        
        # Get the page source HTML after JavaScript execution
        html = driver.page_source
        
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find all elements with id="video-title" (video titles)
        results = soup.find_all(id="video-title")
        
        # List to store dictionaries of video titles and links
        results_list = []
        
        # Iterate over each video title element found
        for tag in results:
            title = tag.get('title')  # Get the title attribute
            href = tag.get('href')    # Get the href attribute
            
            # Check if both title and href are present
            if href and title:
                # Construct the full video link using YouTube base URL
                video_link = f'https://www.youtube.com{href}'
                
                # Create dictionary for each video result
                result_item = {"title": title, "link": video_link}
                
                # Append the result dictionary to the results_list
                results_list.append(result_item)
        
        # Close the webdriver instance
        driver.quit()
        
        # Prepare JSON response with query and results_list
        response = {"query": query, "results": results_list}
        
        # Return JSON response using Flask jsonify function
        return jsonify(response)
    
    except Exception as e:
        # Return error message and status code 500 in case of exception
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
