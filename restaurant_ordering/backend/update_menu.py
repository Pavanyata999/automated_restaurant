import json

# Read the app.py file
with open('app.py', 'r') as f:
    content = f.read()

# Replace the Veg Manchurian image URL
old_url = '"image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop",'
new_url = '"image": "https://imgur.com/upload",'  # Placeholder - we'll use a data URL approach

# For now, let's update with a direct image URL
# Since we can't directly upload, we'll use the image data approach
content = content.replace(
    '{"id": 1, "name": "Veg Manchurian", "price": 160, "category": "Starters (Veg)", "available": True, "description": "Crispy vegetable balls in tangy sauce", "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop"}',
    '{"id": 1, "name": "Veg Manchurian", "price": 160, "category": "Starters (Veg)", "available": True, "description": "Crispy vegetable balls in tangy sauce", "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop"}'
)

with open('app.py', 'w') as f:
    f.write(content)

print("Menu updated!")
