# Seed Templates Import Fix

## The Problem

When running `python src/seed_templates.py` from the backend directory, you got:
```
ModuleNotFoundError: No module named 'src'
```

This happens because Python doesn't automatically recognize the `src` directory as a module when running scripts from the parent directory.

## The Solution

I've fixed the import paths in `seed_templates.py` to work correctly when run from the backend directory.

### Changes Made:

1. **Added sys.path manipulation**:
   ```python
   import sys
   sys.path.append(os.path.dirname(os.path.abspath(__file__)))
   ```

2. **Fixed imports**:
   - Changed `from src.models.content import db, Template` 
   - To `from models.content import db, Template`

3. **Fixed main import**:
   - Changed `from src.main import app`
   - To `from main import app`

## How to Use

### Method 1: Direct Python Command
```bash
cd C:\ContentCraftPro\backend
venv\Scripts\activate
python src\seed_templates.py
```

### Method 2: Use the Batch File (Easier)
```bash
cd C:\ContentCraftPro\backend
seed_templates.bat
```

The batch file automatically:
- Activates the virtual environment
- Runs the seed script
- Shows success message

## What This Does

The seed script populates your database with:
- **Social Media Templates** (Facebook, Instagram, Twitter posts)
- **Email Campaign Templates** (Newsletters, promotions)
- **Digital Ad Templates** (Google Ads, Facebook Ads)

These templates give your users professional starting points for their content creation.

## Expected Output

When successful, you'll see:
```
Successfully seeded [number] templates
```

## Verification

After seeding, you can verify the templates were added by:
1. Starting your Flask app: `python src/main.py`
2. Opening the frontend: http://localhost:3000
3. Going to the Templates section
4. You should see all the professional templates available

## If You Still Have Issues

If you encounter any other import errors, make sure:
1. You're in the `backend` directory
2. Your virtual environment is activated
3. All packages are installed: `pip install -r requirements.txt`

The import paths are now fixed to work correctly with your directory structure.

