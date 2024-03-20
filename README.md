# Install the required dependencies:

pip install -r requirements.txt

# Set up environment variables:

Create a .env file in the root directory.

Add your OpenAI API key to the .env file:

OPEN_AI_KEY=your-openai-api-key

# Not necessary 
Install the local package in the virtual environment:

python setup.py install

# Run the Streamlit application:

streamlit run streamlitapp.py
