# CipherChat Test Scenarios

This document outlines various test scenarios for the CipherChat web application.

## User Authentication Tests

### 1. User Registration
- **Test**: Register a new user
- **Steps**:
  1. Go to http://127.0.0.1:8000/users/register/
  2. Fill in registration form
  3. Submit and verify account creation
- **Expected**: User account created, redirected to login

### 2. User Login
- **Test**: Login with existing credentials
- **Steps**:
  1. Go to http://127.0.0.1:8000/users/login/
  2. Use test credentials:
     - Username: `testuser1`, Password: `testpass123`
     - Username: `testuser2`, Password: `secure456`
     - Username: `testuser3`, Password: `password789`
     - Username: `testuser4`, Password: `secret101`
     - Username: `testuser5`, Password: `cipher202`
  3. Verify successful login
- **Expected**: Successful login, redirected to dashboard

### 3. User Logout
- **Test**: Logout functionality
- **Steps**:
  1. Login as any test user
  2. Click logout
  3. Verify session termination
- **Expected**: Logged out, redirected to login page

## Key Management Tests

### 4. Generate Encryption Keys
- **Test**: Generate new RSA key pair
- **Steps**:
  1. Login as test user
  2. Navigate to key generation page
  3. Generate new keys
  4. Verify key creation
- **Expected**: New RSA key pair generated and stored

### 5. Import Public Keys
- **Test**: Import another user's public key
- **Steps**:
  1. Login as testuser1
  2. Navigate to key management
  3. Import testuser2's public key
  4. Verify key import
- **Expected**: Public key imported successfully

### 6. Export Public Key
- **Test**: Export own public key
- **Steps**:
  1. Login as test user
  2. Navigate to key management
  3. Export public key
  4. Verify key format
- **Expected**: Public key exported in PEM format

## Message Encryption Tests

### 7. Send Encrypted Message
- **Test**: Send encrypted message to another user
- **Steps**:
  1. Login as testuser1
  2. Navigate to send message page
  3. Select testuser2 as recipient
  4. Enter message content
  5. Send message
- **Expected**: Message encrypted and sent successfully

### 8. Receive and Decrypt Message
- **Test**: Receive and decrypt message from another user
- **Steps**:
  1. Login as testuser2
  2. Navigate to inbox
  3. Open message from testuser1
  4. Verify decryption
- **Expected**: Message decrypted and displayed correctly

### 9. Message History
- **Test**: View message history
- **Steps**:
  1. Login as any test user
  2. Navigate to message history
  3. Verify message list
- **Expected**: All sent/received messages displayed

## Security Tests

### 10. Unauthorized Access
- **Test**: Access protected pages without authentication
- **Steps**:
  1. Try to access dashboard without login
  2. Try to access admin without superuser privileges
- **Expected**: Redirected to login page

### 11. CSRF Protection
- **Test**: Verify CSRF protection
- **Steps**:
  1. Try to submit forms without CSRF token
  2. Verify form rejection
- **Expected**: Forms rejected with CSRF error

### 12. XSS Protection
- **Test**: Test XSS protection
- **Steps**:
  1. Try to send message with script tags
  2. Verify content sanitization
- **Expected**: Script tags sanitized or rejected

## Admin Interface Tests

### 13. Admin Access
- **Test**: Access Django admin interface
- **Steps**:
  1. Go to http://127.0.0.1:8000/admin/
  2. Login with admin credentials
  3. Verify admin access
- **Expected**: Admin interface accessible

### 14. User Management
- **Test**: Manage users through admin
- **Steps**:
  1. Access admin interface
  2. Navigate to Users section
  3. View test users
- **Expected**: All test users visible in admin

### 15. Security Logs
- **Test**: View security logs
- **Steps**:
  1. Access admin interface
  2. Navigate to Security Logs
  3. Verify log entries
- **Expected**: Security logs displayed

## Performance Tests

### 16. Multiple Users
- **Test**: Test with multiple concurrent users
- **Steps**:
  1. Open multiple browser sessions
  2. Login as different test users
  3. Send messages simultaneously
- **Expected**: Application handles multiple users

### 17. Large Messages
- **Test**: Test with large message content
- **Steps**:
  1. Send message with large content
  2. Verify handling
- **Expected**: Large messages handled properly

## Error Handling Tests

### 18. Invalid Login
- **Test**: Test invalid login attempts
- **Steps**:
  1. Try to login with wrong credentials
  2. Verify error handling
- **Expected**: Proper error message displayed

### 19. Network Errors
- **Test**: Test network error handling
- **Steps**:
  1. Simulate network issues
  2. Verify graceful degradation
- **Expected**: Application handles network errors

## Browser Compatibility Tests

### 20. Cross-Browser Testing
- **Test**: Test in different browsers
- **Steps**:
  1. Test in Chrome, Firefox, Safari, Edge
  2. Verify functionality
- **Expected**: Consistent behavior across browsers

## Test Data Verification

### 21. Database Integrity
- **Test**: Verify test data integrity
- **Steps**:
  1. Check database tables
  2. Verify relationships
- **Expected**: All test data properly stored

### 22. File System
- **Test**: Verify file system operations
- **Steps**:
  1. Check key files
  2. Check message files
- **Expected**: Files properly stored and accessible

## Running Tests

To run these tests:

1. **Start the application**:
   ```bash
   ./start_web_app.py
   ```

2. **Initialize test data** (if not already done):
   ```bash
   ./init_test_data.py
   ```

3. **Use test credentials**:
   - testuser1 / testpass123
   - testuser2 / secure456
   - testuser3 / password789
   - testuser4 / secret101
   - testuser5 / cipher202

4. **Follow test scenarios** above

## Expected Results

After running all tests, you should have:
- ✅ All authentication features working
- ✅ Key generation and management functional
- ✅ Message encryption/decryption working
- ✅ Security features active
- ✅ Admin interface accessible
- ✅ Test data properly loaded
- ✅ No critical errors or security vulnerabilities
