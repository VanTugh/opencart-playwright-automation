#!/usr/bin/env python3
"""
Script to refactor JSON file and fix all null Use Case values
Logic: For entries with null Use Case, inherit from nearest preceding entry with matching UC code
"""
import json
from pathlib import Path


def fix_use_case_values(json_file):
    """
    Fix all null Use Case values in the JSON file

    Args:
        json_file: Path to the JSON file
    """

    # Read the JSON file
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Dictionary to store Use Case descriptions by UC code or type
    use_case_cache = {}

    # First pass: Build cache of Use Case descriptions
    for entry in data:
        use_case = entry.get('Use Case')
        tc_id = entry.get('TC ID', '')

        if use_case and use_case != 'null':  # Extract UC code from Use Case
            # For standard UC codes (UC_01, UC_02, etc.)
            if use_case.startswith('UC_'):
                uc_code = use_case.split(':')[0].strip()
            else:
                # For special cases like "Security" or "Log check"
                uc_code = use_case.strip()

            use_case_cache[uc_code] = use_case

    # Second pass: Fix null values
    fixed_count = 0
    for entry in data:
        tc_id = entry.get('TC ID', '')
        use_case = entry.get('Use Case')

        # If Use Case is null
        if use_case is None or use_case == 'null' or use_case == '':
            # Extract UC code from TC ID (TC_01_01 -> UC_01, TC_LOG_02 -> Log check)
            if tc_id and '_' in tc_id:
                parts = tc_id.split('_')

                # Handle special prefixes (SEC, LOG)
                if parts[0] in ['TC'] and len(parts) >= 2:
                    prefix = parts[1].upper()

                    if prefix == 'SEC':
                        # Security test
                        if 'Security' in use_case_cache:
                            entry['Use Case'] = use_case_cache['Security']
                            fixed_count += 1
                            print(f"✓ Fixed {tc_id}: Assigned '{entry['Use Case']}'")
                        else:
                            print(f"⚠️  Warning: No Use Case description found for Security (TC: {tc_id})")
                    elif prefix == 'LOG':
                        # Log check test
                        if 'Log check' in use_case_cache:
                            entry['Use Case'] = use_case_cache['Log check']
                            fixed_count += 1
                            print(f"✓ Fixed {tc_id}: Assigned '{entry['Use Case']}'")
                        else:
                            print(f"⚠️  Warning: No Use Case description found for Log check (TC: {tc_id})")
                    else:
                        # Standard UC code (UC_01, UC_02, etc.)
                        uc_code = f'UC_{prefix}'

                        # Get the full Use Case string from cache
                        if uc_code in use_case_cache:
                            entry['Use Case'] = use_case_cache[uc_code]
                            fixed_count += 1
                            print(f"✓ Fixed {tc_id}: Assigned '{entry['Use Case']}'")
                        else:
                            print(f"⚠️  Warning: No Use Case description found for {uc_code} (TC: {tc_id})")
            else:
                print(f"⚠️  Warning: Cannot parse TC ID: {tc_id}")

    print(f"\n📊 Summary: Fixed {fixed_count} entries with null Use Case values")

    # Write back to file
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"✅ JSON file updated: {json_file}")

    # Validation: Check if all entries now have Use Case values
    null_count = sum(1 for entry in data if entry.get('Use Case') is None or entry.get('Use Case') == '')

    if null_count == 0:
        print(f"✅ Validation: All {len(data)} entries have Use Case values!")
    else:
        print(f"❌ Validation failed: {null_count} entries still have null Use Case values")

    return fixed_count, null_count


if __name__ == '__main__':
    json_file = Path(__file__).parent / 'OpenCart_203_TestCases_Final.json'

    if json_file.exists():
        print(f"Processing: {json_file}")
        print("=" * 80)
        fixed, remaining = fix_use_case_values(json_file)
        print("=" * 80)
    else:
        print(f"❌ File not found: {json_file}")

