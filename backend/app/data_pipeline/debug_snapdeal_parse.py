from bs4 import BeautifulSoup

with open("snapdeal_page.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

print("=" * 60)
print("🔍 SEARCHING FOR PRICES (Rs. or ₹)")
print("=" * 60)
price_tags = soup.find_all(string=lambda t: t and ("Rs." in t or "₹" in t))
for tag in price_tags[:10]:
    parent = tag.parent
    print(f"Tag: <{parent.name}> | Class: {parent.get('class')} | Text: {tag.strip()[:40]}")

print("\n" + "=" * 60)
print("🔍 SEARCHING FOR PRODUCT TITLES (Samsung)")
print("=" * 60)
title_tags = soup.find_all(string=lambda t: t and "Samsung" in t)
for tag in title_tags[:10]:
    parent = tag.parent
    print(f"Tag: <{parent.name}> | Class: {parent.get('class')} | Text: {tag.strip()[:60]}")

print("\n" + "=" * 60)
print("🔍 SEARCHING FOR PRODUCT LINKS")
print("=" * 60)
links = soup.find_all("a", href=lambda h: h and "snapdeal.com/product" in h)
for link in links[:5]:
    print(f"Class: {link.get('class')} | href: {link['href'][:70]}")
    