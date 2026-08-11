import csv
import re

# ---------------------------------------------------------------------------
# METHOD 2: Custom Genre & Trope Map for 2026 Books
# ---------------------------------------------------------------------------
GENRE_MAP = {
    "Emily Wilde’s Map of the Otherlands": ["#FaerieFantasy", "#CozyFantasy", "#Academics", "#Romance"],
    "Overruled": ["#Romance", "#Lawyers", "#OppositesAttract", "#Contemporary"],
    "Assistant to the Villain": ["#FantasyRomance", "#GrumpyXSunshine", "#Humor", "#VillainTropes"],
    "Apprentice to the Villain": ["#FantasyRomance", "#GrumpyXSunshine", "#FoundFamily", "#Duology"],
    "My Friends": ["#Contemporary", "#LiteraryFiction", "#Friendship", "#Emotional"],
    "Not Quite Dead Yet": ["#Mystery", "#Thriller", "#YA", "#Whodunit"],
    "Everything Is Tuberculosis": ["#NonFiction", "#History", "#MedicalHistory", "#Science"],
    "Hot for Slayer": ["#ParanormalRomance", "#Vampires", "#ShortRead", "#Humor"],
    "Falling": ["#ContemporaryRomance", "#Drama", "#Emotional", "#FastPaced"],
    "Spicy Little Curses": ["#ParanormalRomance", "#Witches", "#Humor", "#Romance"],
    "Space Vampire": ["#SciFiRomance", "#Aliens", "#Vampires", "#ShortRead"],
    "Beautiful Nightmare": ["#DarkRomance", "#Fantasy", "#Mythology", "#Monsters"],
    "My Boyfriends Are All Monsters": ["#ParanormalRomance", "#MonsterRomance", "#Humor", "#Cozy"],
    "Just for the Summer": ["#ContemporaryRomance", "#FakeDating", "#SummerVibes", "#Emotional"],
    "Funny Story": ["#ContemporaryRomance", "#FakeDating", "#SmallTown", "#Humor"],
    "Mate": ["#ParanormalRomance", "#Werewolves", "#FatedMates", "#Romance"],
    "Sashiko 365": ["#NonFiction", "#Crafts", "#Embroidery", "#DIY"],
    "Katabasis": ["#DarkAcademia", "#Mythology", "#Underworld", "#GothicFantasy"],
    "The Poison Daughter": ["#DarkRomantasy", "#Enemies2Lovers", "#SPICY", "#SlowBurn"]
}

def clean_title(title):
    # Strip series info in parentheses for cleaner display
    return re.sub(r'\s*\([^)]*\)', '', title).strip()

def get_tags_for_book(title):
    # Match title against GENRE_MAP
    for book_key, custom_tags in GENRE_MAP.items():
        if book_key.lower() in title.lower():
            return custom_tags
    
    # Generic fallback if a title is added later
    return ["#BookTok", "#ReadIn2026", "#Fiction", "#MustRead"]

