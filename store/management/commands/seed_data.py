"""
store/management/commands/seed_data.py

CONCEPT 14 (PYTHON BASICS - CLASSES, LOOPS & CONDITIONS):
Custom Django management command to seed the database with initial categories,
12 sample clothing products, and generate realistic local placeholder images using Pillow.

To execute:
python manage.py seed_data
"""

import os
import sys
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
from store.models import Category, Product


class Command(BaseCommand):
    help = 'Seeds categories and 12 sample clothing products with local placeholder images'

    def handle(self, *args, **options):
        for out in (sys.stdout, getattr(self.stdout, '_out', None)):
            if out and hasattr(out, 'reconfigure'):
                try:
                    out.reconfigure(encoding='utf-8')
                except Exception:
                    pass
        self.stdout.write(self.style.SUCCESS("Starting database seeding for ClothStore..."))

        # Ensure media/products/ folder exists
        # CONCEPT 12 (MEDIA): Stored in MEDIA_ROOT for user/admin uploaded files
        media_products_dir = os.path.join(settings.MEDIA_ROOT, 'products')
        os.makedirs(media_products_dir, exist_ok=True)

        # ----------------------------------------------------------------------
        # 1. CREATE CATEGORIES
        # ----------------------------------------------------------------------
        categories_data = [
            {'name': 'Formal & Workwear', 'slug': 'formal-wear'},
            {'name': 'Casuals & Denim', 'slug': 'casuals-denim'},
            {'name': 'Athleisure & Comfort', 'slug': 'athleisure-comfort'},
        ]

        # CONCEPT 14 (PYTHON BASICS - DICTIONARY & LOOP):
        # We store categories in a dictionary and iterate with a for-loop
        category_objects = {}
        for cat_info in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_info['slug'],
                defaults={'name': cat_info['name']}
            )
            category_objects[cat_info['slug']] = cat
            if created:
                self.stdout.write(f"  + Created Category: {cat.name}")
            else:
                self.stdout.write(f"  * Existing Category: {cat.name}")

        # ----------------------------------------------------------------------
        # 2. DEFINE 12 SAMPLE PRODUCTS
        # ----------------------------------------------------------------------
        sample_products = [
            # Formal & Workwear
            {
                'name': 'Classic Oxford Cotton Shirt',
                'slug': 'classic-oxford-cotton-shirt',
                'category_slug': 'formal-wear',
                'price': Decimal('1499.00'),
                'stock': 15,
                'size': 'M',
                'gender': 'Men',
                'description': 'A timeless button-down shirt cut from breathable 100% combed Oxford cotton. Designed with a structured collar, tailored cuffs, and pre-washed softness suitable for boardroom meetings or casual dinners.',
                'bg_color': (24, 43, 73),      # Navy
                'accent_color': (212, 175, 55), # Gold
            },
            {
                'name': 'Tailored Slim-Fit Blazer',
                'slug': 'tailored-slim-fit-blazer',
                'category_slug': 'formal-wear',
                'price': Decimal('3999.00'),
                'stock': 8,
                'size': 'L',
                'gender': 'Men',
                'description': 'Sharply tailored single-breasted blazer featuring notch lapels, structured shoulder padding, and silk lining. Elevate any formal trouser or premium denim outfit effortlessly.',
                'bg_color': (33, 37, 41),      # Charcoal
                'accent_color': (255, 255, 255),
            },
            {
                'name': 'Silk Pleated Evening Blouse',
                'slug': 'silk-pleated-evening-blouse',
                'category_slug': 'formal-wear',
                'price': Decimal('1899.00'),
                'stock': 12,
                'size': 'S',
                'gender': 'Women',
                'description': 'Flowing and elegant evening blouse made from gentle silk-blend chiffon. Features delicate front pleats, buttoned cuffs, and an airy silhouette for formal occasions.',
                'bg_color': (98, 30, 48),      # Wine / Burgundy
                'accent_color': (255, 230, 235),
            },
            {
                'name': 'Tailored High-Waist Trousers',
                'slug': 'tailored-high-waist-trousers',
                'category_slug': 'formal-wear',
                'price': Decimal('1999.00'),
                'stock': 10,
                'size': 'M',
                'gender': 'Women',
                'description': 'Smart ankle-length high-rise trousers with crisp front center creases and side slash pockets. Perfect match with crisp blouses and professional blazers.',
                'bg_color': (67, 76, 94),      # Slate Slate
                'accent_color': (229, 233, 240),
            },

            # Casuals & Denim
            {
                'name': 'Vintage Denim Trucker Jacket',
                'slug': 'vintage-denim-trucker-jacket',
                'category_slug': 'casuals-denim',
                'price': Decimal('2499.00'),
                'stock': 14,
                'size': 'L',
                'gender': 'Men',
                'description': 'Rugged 13.5oz authentic indigo denim jacket with shank brass buttons, dual chest flap pockets, and waist adjusters. Washed for authentic vintage patina.',
                'bg_color': (44, 82, 130),     # Indigo Denim
                'accent_color': (254, 215, 126),
            },
            {
                'name': 'Heavyweight Boxy Crewneck Tee',
                'slug': 'heavyweight-boxy-crewneck-tee',
                'category_slug': 'casuals-denim',
                'price': Decimal('799.00'),
                'stock': 25,
                'size': 'M',
                'gender': 'Men',
                'description': '240 GSM organic cotton heavyweight t-shirt featuring a relaxed boxy cut, ribbed crew neckline, and drop shoulders for street-style comfort.',
                'bg_color': (74, 85, 104),     # Heather Steel
                'accent_color': (255, 255, 255),
            },
            {
                'name': 'Relaxed Straight-Leg Jeans',
                'slug': 'relaxed-straight-leg-jeans',
                'category_slug': 'casuals-denim',
                'price': Decimal('2199.00'),
                'stock': 18,
                'size': 'S',
                'gender': 'Women',
                'description': 'High-rise relaxed straight leg jeans crafted from 100% sustainable denim. Provides comfortable room through the hip and thigh with modern clean aesthetics.',
                'bg_color': (49, 130, 206),    # Medium Blue Denim
                'accent_color': (255, 255, 255),
            },
            {
                'name': 'Oversized Cotton Knit Sweater',
                'slug': 'oversized-cotton-knit-sweater',
                'category_slug': 'casuals-denim',
                'price': Decimal('1699.00'),
                'stock': 9,
                'size': 'M',
                'gender': 'Women',
                'description': 'Cozy chunky knit sweater woven from 100% combed cotton yarn. Soft against bare skin with ribbed cuffs, hem, and a flattering slouchy drape.',
                'bg_color': (183, 121, 64),    # Warm Camel
                'accent_color': (254, 243, 199),
            },
            {
                'name': 'Kids Dino Graphic Raglan Tee',
                'slug': 'kids-dino-graphic-raglan-tee',
                'category_slug': 'casuals-denim',
                'price': Decimal('499.00'),
                'stock': 20,
                'size': 'S',
                'gender': 'Kids',
                'description': 'Fun dinosaur graphic t-shirt featuring contrast two-tone raglan sleeves. Made from ultra-soft tagless cotton to keep active kids comfortable all day.',
                'bg_color': (40, 167, 69),     # Meadow Green
                'accent_color': (255, 255, 255),
            },
            {
                'name': 'Kids Denim Overalls Dungaree',
                'slug': 'kids-denim-overalls-dungaree',
                'category_slug': 'casuals-denim',
                'price': Decimal('1199.00'),
                'stock': 11,
                'size': 'M',
                'gender': 'Kids',
                'description': 'Durable cotton denim overalls with adjustable shoulder buckle straps, multi-tool chest pocket, and reinforced knee stitching for active play.',
                'bg_color': (30, 64, 175),     # Royal Navy
                'accent_color': (251, 191, 36),
            },

            # Athleisure & Comfort
            {
                'name': 'Performance Tech Fleece Hoodie',
                'slug': 'performance-tech-fleece-hoodie',
                'category_slug': 'athleisure-comfort',
                'price': Decimal('1899.00'),
                'stock': 16,
                'size': 'L',
                'gender': 'Men',
                'description': 'Thermal lightweight tech fleece hoodie with dual-layered scuba hood, kangaroo zip pockets, and moisture-wicking technology for workouts or travel.',
                'bg_color': (15, 23, 42),      # Dark Obsidian
                'accent_color': (56, 189, 248), # Sky Blue
            },
            {
                'name': 'Seamless High-Waist Yoga Leggings',
                'slug': 'seamless-high-waist-yoga-leggings',
                'category_slug': 'athleisure-comfort',
                'price': Decimal('1299.00'),
                'stock': 22,
                'size': 'S',
                'gender': 'Women',
                'description': 'Buttery-soft four-way stretch leggings with a compressive ribbed waistband. Squat-proof, breathable, and designed for unrestricted mobility in yoga and running.',
                'bg_color': (76, 29, 149),     # Deep Plum / Violet
                'accent_color': (244, 114, 182),
            },
        ]

        # ----------------------------------------------------------------------
        # 3. HELPER FUNCTION TO GENERATE IMAGES USING PILLOW
        # ----------------------------------------------------------------------
        def generate_mock_image(filepath, title, category_name, gender, bg_color, accent_color):
            """
            Uses Python Pillow library to draw a stylish product mockup card
            saved directly to disk as a JPEG.
            """
            width, height = 600, 720
            img = Image.new('RGB', (width, height), color=bg_color)
            draw = ImageDraw.Draw(img)

            # Draw decorative border inside
            margin = 24
            draw.rectangle(
                [(margin, margin), (width - margin, height - margin)],
                outline=accent_color,
                width=3
            )

            # Draw subtle geometric accent in the background
            draw.ellipse(
                [(width // 2 - 140, 140), (width // 2 + 140, 420)],
                outline=(255, 255, 255, 40),
                width=2
            )

            # Draw top department tag
            tag_text = f"CLOTHSTORE &bull; {gender.upper()} &bull; {category_name.upper()}"
            draw.text((margin + 20, margin + 20), tag_text, fill=accent_color)

            # Draw hanger / apparel icon representation
            center_x, center_y = width // 2, 280
            draw.line([(center_x - 70, center_y + 40), (center_x, center_y), (center_x + 70, center_y + 40)], fill=accent_color, width=4)
            draw.arc([(center_x - 20, center_y - 30), (center_x + 20, center_y + 10)], start=180, end=0, fill=accent_color, width=4)

            # Draw product title and branding text at the lower half
            # Split long title if necessary
            words = title.split()
            lines = []
            cur_line = []
            for w in words:
                cur_line.append(w)
                if len(" ".join(cur_line)) > 20:
                    lines.append(" ".join(cur_line))
                    cur_line = []
            if cur_line:
                lines.append(" ".join(cur_line))

            y_offset = 480
            for line in lines:
                draw.text((width // 2 - 180, y_offset), line, fill=(255, 255, 255))
                y_offset += 30

            draw.text((width // 2 - 180, y_offset + 15), "PREMIUM QUALITY APPAREL", fill=accent_color)

            # Save JPEG image to disk
            img.save(filepath, format='JPEG', quality=90)

        # ----------------------------------------------------------------------
        # 4. LOOP AND CREATE PRODUCT RECORDS
        # ----------------------------------------------------------------------
        for p in sample_products:
            # 1. Reference real photo (.jpeg) if present in media/products
            jpeg_filename = f"{p['slug']}.jpeg"
            jpeg_full_path = os.path.join(media_products_dir, jpeg_filename)
            jpg_filename = f"{p['slug']}.jpg"
            jpg_full_path = os.path.join(media_products_dir, jpg_filename)

            if os.path.exists(jpeg_full_path):
                rel_image_path = f"products/{jpeg_filename}"
            elif os.path.exists(jpg_full_path):
                rel_image_path = f"products/{jpg_filename}"
            else:
                rel_image_path = f"products/{jpeg_filename}"
                # Only generate placeholder if no photo file exists on disk
                generate_mock_image(
                    filepath=jpeg_full_path,
                    title=p['name'],
                    category_name=category_objects[p['category_slug']].name,
                    gender=p['gender'],
                    bg_color=p['bg_color'],
                    accent_color=p['accent_color']
                )

            # 2. CONCEPT 2 (ORM - GET_OR_CREATE):
            # Creates or updates the Product model in sqlite database
            product, created = Product.objects.get_or_create(
                slug=p['slug'],
                defaults={
                    'category': category_objects[p['category_slug']],
                    'name': p['name'],
                    'description': p['description'],
                    'price': p['price'],
                    'stock': p['stock'],
                    'size': p['size'],
                    'gender': p['gender'],
                    'image': rel_image_path,
                    'is_available': True,
                }
            )

            # Ensure image path and price are updated
            if not created:
                product.price = p['price']
                product.image = rel_image_path
                product.save()

            if created:
                self.stdout.write(f"  + Added Product: {product.name} (₹{product.price})")
            else:
                self.stdout.write(f"  * Updated Product: {product.name} (₹{product.price})")

        self.stdout.write(self.style.SUCCESS("[OK] Seed data completed successfully! 3 categories and 12 products ready."))
