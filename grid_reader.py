import requests
from bs4 import BeautifulSoup
import argparse
import re


def is_valid_published_doc_url(url):
    """
    Validates if the URL is a valid published Google Docs URL.

    Args:
        url (str): The URL to validate

    Returns:
        bool: True if the URL is valid, False otherwise
    """
    # check the pattern of the url
    # it typically looks like: https://docs.google.com/document/d/e/[document_id]/pub
    pattern = r'^https://docs\.google\.com/document/d/e/[A-Za-z0-9_-]+/pub$'

    if not re.match(pattern, url):
        return False

    return True


def fetch_and_print_grid(url):
    """
    Fetches data from a published Google Doc, parses the HTML with BeautifulSoup, and prints the grid of characters.

    Args:
        url (str): The URL of the published Google Doc
    """
    # validate URL before proceeding
    if not is_valid_published_doc_url(url):
        print("Error: Invalid or inaccessible published Google Docs URL.")
        print("Please provide a URL in the format: https://docs.google.com/document/d/e/[document_id]/pub")
        return

    try:
        # since we have a published document, we can use requests to fetch the document
        # no need for google api or gspread
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch document. Status code: {response.status_code}")

        # bs for parsing the html
        soup = BeautifulSoup(response.text, 'html.parser')

        # first, find all table rows in the document
        # its actually pure html
        rows = soup.find_all('tr')

        content_lines = []
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 3:  # we need at least 3 cells, all others are headers or rubish
                line_parts = []
                for cell in cells[:3]:  # slice the row to get x, y, and char
                    line_parts.append(cell.get_text().strip())
                content_lines.append(' '.join(line_parts))

        points = []
        # tracking max_x and max_y to determine the dimensions needed for the grid that will display the characters
        # this is to ensure the grid is large enough to display all characters
        # too small and it will cause index errors when placing characters
        max_x, max_y = 0, 0

        for line in content_lines:
            if not line.strip():
                continue
            parts = line.strip().split()
            if len(parts) < 3:
                continue
            try:
                x, y = int(parts[0]), int(parts[2])
                char = parts[1]
                points.append((x, y, char))
                max_x = max(max_x, x)
                max_y = max(max_y, y)
            except (ValueError, IndexError):
                continue

        if not points:
            # todo: handle this better with a custom exception
            print("No valid points found in the document.")
            return

        # create a grid with the dimensions needed to display the characters
        grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]

        # fill grid with characters
        for x, y, char in points:
            grid[y][x] = char

        # print the grid by joining the rows
        for row in grid:
            print("".join(row))

    except Exception as e:
        # if something goes wrong, print the error
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Fetch and display a grid from a published Google Doc.'
    )
    parser.add_argument(
        'url',
        help='URL of the published Google Doc (must be in format: '
             'https://docs.google.com/document/d/e/[document_id]/pub)'
    )
    args = parser.parse_args()

    fetch_and_print_grid(args.url)
