#!/usr/bin/env python3
"""
Add sample certificates with different AI verification results
"""

import sqlite3
import uuid
from datetime import datetime, timedelta
import json

def add_sample_certificates():
    """Add sample certificates with AI verification results"""
    
    conn = sqlite3.connect('certificate_verification.db')
    cursor = conn.cursor()
    
    # Get the user ID
    cursor.execute('SELECT id FROM users LIMIT 1')
    user_result = cursor.fetchone()
    if not user_result:
        print("❌ No users found. Please create an account first.")
        return
    
    user_id = user_result[0]
    print(f"👤 Adding certificates for user: {user_id}")
    
    # Sample certificates with different AI verification results
    sample_certificates = [
        {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "original_filename": "stanford_computer_science_degree.pdf",
            "file_path": "/uploads/sample1.pdf",
            "file_type": "application/pdf",
            "file_size": 2048576,
            "verification_status": "valid",
            "trust_score": 95.8,
            "upload_timestamp": (datetime.utcnow() - timedelta(days=2)).isoformat(),
            "processing_time": 1.2,
            "metadata": json.dumps({
                "ocr_analysis": {
                    "extracted_text": "STANFORD UNIVERSITY\\nCERTIFICATE OF COMPLETION\\nThis is to certify that\\nJOHN SMITH\\nhas successfully completed\\nComputer Science Degree\\nDate: May 15, 2024\\nAuthorized by: Dr. Sarah Johnson, Dean",
                    "confidence": 92.5,
                    "has_institution_name": True,
                    "has_certificate_keywords": True,
                    "has_date": True,
                    "has_signature": True,
                    "ocr_method": "tesseract"
                },
                "qr_code_analysis": {
                    "qr_codes_found": ["https://verify.stanford.edu/cert/abc123"],
                    "validation_results": {
                        "https://verify.stanford.edu/cert/abc123": {
                            "is_valid_url": True,
                            "domain_trusted": True,
                            "is_verification_link": True
                        }
                    },
                    "authenticity_score": 30
                },
                "visual_analysis": {
                    "quality_score": 88.5,
                    "authenticity_indicators": ["high_image_quality", "professional_color_scheme"]
                },
                "fraud_detection": {
                    "fraud_probability": 0.05,
                    "indicators": [],
                    "risk_level": "low"
                }
            })
        },
        {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "original_filename": "coursera_data_science_certificate.jpg",
            "file_path": "/uploads/sample2.jpg",
            "file_type": "image/jpeg",
            "file_size": 1536000,
            "verification_status": "valid",
            "trust_score": 89.2,
            "upload_timestamp": (datetime.utcnow() - timedelta(days=1)).isoformat(),
            "processing_time": 0.8,
            "metadata": json.dumps({
                "ocr_analysis": {
                    "extracted_text": "COURSERA\\nData Science Specialization\\nThis is to certify that\\nVISHAL RAUT\\nhas successfully completed\\nData Science with Python\\nIssued: March 2024\\nVerified by Coursera",
                    "confidence": 87.3,
                    "has_institution_name": True,
                    "has_certificate_keywords": True,
                    "has_date": True,
                    "has_signature": True,
                    "ocr_method": "tesseract"
                },
                "qr_code_analysis": {
                    "qr_codes_found": ["https://coursera.org/verify/ABCD1234"],
                    "validation_results": {
                        "https://coursera.org/verify/ABCD1234": {
                            "is_valid_url": True,
                            "domain_trusted": True,
                            "is_verification_link": True
                        }
                    },
                    "authenticity_score": 30
                },
                "visual_analysis": {
                    "quality_score": 82.1,
                    "authenticity_indicators": ["professional_color_scheme", "sufficient_detail"]
                },
                "fraud_detection": {
                    "fraud_probability": 0.1,
                    "indicators": [],
                    "risk_level": "low"
                }
            })
        },
        {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "original_filename": "suspicious_certificate_template.png",
            "file_path": "/uploads/sample3.png",
            "file_type": "image/png",
            "file_size": 3072000,
            "verification_status": "suspicious",
            "trust_score": 45.7,
            "upload_timestamp": (datetime.utcnow() - timedelta(hours=12)).isoformat(),
            "processing_time": 1.5,
            "metadata": json.dumps({
                "ocr_analysis": {
                    "extracted_text": "CERTIFICATE TEMPLATE\\nThis is a sample certificate\\nStudent Name: [YOUR NAME]\\nCourse: [COURSE NAME]\\nDate: [DATE]\\nWatermark: SAMPLE",
                    "confidence": 65.2,
                    "has_institution_name": False,
                    "has_certificate_keywords": True,
                    "has_date": False,
                    "has_signature": False,
                    "ocr_method": "tesseract"
                },
                "qr_code_analysis": {
                    "qr_codes_found": [],
                    "validation_results": {},
                    "authenticity_score": 0
                },
                "visual_analysis": {
                    "quality_score": 45.3,
                    "authenticity_indicators": []
                },
                "fraud_detection": {
                    "fraud_probability": 0.65,
                    "indicators": ["fraud_keyword_detected: template", "fraud_keyword_detected: sample", "missing_institution_name", "missing_date_information", "no_qr_code_found"],
                    "risk_level": "medium"
                }
            })
        },
        {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "original_filename": "fake_harvard_diploma.pdf",
            "file_path": "/uploads/sample4.pdf",
            "file_type": "application/pdf",
            "file_size": 1024000,
            "verification_status": "fake",
            "trust_score": 15.3,
            "upload_timestamp": (datetime.utcnow() - timedelta(hours=6)).isoformat(),
            "processing_time": 2.1,
            "metadata": json.dumps({
                "ocr_analysis": {
                    "extracted_text": "HARVRD UNIVERSITY\\nFake Diploma\\nThis certifies that\\nJOHN DOE\\ncompleted studies in\\nBusiness Administration\\nCopy - Not Official",
                    "confidence": 45.8,
                    "has_institution_name": True,
                    "has_certificate_keywords": True,
                    "has_date": False,
                    "has_signature": False,
                    "ocr_method": "tesseract"
                },
                "qr_code_analysis": {
                    "qr_codes_found": [],
                    "validation_results": {},
                    "authenticity_score": 0
                },
                "visual_analysis": {
                    "quality_score": 25.7,
                    "authenticity_indicators": []
                },
                "fraud_detection": {
                    "fraud_probability": 0.85,
                    "indicators": ["fraud_keyword_detected: fake", "fraud_keyword_detected: copy", "poor_image_quality", "missing_date_information", "no_qr_code_found"],
                    "risk_level": "high"
                }
            })
        },
        {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "original_filename": "processing_certificate.jpg",
            "file_path": "/uploads/sample5.jpg",
            "file_type": "image/jpeg",
            "file_size": 2560000,
            "verification_status": "pending",
            "trust_score": None,
            "upload_timestamp": datetime.utcnow().isoformat(),
            "processing_time": None,
            "metadata": "{}"
        }
    ]
    
    # Insert sample certificates
    for cert in sample_certificates:
        cursor.execute('''
            INSERT INTO certificates (
                id, user_id, batch_id, original_filename, file_path, file_type, 
                file_size, verification_status, trust_score, upload_timestamp, 
                processing_time, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            cert["id"], cert["user_id"], None, cert["original_filename"],
            cert["file_path"], cert["file_type"], cert["file_size"],
            cert["verification_status"], cert["trust_score"], 
            cert["upload_timestamp"], cert["processing_time"], cert["metadata"]
        ))
        
        print(f"✅ Added: {cert['original_filename']} - Status: {cert['verification_status']}")
        
        # Add verification results for processed certificates
        if cert["verification_status"] != "pending":
            verification_record = {
                "id": f"verify_{cert['id']}",
                "certificate_id": cert["id"],
                "verification_timestamp": cert["upload_timestamp"],
                "ocr_results": cert["metadata"],
                "qr_results": cert["metadata"],
                "template_match_results": cert["metadata"],
                "fraud_indicators": cert["metadata"],
                "trust_score": cert["trust_score"],
                "verification_details": cert["metadata"]
            }
            
            cursor.execute('''
                INSERT INTO verification_results (
                    id, certificate_id, verification_timestamp, ocr_results,
                    qr_results, template_match_results, fraud_indicators,
                    trust_score, verification_details
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                verification_record["id"], verification_record["certificate_id"],
                verification_record["verification_timestamp"], verification_record["ocr_results"],
                verification_record["qr_results"], verification_record["template_match_results"],
                verification_record["fraud_indicators"], verification_record["trust_score"],
                verification_record["verification_details"]
            ))
    
    conn.commit()
    conn.close()
    
    print(f"\n🎉 Successfully added {len(sample_certificates)} sample certificates!")
    print("\n📊 Certificate Status Summary:")
    print("✅ Valid: 2 certificates (Stanford CS Degree, Coursera Data Science)")
    print("⚠️ Suspicious: 1 certificate (Template with fraud indicators)")
    print("❌ Fake: 1 certificate (Fake Harvard diploma)")
    print("⏳ Pending: 1 certificate (Still processing)")
    
    print("\n🤖 AI Features Demonstrated:")
    print("• OCR Text Extraction with confidence scores")
    print("• QR Code Detection and validation")
    print("• Visual Quality Analysis")
    print("• Fraud Pattern Detection")
    print("• Trust Score Calculation (0-100%)")
    print("• Institution Recognition")
    print("• Date and Signature Detection")

if __name__ == "__main__":
    add_sample_certificates()