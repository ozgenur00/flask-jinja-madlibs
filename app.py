from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from stories import Story, story1, story2
import random


# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# Create a dictionary of stories
stories = {story1.code: story1, story2.code: story2}

@app.route('/')
def home():
    # Randomly select a story
    story = random.choice(list(stories.values()))
    # Pass the story prompts to the template
    return render_template('homepage.html', story=story)

@app.route('/story', methods=['POST'])
def show_story():
    story_code = request.form['story_code']
    story = stories.get(story_code)

    if not story:
        return "Story not found", 404

    # Extract answers from the form submission
    answers = {prompt: request.form[prompt] for prompt in story.prompts}
    # Generate the story text
    story_text = story.generate(answers)
    # Render the story text in the story template
    return render_template('story.html', text=story_text)

if __name__ == '__main__':
    app.run(debug=True)