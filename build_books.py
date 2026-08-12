import pandas as pd
import html

# Load the Goodreads CSV export
df = pd.read_csv('goodreads_library_export.csv')

# Filter for books you've marked as 'read'
read_books = df[df['Exclusive Shelf'] == 'read'].copy()

# List of target titles you want to map to book1.html - book6.html
target_titles = [
    'The Poison Daughter',
    'Divine Rivals',
    'Ruthless Vows',
    'One Dark Window',
    'My Friends',
    'Bride'
]

for i, target in enumerate(target_titles, start=1):
    # Match title in CSV
    matches = read_books[read_books['Title'].str.contains(target, case=False, na=False)]
    
    if not matches.empty:
        book = matches.iloc[0]
        title = book['Title']
        author = book['Author']
        rating = int(book['My Rating']) if pd.notna(book['My Rating']) and book['My Rating'] > 0 else 5
        
        # Format review text into HTML paragraphs
        raw_review = str(book['My Review']) if pd.notna(book['My Review']) else "No written review provided."
        formatted_review = "".join(f"<p>{p.strip()}</p>" for p in raw_review.split('<br/><br/>') if p.strip())
        
        filename = f"book{i}.html"
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Review</title>
    <link rel="stylesheet" href="style.css">
</head>
<body class="review-page">
    <div class="review-container">
        <a href="index.html" class="back-link">&larr; Back to Bookshelf</a>
        
        <header class="review-header">
            <h1>{title}</h1>
            <h3>by {author}</h3>
            <div class="star-rating">{"★" * rating}</div>
        </header>

        <main class="review-body">
            {formatted_review}
        </main>
    </div>
</body>
</html>"""

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"Generated {filename} for '{title}'")

print("Done! All book review pages updated from your Goodreads CSV.")