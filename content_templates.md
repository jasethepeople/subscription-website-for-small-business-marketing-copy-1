# Digital Marketing Content Templates

This file contains a collection of template definitions for various digital marketing content types. These templates will be used to seed the database with initial content that small business owners can customize.

## Social Media Post Templates

```json
[
  {
    "category": "social",
    "name": "Product Showcase",
    "description": "Highlight a product or service with an eye-catching image and compelling description",
    "structure_json": {
      "template_type": "product_showcase",
      "fields": [
        {
          "name": "headline",
          "type": "text",
          "max_length": 80,
          "placeholder": "Introducing our bestselling product"
        },
        {
          "name": "description",
          "type": "textarea",
          "max_length": 280,
          "placeholder": "Describe what makes your product special and why customers need it"
        },
        {
          "name": "call_to_action",
          "type": "text",
          "max_length": 30,
          "placeholder": "Shop Now"
        },
        {
          "name": "product_image",
          "type": "image",
          "aspect_ratio": "1:1"
        }
      ],
      "platforms": ["facebook", "instagram", "linkedin"]
    },
    "thumbnail_url": "/static/templates/thumbnails/product_showcase.jpg",
    "is_premium": false
  },
  {
    "category": "social",
    "name": "Customer Testimonial",
    "description": "Share positive feedback from your customers to build trust",
    "structure_json": {
      "template_type": "testimonial",
      "fields": [
        {
          "name": "customer_quote",
          "type": "textarea",
          "max_length": 200,
          "placeholder": "\"This product changed my life! I can't imagine going back to what I used before.\""
        },
        {
          "name": "customer_name",
          "type": "text",
          "max_length": 50,
          "placeholder": "Jane Smith"
        },
        {
          "name": "customer_title",
          "type": "text",
          "max_length": 100,
          "placeholder": "CEO, Smith Enterprises"
        },
        {
          "name": "background_image",
          "type": "image",
          "aspect_ratio": "16:9"
        }
      ],
      "platforms": ["facebook", "instagram", "linkedin", "twitter"]
    },
    "thumbnail_url": "/static/templates/thumbnails/testimonial.jpg",
    "is_premium": false
  },
  {
    "category": "social",
    "name": "Limited Time Offer",
    "description": "Create urgency with a special promotion or limited-time discount",
    "structure_json": {
      "template_type": "promotion",
      "fields": [
        {
          "name": "offer_headline",
          "type": "text",
          "max_length": 80,
          "placeholder": "FLASH SALE: 24 HOURS ONLY!"
        },
        {
          "name": "offer_details",
          "type": "textarea",
          "max_length": 200,
          "placeholder": "Get 25% off all products with code FLASH25"
        },
        {
          "name": "expiration",
          "type": "text",
          "max_length": 50,
          "placeholder": "Offer ends tonight at midnight"
        },
        {
          "name": "promotion_image",
          "type": "image",
          "aspect_ratio": "4:5"
        }
      ],
      "platforms": ["facebook", "instagram", "twitter"]
    },
    "thumbnail_url": "/static/templates/thumbnails/limited_offer.jpg",
    "is_premium": false
  },
  {
    "category": "social",
    "name": "Industry Tip",
    "description": "Share valuable expertise to position your business as an industry leader",
    "structure_json": {
      "template_type": "tip",
      "fields": [
        {
          "name": "tip_headline",
          "type": "text",
          "max_length": 100,
          "placeholder": "Pro Tip: How to maximize your results"
        },
        {
          "name": "tip_content",
          "type": "textarea",
          "max_length": 300,
          "placeholder": "Share a valuable tip that demonstrates your expertise"
        },
        {
          "name": "tip_image",
          "type": "image",
          "aspect_ratio": "1:1"
        }
      ],
      "platforms": ["facebook", "instagram", "linkedin", "twitter"]
    },
    "thumbnail_url": "/static/templates/thumbnails/industry_tip.jpg",
    "is_premium": false
  },
  {
    "category": "social",
    "name": "Behind the Scenes",
    "description": "Show the human side of your business with behind-the-scenes content",
    "structure_json": {
      "template_type": "behind_scenes",
      "fields": [
        {
          "name": "headline",
          "type": "text",
          "max_length": 80,
          "placeholder": "A peek behind the curtain"
        },
        {
          "name": "story",
          "type": "textarea",
          "max_length": 280,
          "placeholder": "Share what goes into making your product or service special"
        },
        {
          "name": "behind_scenes_image",
          "type": "image",
          "aspect_ratio": "4:5"
        }
      ],
      "platforms": ["facebook", "instagram", "linkedin"]
    },
    "thumbnail_url": "/static/templates/thumbnails/behind_scenes.jpg",
    "is_premium": true
  }
]
```

