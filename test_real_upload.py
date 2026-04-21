#!/usr/bin/env python3
"""
Test real certificate upload and AI verification
"""

import requests
import json
from PIL import Image, ImageDraw, ImageFont
import io
import time

def create_realistic_certificate():
    """Create a realistic-looking certificate for testing"""
    # Create a professional certificate
    width, height = 1200, 900
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Try to use better fonts
    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
        header_font = ImageFont.truetype("arial.ttf", 32)
        body_font = ImageFont.truetype("arial.ttf", 24)
        small_font = ImageFont.truetype("arial.ttf", 18)
    except:
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw professional certificate border
    draw.rectangle([20, 20, width-20, height-20], outline='#1f4e79', width=8)
    draw.rectangle([40, 40, width-40, height-40], outline='#1f4e79', width=2)
    
    # Header
    draw.text((width//2, 80), "STANFORD UNIVERSITY", font=title_font, fill='#1f4e79', anchor='mt')
    draw.text((width//2, 140), "CERTIFICATE OF COMPLETION", font=header_font, fill='#8b0000', anchor='mt')
    
    # Main content
    draw.text((width//2, 220), "This is to certify that", font=body_font, fill='black', anchor='mt')
    draw.text((width//2, 280), "VISHAL RAUT", font=title_font, fill='#1f4e79', anchor='mt')
    draw.text((width//2, 340), "has successfully completed the course", font=body_font, fill='black', anchor='mt')
    draw.text((width//2, 400), "Artificial Intelligence and Machine Learning", font=header_font, fill='#8b0000', anchor='mt')
    draw.text((width//2, 460), "with distinction", font=body_font, fill='black', anchor='mt')
    
    # Date and signatures
    draw.text((width//2, 550), "Date: December 15, 2024", font=body_font, fill='black', anchor='mt')
    draw.text((200, 700), "Dr. Sarah Johnson", font=body_font, fill='black', anchor='mt')
    draw.text((200, 730), "Dean of Engineering", font=small_font, fill='gray', anchor='mt')
    draw.text((200, 750), "Stanford University", font=small_font, fill='gray', anchor='mt')
    
    draw.text((width-200, 700), "Prof. Michael Chen", font=body_font, fill='black', anchor='mt')
    draw.text((width-200, 730), "Course Director", font=small_font, fill='gray', anchor='mt')
    draw.text((width-200, 750), "AI Department", font=small_font, fill='gray', anchor='mt')
    
    # Add some decorative elements
    draw.text((width//2, 800), "Certificate ID: STAN-AI-2024-001234", font=small_font, fill='gray', anchor='mt')
    draw.text((width//2, 820), "Verify at: https://verify.stanford.edu/cert/001234", font=small_font, fill='blue', anchor='mt')
    
    return image

def get_user_token():
    """Get authentication token for the current user"""
    # Try to login with the existing user
    login_data = {
        "username": "Vishalraut.login@gmail.com",
        "password": "your_password_here"  # You'll need to provide the correct password
    }
    
    try:
        response = requests.post("http://127.0.0.1:8000/api/v1/auth/login", data=login_data)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print("Please update the password in the script or create a new account")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def upload_certificate(token, image):
    """Upload certificate for AI verification"""
    # Convert image to bytes
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    # Prepare upload
    files = {
        'file': ('stanford_ai_certificate.png', img_bytes, 'image/png')
    }
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/v1/upload/single",
            files=files,
            headers=headers
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            print("✅ Certificate uploaded successfully!")
            print(f"📄 Certificate ID: {result.get('certificate_id')}")
            return result.get('certificate_id')
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return None

def monitor_verification(token, certificate_id):
    """Monitor the AI verification process"""
    headers = {'Authorization': f'Bearer {token}'}
    
    print("\n🤖 Monitoring AI Verification Process...")
    print("AI is analyzing:")
    print("• 🔍 OCR Text Extraction")
    print("• 📱 QR Code Detection") 
    print("• 🎨 Visual Quality Analysis")
    print("• 🚨 Fraud Pattern Detection")
    print("• 🎯 Trust Score Calculation")
    
    for attempt in range(10):  # Check for up to 50 seconds
        try:
            time.sleep(5)
            
            response = requests.get(
                f"http://127.0.0.1:8000/api/v1/certificates/{certificate_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                cert_data = response.json()
                status = cert_data.get('verification_status', 'unknown')
                trust_score = cert_data.get('trust_score')
                processing_time = cert_data.get('processing_time')
                
                print(f"\n⏱️  Check #{attempt + 1}: Status = {status}")
                
                if status not in ['pending', 'processing']:
                    # Verification complete!
                    print("\n🎉 AI Verification Complete!")
                    print("=" * 60)
                    print(f"📊 Final Status: {status.upper()}")
                    print(f"🎯 Trust Score: {trust_score}%")
                    print(f"⚡ Processing Time: {processing_time}s")
                    
                    # Show detailed results
                    metadata = cert_data.get('metadata', '{}')
                    if metadata and metadata != '{}':
                        try:
                            details = json.loads(metadata) if isinstance(metadata, str) else metadata
                            
                            print("\n🔍 Detailed AI Analysis:")
                            
                            # OCR Results
                            ocr = details.get('ocr_analysis', {})
                            if ocr:
                                print(f"📝 OCR Confidence: {ocr.get('confidence', 0)}%")
                                print(f"🏫 Institution Detected: {ocr.get('has_institution_name', False)}")
                                print(f"📜 Certificate Keywords: {ocr.get('has_certificate_keywords', False)}")
                                print(f"📅 Date Found: {ocr.get('has_date', False)}")
                                print(f"✍️ Signature Detected: {ocr.get('has_signature', False)}")
                            
                            # QR Code Results
                            qr = details.get('qr_code_analysis', {})
                            if qr:
                                qr_codes = qr.get('qr_codes_found', [])
                                print(f"📱 QR Codes Found: {len(qr_codes)}")
                                if qr_codes:
                                    print(f"🔗 QR Content: {qr_codes[0][:50]}...")
                            
                            # Visual Analysis
                            visual = details.get('visual_analysis', {})
                            if visual:
                                print(f"🎨 Visual Quality: {visual.get('quality_score', 0)}%")
                                indicators = visual.get('authenticity_indicators', [])
                                print(f"✅ Authenticity Indicators: {len(indicators)}")
                            
                            # Fraud Detection
                            fraud = details.get('fraud_detection', {})
                            if fraud:
                                fraud_prob = fraud.get('fraud_probability', 0) * 100
                                print(f"🚨 Fraud Probability: {fraud_prob:.1f}%")
                                print(f"⚠️ Risk Level: {fraud.get('risk_level', 'unknown')}")
                                
                        except Exception as e:
                            print(f"📋 Metadata available but couldn't parse: {str(e)[:100]}")
                    
                    # Interpretation
                    if status == 'valid':
                        print("\n✅ AI Assessment: Certificate appears authentic")
                    elif status == 'suspicious':
                        print("\n⚠️ AI Assessment: Certificate has potential issues")
                    elif status == 'fake':
                        print("\n❌ AI Assessment: Certificate likely not authentic")
                    
                    return True
                else:
                    print(f"   🔄 Still processing... (Trust Score: {trust_score}%)")
            else:
                print(f"   ❌ Status check failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Status check error: {e}")
    
    print("\n⏰ Verification taking longer than expected. Check the frontend for results.")
    return False

def main():
    """Main test function"""
    print("🧪 Real Certificate AI Verification Test")
    print("=" * 50)
    
    # Note: You need to provide the correct password
    print("\n⚠️ IMPORTANT: Update the password in get_user_token() function")
    print("Or create a new account and update the email/password")
    
    # For now, let's create a test certificate and show what the AI would detect
    print("\n📄 Creating realistic test certificate...")
    cert_image = create_realistic_certificate()
    
    # Save the certificate for manual upload
    cert_image.save("test_certificate.png")
    print("✅ Test certificate saved as 'test_certificate.png'")
    
    print("\n📋 What the AI will detect in this certificate:")
    print("🔍 OCR Text: 'STANFORD UNIVERSITY', 'CERTIFICATE OF COMPLETION', 'VISHAL RAUT'")
    print("🏫 Institution: Stanford University (recognized)")
    print("📜 Keywords: 'certificate', 'completion', 'course'")
    print("📅 Date: 'December 15, 2024'")
    print("✍️ Signatures: Dr. Sarah Johnson, Prof. Michael Chen")
    print("🔗 Verification URL: https://verify.stanford.edu/cert/001234")
    print("🎨 Visual Quality: High (professional design, clear text)")
    print("🚨 Fraud Indicators: None (legitimate format)")
    print("🎯 Expected Trust Score: 85-95% (Valid)")
    
    print("\n📱 Manual Upload Instructions:")
    print("1. Go to http://localhost:3000")
    print("2. Login with your account")
    print("3. Go to 'Upload' section")
    print("4. Upload the 'test_certificate.png' file")
    print("5. Watch the AI verification in real-time!")
    
    # Uncomment below if you want to test automatic upload
    # (You need to update the password first)
    """
    token = get_user_token()
    if token:
        certificate_id = upload_certificate(token, cert_image)
        if certificate_id:
            monitor_verification(token, certificate_id)
    """

if __name__ == "__main__":
    main()