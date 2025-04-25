# Grid Character Reader

This Python script reads a grid of Unicode characters from a Google Doc and prints them in a way that forms a graphic message.

## Requirements

- Python 3.8 or higher
- Poetry for dependency management

## Setup

1. Install Poetry if you haven't already:

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Clone this repository and install dependencies:

   ```bash
   poetry install
   ```

3. Set up Google API credentials:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable the Google Docs API for your project
   - Create OAuth 2.0 credentials:
     - Go to "APIs & Services" > "Credentials"
     - Click "Create Credentials" > "OAuth client ID"
     - Choose "Desktop app" as the application type
     - Download the credentials and save them as `credentials.json` in the project root

## Usage

1. Activate the Poetry environment:

   ```bash
   poetry shell
   ```

2. Run the script:

   ```bash
   python grid_reader.py
   ```

3. When prompted, enter the URL of your Google Doc containing the grid data.

## Input Format

The Google Doc should contain lines in the format:

```
x y character
```

For example, for a grid that forms the letter 'F':

```
0 0 █
0 1 █
0 2 █
1 0 ▀
2 0 ▀
3 0 ▀
1 1 ▀
2 1 ▀
```

This would output:

```
█▀▀▀
█▀▀
█
```

## Notes

- Coordinates start at (0,0) in the top-left corner
- X increases to the right
- Y increases downward
- Empty spaces are filled with spaces
- The first time you run the script, it will open a browser window for you to authenticate with Google
- Authentication tokens are stored in `token.pickle` for future use