## Email Marketing Templates

```json
[
  {
    "category": "email",
    "name": "Welcome Email",
    "description": "Introduce new subscribers to your business and what they can expect",
    "structure_json": {
      "template_type": "welcome_email",
      "fields": [
        {
          "name": "subject_line",
          "type": "text",
          "max_length": 100,
          "placeholder": "Welcome to [Your Business] - We're glad you're here!"
        },
        {
          "name": "greeting",
          "type": "text",
          "max_length": 100,
          "placeholder": "Hi [First Name],"
        },
        {
          "name": "intro_paragraph",
          "type": "textarea",
          "max_length": 500,
          "placeholder": "Thank you for subscribing to our newsletter! We're excited to have you join our community."
        },
        {
          "name": "what_to_expect",
          "type": "textarea",
          "max_length": 800,
          "placeholder": "Here's what you can expect from us..."
        },
        {
          "name": "cta_button_text",
          "type": "text",
          "max_length": 30,
          "placeholder": "Explore Our Products"
        },
        {
          "name": "cta_button_url",
          "type": "text",
          "max_length": 500,
          "placeholder": "https://yourbusiness.com/products"
        },
        {
          "name": "header_image",
          "type": "image",
          "aspect_ratio": "2:1"
        }
      ]
    },
    "thumbnail_url": "/static/templates/thumbnails/welcome_email.jpg",
    "is_premium": false
  },
  {
    "category": "email",
    "name": "Product Announcement",
    "description": "Announce a new product or service to your email subscribers",
    "structure_json": {
      "template_type": "product_announcement",
      "fields": [
        {
          "name": "subject_line",
          "type": "text",
          "max_length": 100,
          "placeholder": "Introducing Our Newest [Product/Service]!"
        },
        {
          "name": "headline",
          "type": "text",
          "max_length": 150,
          "placeholder": "Meet [Product Name]: The Solution You've Been Waiting For"
        },
        {
          "name": "product_description",
          "type": "textarea",
          "max_length": 800,
          "placeholder": "Describe your new product or service and its key benefits"
        },
        {
          "name": "feature_list",
          "type": "textarea",
          "max_length": 500,
          "placeholder": "• Feature 1\n• Feature 2\n• Feature 3"
        },
        {
          "name": "pricing_info",
          "type": "textarea",
          "max_length": 300,
          "placeholder": "Available now starting at $XX"
        },
        {
          "name": "cta_button_text",
          "type": "text",
          "max_length": 30,
          "placeholder": "Shop Now"
        },
        {
          "name": "cta_button_url",
          "type": "text",
          "max_length": 500,
          "placeholder": "https://yourbusiness.com/new-product"
        },
        {
          "name": "product_image",
          "type": "image",
          "aspect_ratio": "1:1"
        }
      ]
    },
    "thumbnail_url": "/static/templates/thumbnails/product_announcement.jpg",
    "is_premium": true
  },
  {
    "category": "email",
    "name": "Special Promotion",
    "description": "Promote a special offer or discount to drive sales",
    "structure_json": {
      "template_type": "promotion_email",
      "fields": [
        {
          "name": "subject_line",
          "type": "text",
          "max_length": 100,
          "placeholder": "Special Offer Inside: Save 25% This Week Only!"
        },
        {
          "name": "headline",
          "type": "text",
          "max_length": 150,
          "placeholder": "SAVE 25% ON EVERYTHING"
        },
        {
          "name": "offer_details",
          "type": "textarea",
          "max_length": 500,
          "placeholder": "For a limited time, enjoy 25% off your entire purchase"
        },
        {
          "name": "promo_code",
          "type": "text",
          "max_length": 30,
          "placeholder": "SAVE25"
        },
        {
          "name": "expiration_date",
          "type": "text",
          "max_length": 50,
          "placeholder": "Offer valid through [Date]"
        },
        {
          "name": "cta_button_text",
          "type": "text",
          "max_length": 30,
          "placeholder": "Shop Now"
        },
        {
          "name": "cta_button_url",
          "type": "text",
          "max_length": 500,
          "placeholder": "https://yourbusiness.com/sale"
        },
        {
          "name": "promotion_image",
          "type": "image",
          "aspect_ratio": "16:9"
        }
      ]
    },
    "thumbnail_url": "/static/templates/thumbnails/special_promotion.jpg",
    "is_premium": false
  }
]
```

