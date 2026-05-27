#!/usr/bin/env python
"""
Utility script to run OpenCart automation tests with various options
"""
import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")


def run_all_tests():
    """Run all tests"""
    print_header("Running All 203 Test Cases")
    cmd = [
        'pytest', 'main.py', '-v',
        '--html=reports/test_report.html',
        '--self-contained-html'
    ]
    subprocess.run(cmd)


def run_high_priority():
    """Run only high priority tests"""
    print_header("Running High Priority Tests")
    cmd = ['pytest', 'main.py', '-m', 'high', '-v']
    subprocess.run(cmd)


def run_by_use_case():
    """Run tests by selected use case"""
    use_cases = {
        '1': ('registration', 'UC_01: Registration'),
        '2': ('login', 'UC_02: Login'),
        '3': ('password', 'UC_03: Password'),
        '4': ('address', 'UC_04: Address'),
        '5': ('wishlist', 'UC_05: Wishlist'),
        '6': ('comparison', 'UC_06: Comparison'),
        '7': ('review', 'UC_07: Review'),
        '8': ('cart', 'UC_08: Cart'),
        '9': ('checkout', 'UC_09: Checkout'),
        '10': ('order', 'UC_10: Order'),
        '11': ('category', 'UC_11: Category'),
        '12': ('product', 'UC_12: Product'),
        '13': ('discount', 'UC_13: Discount'),
        '14': ('coupon', 'UC_14: Coupon'),
        '15': ('category_seo', 'UC_15: Category SEO'),
        '16': ('product_seo', 'UC_16: Product SEO'),
        '17': ('product_attribute', 'UC_17: Attributes'),
        '18': ('product_related', 'UC_18: Related'),
        '19': ('currency', 'UC_19: Currency'),
        '20': ('customer_group', 'UC_20: Customer Group'),
    }
    
    print_header("Select Use Case to Test")
    for key, (_, name) in use_cases.items():
        print(f"  {key:2s} - {name}")
    print(f"  0  - Back to Main Menu")
    
    choice = input("\nEnter your choice: ").strip()
    
    if choice == '0':
        return
    
    if choice in use_cases:
        marker, name = use_cases[choice]
        print_header(f"Running {name} Tests")
        cmd = ['pytest', 'main.py', '-m', marker, '-v']
        subprocess.run(cmd)
    else:
        print("Invalid choice!")


def run_parallel():
    """Run tests in parallel"""
    print_header("Running Tests in Parallel")
    
    workers = input("Enter number of parallel workers (default 4): ").strip() or '4'
    
    cmd = ['pytest', 'main.py', '-n', workers, '-v']
    subprocess.run(cmd)


def run_with_logging():
    """Run tests with verbose logging"""
    print_header("Running Tests with Verbose Logging")
    cmd = [
        'pytest', 'main.py', '-vv',
        '--log-cli-level=DEBUG',
        '--html=reports/test_report.html',
        '--self-contained-html'
    ]
    subprocess.run(cmd)


def run_specific_test():
    """Run a specific test case"""
    print_header("Run Specific Test Case")
    tc_id = input("Enter TC ID (e.g., TC_01_01): ").strip()
    
    if not tc_id:
        return
    
    print_header(f"Running Test Case: {tc_id}")
    cmd = ['pytest', 'main.py', '-k', tc_id, '-v']
    subprocess.run(cmd)


def check_reports():
    """Open test reports"""
    print_header("Opening Test Reports")
    
    report_path = Path('reports/test_report.html')
    
    if report_path.exists():
        print(f"Report location: {report_path.absolute()}")
        try:
            import webbrowser
            webbrowser.open(f'file://{report_path.absolute()}')
            print("✓ Report opened in browser")
        except:
            print(f"Please open manually: {report_path.absolute()}")
    else:
        print("No report found. Run tests first!")


def check_failures():
    """Check failed test screenshots"""
    print_header("Failed Test Screenshots")
    
    failures_dir = Path('failures')
    if failures_dir.exists():
        screenshots = list(failures_dir.glob('*.png'))
        if screenshots:
            print(f"Found {len(screenshots)} failure screenshots:")
            for i, ss in enumerate(screenshots[-10:], 1):  # Show last 10
                print(f"  {i}. {ss.name}")
        else:
            print("No failure screenshots found!")
    else:
        print("Failures directory not found. Run tests first!")


def check_logs():
    """View test logs"""
    print_header("Test Execution Logs")
    
    log_path = Path('logs/automation.log')
    if log_path.exists():
        print(f"Log location: {log_path.absolute()}")
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Show last 50 lines
            start_idx = max(0, len(lines) - 50)
            print("\n--- Last 50 lines of log ---\n")
            for line in lines[start_idx:]:
                print(line.rstrip())
        except Exception as e:
            print(f"Error reading log: {e}")
    else:
        print("No logs found. Run tests first!")


def install_dependencies():
    """Install required dependencies"""
    print_header("Installing Dependencies")
    
    # Install Python packages
    print("Installing Python packages...")
    subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
    
    # Install Playwright browsers
    print("\nInstalling Playwright browsers...")
    subprocess.run(['playwright', 'install', 'chromium'])
    
    print("\n✓ Installation complete!")


def setup_environment():
    """Setup environment"""
    print_header("Setting Up Environment")
    
    # Create necessary directories
    dirs = ['logs', 'reports', 'failures']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✓ Created {dir_name} directory")
    
    print("\n✓ Environment setup complete!")


def main_menu():
    """Display main menu"""
    while True:
        print_header("OpenCart Automation Testing Framework")
        print("""
  Test Execution:
    1  - Run all 203 test cases
    2  - Run high priority tests only
    3  - Run by use case (UC_01-UC_20)
    4  - Run tests in parallel
    5  - Run with verbose logging
    6  - Run specific test case
  
  Reports & Logs:
    7  - View test report
    8  - Check failed screenshots
    9  - View test logs
  
  Setup:
    10 - Install dependencies
    11 - Setup environment
    
    0  - Exit
        """)
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            run_all_tests()
        elif choice == '2':
            run_high_priority()
        elif choice == '3':
            run_by_use_case()
        elif choice == '4':
            run_parallel()
        elif choice == '5':
            run_with_logging()
        elif choice == '6':
            run_specific_test()
        elif choice == '7':
            check_reports()
        elif choice == '8':
            check_failures()
        elif choice == '9':
            check_logs()
        elif choice == '10':
            install_dependencies()
        elif choice == '11':
            setup_environment()
        elif choice == '0':
            print("\nGoodbye! 👋\n")
            break
        else:
            print("Invalid choice! Please try again.")
        
        input("\nPress Enter to continue...")


if __name__ == '__main__':
    # Check if pytest is installed
    try:
        import pytest
    except ImportError:
        print("\n⚠️  Pytest not installed. Installing dependencies...")
        install_dependencies()
    
    # Setup environment if needed
    if not Path('logs').exists():
        setup_environment()
    
    # Show menu
    main_menu()

