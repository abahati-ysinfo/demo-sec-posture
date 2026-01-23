"""
Browser-based UI test for complete assessment flow on production site
Tests: https://echostor-security-posture-tool.vercel.app/
"""
import random
import time
from playwright.sync_api import Page, expect


def generate_test_email():
    """Generate unique test email"""
    random_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
    return f"test_{random_id}@echostor-test.com"


def generate_password():
    """Generate secure password"""
    return "TestPass123!@#"


def test_complete_assessment_flow(page: Page):
    """
    Complete end-to-end assessment flow:
    1. Navigate to production site
    2. Register new user
    3. Start assessment
    4. Answer all questions
    5. Complete assessment
    6. Generate and download report
    """
    
    BASE_URL = "https://echostor-security-posture-tool.vercel.app"
    test_email = generate_test_email()
    test_password = generate_password()
    
    print(f"\n{'='*80}")
    print(f"BROWSER UI TEST - HAPPY PATH")
    print(f"Testing: {BASE_URL}")
    print(f"Test User: {test_email}")
    print(f"{'='*80}\n")
    
    print("[1/7] Navigating to production site...")
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle")
    print("✓ Site loaded")
    
    print(f"\n[2/7] Registering new user...")
    page.click("text=Register")
    page.fill("input[type='email']", test_email)
    page.fill("input[name='fullName']", "Test User")
    page.fill("input[type='password']", test_password)
    page.click("button:has-text('Register')")
    page.wait_for_url("**/dashboard", timeout=10000)
    print("✓ User registered and logged in")
    
    print(f"\n[3/7] Starting new assessment...")
    page.click("text=Start New Assessment")
    page.wait_for_url("**/assessment/questions", timeout=10000)
    print("✓ Assessment started")
    
    print(f"\n[4/7] Answering all questions...")
    questions_answered = 0
    
    while True:
        if page.locator("text=Consultation Interest").is_visible():
            print(f"  Reached consultation question after {questions_answered} questions")
            break
        
        radio_buttons = page.locator("input[type='radio']").all()
        checkboxes = page.locator("input[type='checkbox']").all()
        
        if radio_buttons:
            random.choice(radio_buttons).click()
        elif checkboxes:
            num_to_select = random.randint(1, min(3, len(checkboxes)))
            for checkbox in random.sample(checkboxes, num_to_select):
                checkbox.click()
        
        questions_answered += 1
        
        if questions_answered % 10 == 0:
            print(f"  Progress: {questions_answered} questions answered")
        
        next_button = page.locator("button:has-text('Next')")
        if next_button.is_enabled():
            next_button.click()
            time.sleep(0.5)  # Small delay for page to update
        else:
            print(f"  Next button disabled, waiting...")
            time.sleep(1)
    
    print(f"✓ All {questions_answered} questions answered")
    
    print(f"\n[5/7] Answering consultation question...")
    page.click("input[value='yes']")  # Click "Yes" for consultation
    
    consultation_text = " ".join([
        "We need comprehensive security consultation for our organization.",
        "Our primary concerns include cloud security architecture, data protection strategies,",
        "incident response planning, and compliance with industry standards.",
        "We are particularly interested in implementing zero trust security model,",
        "enhancing our threat detection capabilities, and establishing robust security governance.",
        "Our team requires guidance on security awareness training programs,",
        "vulnerability management processes, and third-party risk assessment.",
        "We would like to discuss penetration testing methodologies,",
        "security operations center setup, and continuous monitoring solutions.",
        "Additionally, we need assistance with developing comprehensive security policies,",
        "implementing multi-factor authentication across all systems,",
        "and establishing effective backup and disaster recovery procedures.",
        "We are also looking to improve our application security practices,",
        "implement secure software development lifecycle, and enhance our API security.",
        "Our organization needs help with security metrics and KPI development,",
        "security budget planning, and building a mature security program.",
        "We would appreciate consultation on emerging security threats,",
        "best practices for remote work security, and IoT device security management."
    ] * 2)  # Repeat to ensure 200+ words
    
    page.fill("textarea", consultation_text[:1500])  # Limit to reasonable length
    print("✓ Consultation details provided")
    
    print(f"\n[6/7] Completing assessment...")
    page.click("button:has-text('Complete Assessment')")
    
    page.on("dialog", lambda dialog: dialog.accept())
    
    page.wait_for_url("**/dashboard", timeout=15000)
    print("✓ Assessment completed")
    
    print(f"\n[7/7] Navigating to reports...")
    page.click("text=Reports")
    page.wait_for_url("**/reports", timeout=10000)
    
    page.wait_for_selector("text=Standard Report", timeout=30000)
    print("✓ Report generated")
    
    print(f"\n{'='*80}")
    print(f"✅ HAPPY PATH TEST PASSED")
    print(f"{'='*80}\n")
    
    time.sleep(2)