## Digital Ad Templates

```json
[
  {
    "category": "ad",
    "name": "Product Spotlight Ad",
    "description": "Showcase a specific product with a clean, focused design",
    "structure_json": {
      "template_type": "product_ad",
      "fields": [
        {
          "name": "headline",
          "type": "text",
          "max_length": 40,
          "placeholder": "Meet Your New Favorite [Product]"
        },
        {
          "name": "description",
          "type": "textarea",
          "max_length": 125,
          "placeholder": "Brief description highlighting key benefits"
        },
        {
          "name": "price",
          "type": "text",
          "max_length": 20,
          "placeholder": "$XX.XX"
        },
        {
          "name": "call_to_action",
          "type": "text",
          "max_length": 20,
          "placeholder": "Shop Now"
        },
        {
          "name": "product_image",
          "type": "image",
          "aspect_ratio": "1:1"
        }
      ],
      "platforms": ["facebook", "instagram", "google"]
    },
    "thumbnail_url": "/static/templates/thumbnails/product_ad.jpg",
    "is_premium": false
  },
  {
    "category": "ad",
    "name": "Brand Awareness Ad",
    "description": "Increase brand recognition with a visually striking ad",
    "structure_json": {
      "template_type": "brand_ad",
      "fields": [
        {
          "name": "headline",
          "type": "text",
          "max_length": 50,
          "placeholder": "Discover the [Your Brand] Difference"
        },
        {
          "name": "tagline",
          "type": "text",
          "max_length": 100,
          "placeholder": "Your catchy brand tagline goes here"
        },
        {
          "name": "description",
          "type": "textarea",
          "max_length": 150,
          "placeholder": "Brief description of your brand's unique value proposition"
        },
        {
          "name": "call_to_action",
          "type": "text",
          "max_length": 20,
          "placeholder": "Learn More"
        },
        {
          "name": "brand_image",
          "type": "image",
          "aspect_ratio": "16:9"
        }
      ],
      "platforms": ["facebook", "instagram", "google", "linkedin"]
    },
    "thumbnail_url": "/static/templates/thumbnails/brand_ad.jpg",
    "is_premium": true
  },
  {
    "category": "ad",
    "name": "Limited Time Offer Ad",
    "description": "Create urgency with a time-sensitive promotion",
    "structure_json": {
      "template_type": "offer_ad",
      "fields": [
        {
          "name": "headline",
          "type": "text",
          "max_length": 40,
          "placeholder": "24-HOUR FLASH SALE"
        },
        {
          "name": "offer_details",
          "type": "text",
          "max_length": 80,
          "placeholder": "Save 30% on all products"
        },
        {
          "name": "expiration",
          "type": "text",
          "max_length": 40,
          "placeholder": "Today Only!"
        },
        {
          "name": "call_to_action",
          "type": "text",
          "max_length": 20,
          "placeholder": "Shop Now"
        },
        {
          "name": "offer_image",
          "type": "image",
          "aspect_ratio": "4:5"
        }
      ],
      "platforms": ["facebook", "instagram", "google"]
    },
    "thumbnail_url": "/static/templates/thumbnails/offer_ad.jpg",
    "is_premium": false
  }
]
```
