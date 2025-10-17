"""
Comprehensive MD5 Hash and Integrity Testing Script
Tests all MD5 functionality for Oracle Samuel
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime
import tempfile
import shutil

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

print("=" * 80)
print("ORACLE SAMUEL - MD5 INTEGRITY TESTING SUITE")
print("=" * 80)
print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Test results
test_results = {
    'passed': [],
    'failed': [],
    'warnings': []
}

def test_result(test_name, passed, message=""):
    """Record test result"""
    if passed:
        test_results['passed'].append(test_name)
        print(f"[PASS] {test_name}")
    else:
        test_results['failed'].append(test_name)
        print(f"[FAIL] {test_name}")
    if message:
        print(f"   {message}")
    print()

# =============================================================================
# TEST 1: MD5 Hash Generation from DataFrame
# =============================================================================
print("TEST 1: MD5 Hash Generation from DataFrame")
print("-" * 80)

try:
    from utils.md5_manager import generate_md5_from_dataframe

    # Create test DataFrame
    test_df = pd.DataFrame({
        'price': [100000, 200000, 300000],
        'sqft': [1000, 2000, 3000],
        'bedrooms': [2, 3, 4]
    })

    # Generate MD5 hash
    hash1 = generate_md5_from_dataframe(test_df)

    # Verify hash is valid (32 character hex string)
    if len(hash1) == 32 and all(c in '0123456789abcdef' for c in hash1):
        test_result("MD5 Hash Generation", True, f"Hash: {hash1}")
    else:
        test_result("MD5 Hash Generation", False, f"Invalid hash format: {hash1}")

    # Test consistency - same data should produce same hash
    hash2 = generate_md5_from_dataframe(test_df)

    if hash1 == hash2:
        test_result("MD5 Hash Consistency", True, "Same data produces same hash")
    else:
        test_result("MD5 Hash Consistency", False, "Hash inconsistency detected")

    # Test uniqueness - different data should produce different hash
    modified_df = test_df.copy()
    modified_df.loc[0, 'price'] = 150000
    hash3 = generate_md5_from_dataframe(modified_df)

    if hash1 != hash3:
        test_result("MD5 Hash Uniqueness", True, "Different data produces different hash")
    else:
        test_result("MD5 Hash Uniqueness", False, "Hash collision detected")

except Exception as e:
    test_result("MD5 Hash Generation", False, str(e))

# =============================================================================
# TEST 2: MD5 Signature from File
# =============================================================================
print("TEST 2: MD5 Signature from File")
print("-" * 80)

try:
    from utils.md5_manager import generate_md5_signature

    # Create temporary test file
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
    temp_file.write("Oracle Samuel Test Data")
    temp_file.close()

    # Generate MD5 signature
    file_hash = generate_md5_signature(temp_file.name)

    if len(file_hash) == 32:
        test_result("File MD5 Signature", True, f"Hash: {file_hash}")
    else:
        test_result("File MD5 Signature", False, f"Invalid hash: {file_hash}")

    # Test file consistency
    file_hash2 = generate_md5_signature(temp_file.name)

    if file_hash == file_hash2:
        test_result("File Hash Consistency", True, "Same file produces same hash")
    else:
        test_result("File Hash Consistency", False, "File hash inconsistency")

    # Cleanup
    os.unlink(temp_file.name)

except Exception as e:
    test_result("File MD5 Signature", False, str(e))

# =============================================================================
# TEST 3: Data Integrity Verification
# =============================================================================
print("TEST 3: Data Integrity Verification")
print("-" * 80)

try:
    from utils.md5_manager import generate_md5_from_dataframe, verify_data_integrity

    # Create test DataFrame
    original_df = pd.DataFrame({
        'price': [100000, 200000, 300000],
        'sqft': [1000, 2000, 3000]
    })

    # Generate and store hash
    stored_hash = generate_md5_from_dataframe(original_df)

    # Verify unchanged data
    is_valid = verify_data_integrity(original_df, stored_hash)

    if is_valid:
        test_result("Data Integrity - Unchanged Data", True, "Integrity verified")
    else:
        test_result("Data Integrity - Unchanged Data", False, "Verification failed")

    # Verify modified data is detected
    modified_df = original_df.copy()
    modified_df.loc[0, 'price'] = 999999

    is_tampered = not verify_data_integrity(modified_df, stored_hash)

    if is_tampered:
        test_result("Data Integrity - Tamper Detection", True, "Modification detected")
    else:
        test_result("Data Integrity - Tamper Detection", False, "Failed to detect modification")

except Exception as e:
    test_result("Data Integrity Verification", False, str(e))

# =============================================================================
# TEST 4: Signature Record Creation
# =============================================================================
print("TEST 4: Signature Record Creation")
print("-" * 80)

try:
    from utils.md5_manager import create_signature_record

    # Create signature record
    test_hash = "abc123def456789"
    record = create_signature_record("test_file.csv", test_hash)

    # Verify record structure
    required_fields = ['file_name', 'md5_hash', 'timestamp', 'status']
    has_all_fields = all(field in record for field in required_fields)

    if has_all_fields:
        test_result("Signature Record Creation", True,
                   f"File: {record['file_name']}, Status: {record['status']}")
    else:
        test_result("Signature Record Creation", False, "Missing required fields")

    # Verify timestamp format
    try:
        datetime.strptime(record['timestamp'], '%Y-%m-%d %H:%M:%S')
        test_result("Signature Timestamp Format", True, f"Timestamp: {record['timestamp']}")
    except:
        test_result("Signature Timestamp Format", False, "Invalid timestamp format")

except Exception as e:
    test_result("Signature Record Creation", False, str(e))

# =============================================================================
# TEST 5: ProjectIntegrityChecker Initialization
# =============================================================================
print("TEST 5: ProjectIntegrityChecker Initialization")
print("-" * 80)

try:
    from utils.integrity_checker import ProjectIntegrityChecker

    # Create temp database for testing
    test_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    test_db.close()

    checker = ProjectIntegrityChecker(db_name=test_db.name)

    test_result("IntegrityChecker Initialization", True,
               f"Database created: {test_db.name}")

    # Verify critical files list
    if len(checker.critical_files) > 0:
        test_result("Critical Files List", True,
                   f"Tracking {len(checker.critical_files)} critical files")
    else:
        test_result("Critical Files List", False, "No critical files defined")

except Exception as e:
    test_result("IntegrityChecker Initialization", False, str(e))

# =============================================================================
# TEST 6: File Hash Calculation
# =============================================================================
print("TEST 6: File Hash Calculation")
print("-" * 80)

try:
    # Create temporary test file
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py')
    temp_file.write("# Test Python File\nprint('Hello Oracle Samuel')")
    temp_file.close()

    # Calculate hash
    md5_hash, file_size = checker.calculate_file_hash(temp_file.name)

    if md5_hash and len(md5_hash) == 32:
        test_result("File Hash Calculation", True,
                   f"Hash: {md5_hash}, Size: {file_size} bytes")
    else:
        test_result("File Hash Calculation", False, "Invalid hash or size")

    # Test non-existent file
    missing_hash, error_msg = checker.calculate_file_hash("nonexistent_file.txt")

    if missing_hash is None and "not found" in error_msg.lower():
        test_result("Missing File Detection", True, "Correctly handles missing files")
    else:
        test_result("Missing File Detection", False, "Failed to detect missing file")

    # Cleanup
    os.unlink(temp_file.name)

except Exception as e:
    test_result("File Hash Calculation", False, str(e))

# =============================================================================
# TEST 7: File Registration
# =============================================================================
print("TEST 7: File Registration")
print("-" * 80)

try:
    # Create test file
    test_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py')
    test_file.write("# Oracle Samuel Test File")
    test_file.close()

    # Register file
    success, result = checker.register_file(test_file.name)

    if success:
        test_result("File Registration", True, f"Registered with hash: {result[:16]}...")
    else:
        test_result("File Registration", False, f"Registration failed: {result}")

except Exception as e:
    test_result("File Registration", False, str(e))

# =============================================================================
# TEST 8: File Verification
# =============================================================================
print("TEST 8: File Verification")
print("-" * 80)

try:
    # Verify unchanged file
    status, message = checker.verify_file(test_file.name)

    if status is True:
        test_result("File Verification - Unchanged", True, message)
    else:
        test_result("File Verification - Unchanged", False, message)

    # Modify file
    with open(test_file.name, 'a') as f:
        f.write("\n# Modified content")

    # Verify modified file is detected
    status, message = checker.verify_file(test_file.name)

    if status is False:
        test_result("File Verification - Modified Detection", True, message)
    else:
        test_result("File Verification - Modified Detection", False,
                   "Failed to detect modification")

    # Cleanup
    os.unlink(test_file.name)

except Exception as e:
    test_result("File Verification", False, str(e))

# =============================================================================
# TEST 9: Integrity Log
# =============================================================================
print("TEST 9: Integrity Log")
print("-" * 80)

try:
    # Get integrity log
    log_df = checker.get_integrity_log(limit=10)

    if not log_df.empty:
        test_result("Integrity Log Retrieval", True,
                   f"Retrieved {len(log_df)} records")

        # Verify log structure
        required_columns = ['file_path', 'md5_hash', 'last_verified', 'status']
        has_columns = all(col in log_df.columns for col in required_columns)

        if has_columns:
            test_result("Integrity Log Structure", True,
                       f"Columns: {', '.join(log_df.columns)}")
        else:
            test_result("Integrity Log Structure", False, "Missing required columns")
    else:
        test_result("Integrity Log Retrieval", True, "Empty log (expected for new database)")

except Exception as e:
    test_result("Integrity Log", False, str(e))

# =============================================================================
# TEST 10: Large DataFrame MD5
# =============================================================================
print("TEST 10: Large DataFrame MD5 Performance")
print("-" * 80)

try:
    from utils.md5_manager import generate_md5_from_dataframe
    import time

    # Create large DataFrame (10,000 rows)
    large_df = pd.DataFrame({
        'price': np.random.randint(100000, 1000000, 10000),
        'sqft': np.random.randint(500, 5000, 10000),
        'bedrooms': np.random.randint(1, 6, 10000),
        'bathrooms': np.random.randint(1, 5, 10000)
    })

    # Measure hash generation time
    start_time = time.time()
    hash_value = generate_md5_from_dataframe(large_df)
    elapsed_time = time.time() - start_time

    if len(hash_value) == 32 and elapsed_time < 5.0:
        test_result("Large DataFrame MD5", True,
                   f"10,000 rows hashed in {elapsed_time:.3f}s")
    else:
        test_result("Large DataFrame MD5", False,
                   f"Performance issue: {elapsed_time:.3f}s")

except Exception as e:
    test_result("Large DataFrame MD5", False, str(e))

# =============================================================================
# TEST 11: Integrity Report Generation
# =============================================================================
print("TEST 11: Integrity Report Generation")
print("-" * 80)

try:
    # Note: This will fail for files not registered, which is expected
    report = checker.generate_integrity_report()

    if "PROJECT INTEGRITY REPORT" in report:
        test_result("Integrity Report Generation", True,
                   f"Report generated ({len(report)} characters)")

        # Check report contains key sections
        has_summary = "Summary" in report
        has_details = "File Details" in report
        has_score = "Integrity Score" in report

        if has_summary and has_details and has_score:
            test_result("Integrity Report Structure", True,
                       "All sections present")
        else:
            test_result("Integrity Report Structure", False,
                       "Missing report sections")
    else:
        test_result("Integrity Report Generation", False,
                   "Invalid report format")

except Exception as e:
    test_result("Integrity Report Generation", False, str(e))

# Cleanup test database
try:
    if os.path.exists(test_db.name):
        os.unlink(test_db.name)
except:
    pass

# =============================================================================
# FINAL SUMMARY
# =============================================================================
print("=" * 80)
print("MD5 INTEGRITY TESTING SUMMARY")
print("=" * 80)
print(f"Tests Passed: {len(test_results['passed'])}")
print(f"Tests Failed: {len(test_results['failed'])}")
print(f"Warnings: {len(test_results['warnings'])}")
print()

if test_results['failed']:
    print("FAILED TESTS:")
    for test in test_results['failed']:
        print(f"  - {test}")
    print()
    print("[FAIL] Some MD5 integrity tests failed - Review errors above")
    sys.exit(1)
else:
    print("[PASS] ALL MD5 INTEGRITY TESTS PASSED!")
    print()
    print("MD5 INTEGRITY VERIFICATION CHECKLIST:")
    print("  [PASS] DataFrame MD5 hash generation working")
    print("  [PASS] File MD5 signature generation working")
    print("  [PASS] Data integrity verification working")
    print("  [PASS] Tamper detection working")
    print("  [PASS] Signature record creation working")
    print("  [PASS] ProjectIntegrityChecker initialization working")
    print("  [PASS] File hash calculation working")
    print("  [PASS] File registration working")
    print("  [PASS] File verification working")
    print("  [PASS] Modification detection working")
    print("  [PASS] Integrity log retrieval working")
    print("  [PASS] Large dataset performance acceptable")
    print("  [PASS] Integrity report generation working")
    print()
    print("MD5 protection system fully operational!")
    sys.exit(0)
