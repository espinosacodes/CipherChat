# CipherChat Encryption Feature

## Overview

The CipherChat application now supports sending messages with or without encryption. This feature allows users to compare encrypted and non-encrypted traffic for educational and analysis purposes, particularly useful for Wireshark network analysis.

## Features

### 1. Encryption Toggle
- Users can choose whether to encrypt their messages or send them as plaintext
- The encryption option is controlled by a checkbox in the send message form
- Default behavior is encryption enabled (secure by default)

### 2. Dynamic UI
- The interface changes dynamically based on encryption status
- When encryption is disabled:
  - Button changes to red with warning icon
  - Encryption information panels are hidden
  - Clear warnings about security implications

### 3. Message Status Tracking
- All messages are marked with encryption status (`is_encrypted` field)
- Messages list shows clear indicators for encrypted vs plaintext messages
- Message details page shows appropriate warnings for non-encrypted messages

## Database Changes

### Message Model Updates
- Added `is_encrypted` boolean field (default: True)
- Made encryption-related fields optional (`encrypted_aes_key`, `iv`, `signature`)
- Updated field descriptions to reflect dual usage

### Migration
- Migration file: `chat/migrations/0002_message_is_encrypted_alter_message_encrypted_aes_key_and_more.py`
- Applied automatically when running `python manage.py migrate`

## Usage Instructions

### Sending Messages

1. **Navigate to Send Message Page**
   - Go to the dashboard and click "Send New Message"
   - Or navigate directly to `/chat/send_message/`

2. **Fill in Message Details**
   - Enter recipient username
   - Select message type
   - Type your message content

3. **Choose Encryption Option**
   - **Encrypted (Default)**: Check the "Enable Encryption" checkbox
     - Requires both sender and recipient to have cryptographic keys
     - Message will be encrypted before transmission
     - Secure for sensitive communications
   
   - **Non-Encrypted**: Uncheck the "Enable Encryption" checkbox
     - No cryptographic keys required
     - Message sent as plaintext
     - **Warning**: Not secure, visible to anyone intercepting traffic

4. **Send Message**
   - Click the send button
   - The button text and color will change based on encryption choice

### Viewing Messages

1. **Message List**
   - Encrypted messages show with 🔒 icon and "ENCRYPTED" badge
   - Non-encrypted messages show with ⚠️ icon and "PLAINTEXT" badge
   - Clear visual distinction between secure and insecure messages

2. **Message Details**
   - Encrypted messages show cryptographic information
   - Non-encrypted messages show security warnings
   - Content is displayed appropriately for each type

## Wireshark Analysis

### Purpose
This feature enables network traffic analysis to compare encrypted vs non-encrypted communications.

### Setup for Analysis

1. **Start Wireshark Capture**
   ```bash
   # Capture traffic on your network interface
   sudo wireshark -i eth0 -k
   ```

2. **Send Encrypted Message**
   - Enable encryption in the web interface
   - Send a message with sensitive content
   - Note the timestamp

3. **Send Non-Encrypted Message**
   - Disable encryption in the web interface
   - Send the same or similar content
   - Note the timestamp

4. **Analyze Captured Traffic**
   - Filter by HTTP traffic to your Django server
   - Compare the packet contents
   - Look for differences in:
     - Payload encryption
     - Packet sizes
     - Transmission patterns

### Expected Differences

**Encrypted Messages:**
- Payload appears as random/encrypted data
- Larger packet sizes due to encryption overhead
- Consistent encryption patterns

**Non-Encrypted Messages:**
- Payload contains readable plaintext
- Smaller packet sizes
- No encryption patterns visible

## Security Considerations

### ⚠️ Important Warnings

1. **Non-Encrypted Messages Are Not Secure**
   - Content is transmitted as plaintext
   - Visible to anyone intercepting network traffic
   - Should only be used for testing/analysis

2. **Educational Use Only**
   - This feature is designed for educational purposes
   - Not recommended for production use with sensitive data
   - Always use encryption for real communications

3. **Key Requirements**
   - Encrypted messages require both users to have cryptographic keys
   - Non-encrypted messages bypass key requirements
   - System will warn users about missing keys for encrypted messages

## Technical Implementation

### Form Changes
- Added `encryption_enabled` boolean field to `SendMessageForm`
- Default value: `True` (secure by default)
- Includes help text explaining the option

### View Changes
- Updated `send_message` view to handle both encryption modes
- Conditional logic for key validation
- Different message creation paths for encrypted vs non-encrypted
- Appropriate logging and user feedback

### Template Changes
- Dynamic UI updates based on encryption checkbox
- JavaScript for real-time interface changes
- Clear visual indicators for security status
- Warning messages for non-encrypted messages

### Model Changes
- Added `is_encrypted` field to track message status
- Made encryption fields optional
- Updated string representation to show encryption status

## Testing

### Manual Testing
1. Create test users with cryptographic keys
2. Send encrypted message (verify encryption process)
3. Send non-encrypted message (verify bypass of encryption)
4. View messages in list (verify status indicators)
5. View message details (verify appropriate warnings)

### Automated Testing
Run the test script:
```bash
python test_encryption_feature.py
```

This script will:
- Create test users and profiles
- Send both encrypted and non-encrypted messages
- Verify database storage and retrieval
- Clean up test data

## Future Enhancements

1. **Real Encryption Implementation**
   - Replace placeholder encryption with actual cryptographic operations
   - Implement proper key management
   - Add encryption algorithm selection

2. **Advanced Analysis Features**
   - Built-in traffic analysis tools
   - Encryption strength indicators
   - Security audit reports

3. **User Interface Improvements**
   - More detailed encryption status information
   - Real-time encryption process visualization
   - Advanced security settings

## Troubleshooting

### Common Issues

1. **"You need to generate cryptographic keys first"**
   - Solution: Generate keys or disable encryption
   - Non-encrypted messages don't require keys

2. **"User has not generated keys yet"**
   - Solution: Ask recipient to generate keys or send non-encrypted
   - Only applies to encrypted messages

3. **Migration Errors**
   - Solution: Run `python manage.py migrate`
   - Ensure database is up to date

### Support
For issues or questions about this feature, refer to the main project documentation or create an issue in the project repository.
