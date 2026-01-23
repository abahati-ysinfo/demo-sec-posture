# Browser-Based UI Testing

Automated browser testing for the Security Posture Assessment Tool production site.

## What This Tests

These tests open a **real browser** and interact with your **production website**:
- URL: https://echostor-security-posture-tool.vercel.app/
- Clicks buttons, fills forms, navigates pages
- Simulates real user behavior
- Tests the complete user journey

## Quick Start

### 1. Install Dependencies

```bash
cd tests/
pip install -r requirements.txt
playwright install chromium
```

### 2. Run Tests

```bash
# Run with visible browser (recommended first time)
pytest --headed

# Run in headless mode (faster, no browser window)
pytest

# Run specific test
pytest ui_tests/test_happy_path_ui.py

# Run with slower actions (easier to watch)
pytest --headed --slowmo=1000
```

## What Gets Tested

### Happy Path Test (`test_happy_path_ui.py`)

**Complete assessment flow:**
1. Opens https://echostor-security-posture-tool.vercel.app/
2. Registers a new test user (auto-generated email)
3. Starts a new assessment
4. Answers ALL questions with random selections
5. Fills consultation details (200-300 words)
6. Completes the assessment
7. Verifies report is generated

**Runtime:** ~10-15 minutes (answers 400+ questions)

## Test Output

```
================================================================================
BROWSER UI TEST - HAPPY PATH
Testing: https://echostor-security-posture-tool.vercel.app
Test User: test_abc12345@echostor-test.com
================================================================================

[1/7] Navigating to production site...
✓ Site loaded

[2/7] Registering new user...
✓ User registered and logged in

[3/7] Starting new assessment...
✓ Assessment started

[4/7] Answering all questions...
  Progress: 10 questions answered
  Progress: 20 questions answered
  ...
  Progress: 400 questions answered
  Reached consultation question after 409 questions
✓ All 409 questions answered

[5/7] Answering consultation question...
✓ Consultation details provided

[6/7] Completing assessment...
✓ Assessment completed

[7/7] Navigating to reports...
✓ Report generated

================================================================================
✅ HAPPY PATH TEST PASSED
================================================================================
```

## Configuration

Edit `pytest.ini` to customize:

```ini
[pytest]
addopts = 
    --headed              # Show browser (remove for headless)
    --slowmo=500          # Slow down actions by 500ms
    --screenshot=only-on-failure
    --video=retain-on-failure
```

## Command Line Options

```bash
# Show browser window
pytest --headed

# Run headless (no browser window)
pytest

# Slow down actions (milliseconds)
pytest --headed --slowmo=1000

# Take screenshots on failure
pytest --screenshot=only-on-failure

# Record video on failure
pytest --video=retain-on-failure

# Run specific browser
pytest --browser=chromium  # or firefox, webkit
```

## Troubleshooting

### "Playwright not installed"
```bash
playwright install chromium
```

### "Test times out"
- Check if production site is accessible
- Increase timeout in test code
- Check your internet connection

### "Element not found"
- Production site UI may have changed
- Update selectors in test code
- Run with `--headed --slowmo=1000` to debug

### Test fails at registration
- Email might already exist (tests auto-generate unique emails)
- Check if registration is working on production site

## Adding More Tests

Create new test files in `ui_tests/`:

```python
# ui_tests/test_my_feature.py
from playwright.sync_api import Page

def test_my_feature(page: Page):
    page.goto("https://echostor-security-posture-tool.vercel.app")
    # Your test code here
```

## CI/CD Integration

```yaml
# .github/workflows/ui-tests.yml
name: UI Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd tests
          pip install -r requirements.txt
          playwright install chromium
      
      - name: Run UI tests
        run: |
          cd tests
          pytest
```

## Best Practices

1. **Run before deployments** - Catch issues before users do
2. **Check test output** - Review what the test is doing
3. **Use --headed first time** - Watch the browser to understand the test
4. **Keep tests updated** - Update selectors if UI changes
5. **Monitor test duration** - Track how long tests take over time

## Notes

- Tests create real user accounts on production (email: test_*@echostor-test.com)
- Each test run uses a unique email to avoid conflicts
- Tests interact with real production data
- Reports are actually generated on production
- Consider cleanup of test data periodically

## Support

If tests fail:
1. Run with `--headed --slowmo=1000` to watch what's happening
2. Check if production site is accessible
3. Verify UI elements haven't changed
4. Check browser console for errors (in headed mode)