# ---------------------------------------------------------------------------
# Step 1: Read Goodreads Export & Build 3D Pages
# ---------------------------------------------------------------------------
books_2026 = []
with open('goodreads_library_export.csv', mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        date_read = row.get('Date Read', '').strip()
        if date_read.startswith('2026'):
            books_2026.append(row)

# Sort chronologically by date read
books_2026.sort(key=lambda x: x.get('Date Read', ''))

print(f"Found {len(books_2026)} books read in 2026.")

book_cards_html = []

for idx, book in enumerate(books_2026, start=1):
    full_title = book.get('Title', 'Untitled')
    display_title = clean_title(full_title)
    author = book.get('Author', 'Unknown')
    book_id = book.get('Book Id', '')
    
    # Goodreads direct URL using Book Id
    goodreads_url = f"https://www.goodreads.com/book/show/{book_id}" if book_id else "https://www.goodreads.com/user/show/119296496-anindita"
    
    # Convert Rating
    try:
        rating = int(float(book.get('My Rating', 0)))
    except (ValueError, TypeError):
        rating = 0
        
    # Get 4 tags from GENRE_MAP
    tropes = get_tags_for_book(display_title)
    
    # Format Review Paragraphs
    raw_review = book.get('My Review', '').strip()
    if raw_review:
        paragraphs = raw_review.split('<br/><br/>')
        formatted_review = "".join(f"<p>{p.strip()}</p>" for p in paragraphs if p.strip())
    else:
        formatted_review = '<p class="review-placeholder"><em>Review coming soon! Currently organizing thoughts...</em></p>'

    review_filename = f"book_{idx}.html"
    cover_img_path = f"images/book_{idx}.jpg"
    theme_class = f"theme-{re.sub(r'[^a-z0-9]', '-', display_title.lower())}"

    # Build 3D HTML Page Template
    review_html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{display_title} - Review</title>
    <link rel="stylesheet" href="style.css">
</head>
<body class="{theme_class}">
    <div class="main-container">
        <!-- Back Navigation -->
        <a href="index.html" class="back-link">&larr; Back to 2026 Bookshelf</a>

        <!-- Book Header -->
        <header class="review-header">
            <h1>{display_title}</h1>
            <h3>by {author}</h3>
        </header>

        <!-- Interactive 3D Showcase Section -->
                <section class="book-showcase-container">
                    <p class="hover-prompt">Hover over the book to reveal tropes!</p>
                    
                    <div class="scene">
                        <div class="book-3d">
                            <!-- Front Cover -->
                            <div class="face front">
                                <img src="{cover_img_path}" alt="{display_title} Cover" onerror="this.src='https://via.placeholder.com/100x150?text=Cover';">
                            </div>
                            <!-- Spine -->
                            <div class="face spine">
                                <span>{display_title}</span>
                            </div>
                            <!-- Back Cover -->
                            <div class="face back">
                                <img src="{cover_img_path}" alt="Back Cover" onerror="this.src='https://via.placeholder.com/100x150?text=Cover';">
                            </div>
                            <div class="face right"></div>
                            <div class="face top"></div>
                            <div class="face bottom"></div>

                            <!-- Double-Sided Hover Tropes -->
                            <div class="trope-tag trope-1">
                                <span class="tag-face tag-front">{tropes[0]}</span>
                                <span class="tag-face tag-back">{tropes[0]}</span>
                            </div>
                            <div class="trope-tag trope-2">
                                <span class="tag-face tag-front">{tropes[1]}</span>
                                <span class="tag-face tag-back">{tropes[1]}</span>
                            </div>
                            <div class="trope-tag trope-3">
                                <span class="tag-face tag-front">{tropes[2]}</span>
                                <span class="tag-face tag-back">{tropes[2]}</span>
                            </div>
                            <div class="trope-tag trope-4">
                                <span class="tag-face tag-front">{tropes[3]}</span>
                                <span class="tag-face tag-back">{tropes[3]}</span>
                            </div>
                        </div>
                    </div>
                </section>

        <!-- Goodreads Links Section -->
        <section class="review-content">
            <div class="goodreads-actions">
                <a href="{goodreads_url}" 
                   target="_blank" 
                   rel="noopener noreferrer" 
                   class="goodreads-btn">
                    View Book on Goodreads &rarr;
                </a>
                <a href="https://www.goodreads.com/user/show/119296496-anindita" 
                   target="_blank" 
                   rel="noopener noreferrer" 
                   class="goodreads-btn secondary-btn">
                    Visit My Goodreads Profile &rarr;
                </a>
            </div>

            <!-- Review Body Container -->
            <article class="review-body">
                <h2>My Thoughts</h2>
                {formatted_review}
            </article>
        </section>
    </div>
</body>
</html>"""

    with open(review_filename, 'w', encoding='utf-8') as out_file:
        out_file.write(review_html_content)

    # Shelf card for index.html
    badge_html = f'<div class="star-badge" title="{rating} Stars!">✨ {rating}</div>' if rating == 5 else ''
    
    card_snippet = f"""                    <a href="{review_filename}" class="book-card" title="{display_title}">
                        {badge_html}
                        <img src="{cover_img_path}" alt="{display_title} by {author}" class="book-cover" onerror="this.src='https://via.placeholder.com/100x150?text=Cover';">
                    </a>"""
    book_cards_html.append(card_snippet)

print("Generated all 19 3D review pages with custom genre tags!")

# ---------------------------------------------------------------------------
# Step 2: Build Complete Updated index.html
# ---------------------------------------------------------------------------
all_cards_str = "\n".join(book_cards_html)

index_html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My 2026 Bookshelf</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="main-container">
        
        <!-- Header Banner -->
        <header class="page-banner">
            <h1>My 2026 Reading Archive</h1>
            <p>Select a book cover to view my 3D review & tropes.</p>
        </header>

        <!-- Two-Column Grid Layout -->
        <div class="dashboard-grid">
            
            <!-- Left Invisible Column: Profile & Navigation Hub -->
            <aside class="profile-column">
                <div class="profile-avatar">
                    <img src="images/profile.jpg" alt="Anindita's Avatar" onerror="this.src='https://www.goodreads.com/assets/nophoto/user/f_225x225-7064bb4f551751d93e706612d3309a6d.png';">
                </div>
                
                <h2>Anindita</h2>
                <p class="profile-bio">Welcome to my 2026 reading sanctuary! I review fantasy, gothic fiction, and romance novels with interactive 3D breakdowns.</p>

                <div class="link-stack">
                    <a href="https://www.goodreads.com/user/show/119296496-anindita" target="_blank" rel="noopener noreferrer" class="hub-btn goodreads-btn">
                        <span class="btn-icon">📚</span> Goodreads Profile
                    </a>
                    
                    <a href="https://www.goodreads.com/readingchallenges?ref=web_ingress" target="_blank" rel="noopener noreferrer" class="hub-btn challenge-btn">
                        <span class="btn-icon">🎯</span> 2026 Reading Goal
                    </a>

                    <a href="https://www.goodreads.com/user/year_in_books/2025/119296496" target="_blank" rel="noopener noreferrer" class="hub-btn stats-btn">
                        <span class="btn-icon">📊</span> 2025 Reading Stats
                    </a>

                    <a href="https://www.goodreads.com/notes/119296496-anindita?ref=nav_profile_knh" target="_blank" rel="noopener noreferrer" class="hub-btn kindle-btn">
                        <span class="btn-icon">📖</span> Kindle Notes
                    </a>

                    <a href="https://www.youtube.com/@DitasVirtualDesk" target="_blank" rel="noopener noreferrer" class="hub-btn youtube-btn">
                        <span class="btn-icon">▶</span> YouTube Channel
                    </a>
                </div>
            </aside>

            <!-- Right Invisible Column: Bookshelf -->
            <main class="bookshelf-column">
                <div class="shelf-header">
                    <h2>2026 Reads ({len(books_2026)} Books)</h2>
                </div>
                
                <div class="bookshelf">
{all_cards_str}
                </div>
                <!-- Wooden Shelf Base -->
                <div class="shelf-wood"></div>
            </main>

        </div>
    </div>
</body>
</html>"""

with open('index.html', 'w', encoding='utf-8') as out_file:
    out_file.write(index_html_content)

print("Updated index.html with all 2026 books successfully!")