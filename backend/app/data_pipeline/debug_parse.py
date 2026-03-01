from bs4 import BeautifulSoup

with open("flipkart_page.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

print("=" * 60)
print("🔍 SEARCHING FOR PRICES (₹ symbol)")
print("=" * 60)

# Find all elements containing ₹
price_tags = soup.find_all(string=lambda t: t and "₹" in t)
for tag in price_tags[:10]:
    parent = tag.parent
    print(f"Tag: <{parent.name}> | Class: {parent.get('class')} | Text: {tag.strip()[:40]}")

print("\n" + "=" * 60)
print("🔍 SEARCHING FOR PRODUCT TITLES (Samsung)")
print("=" * 60)

# Find all elements containing 'Samsung Galaxy S24'
title_tags = soup.find_all(string=lambda t: t and "Samsung Galaxy S24" in t)
for tag in title_tags[:10]:
    parent = tag.parent
    print(f"Tag: <{parent.name}> | Class: {parent.get('class')} | Text: {tag.strip()[:60]}")

print("\n" + "=" * 60)
print("🔍 SEARCHING FOR PRODUCT LINKS (/p/)")
print("=" * 60)

# Find all product links
links = soup.find_all("a", href=lambda h: h and "/p/" in h)
for link in links[:5]:
    print(f"Class: {link.get('class')} | href: {link['href'][:60]}")