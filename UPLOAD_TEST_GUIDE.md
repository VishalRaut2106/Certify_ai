# 🧪 Real Certificate Testing Guide

## 🎯 How to Test AI Verification with Real Certificates

### Step 1: Access the System
1. **Open your browser**: Go to http://localhost:3000
2. **Login**: Use your account credentials
   - Email: `Vishalraut.login@gmail.com` (or create new account)
   - Password: Your password

### Step 2: Upload Real Certificates
1. **Go to "Upload" section** in the dashboard
2. **Choose one of these options**:

#### Option A: Use the Test Certificate I Created
- **File**: `test_certificate.png` (created in the project folder)
- **Expected Result**: Valid (85-95% trust score)
- **AI Will Detect**: Stanford University, completion certificate, dates, signatures

#### Option B: Upload Your Own Real Certificates
- **Supported formats**: PNG, JPG, PDF, TIFF
- **Max size**: 10MB per file
- **Best results**: Clear, high-resolution images

### Step 3: Watch AI Verification in Real-Time

The AI will analyze:

#### 🔍 **OCR Text Extraction**
- Institution names (Stanford, MIT, Coursera, etc.)
- Certificate keywords (certificate, diploma, completion)
- Student/recipient names
- Dates and signatures
- Course/program names

#### 📱 **QR Code Detection**
- Scans for verification QR codes
- Validates QR code URLs
- Checks for trusted domains (coursera.org, edx.org, etc.)

#### 🎨 **Visual Quality Analysis**
- Image sharpness and clarity
- Professional color schemes
- Layout and design quality
- Edge detection and detail analysis

#### 🚨 **Fraud Pattern Detection**
- Suspicious keywords (fake, template, sample)
- Missing essential elements
- Poor image quality indicators
- Filename analysis

#### 🎯 **Trust Score Calculation**
- **85-100%**: Valid Certificate ✅
- **30-84%**: Suspicious Certificate ⚠️
- **0-29%**: Fake Certificate ❌

### Step 4: View Detailed Results

Click on any certificate to see:
- **Trust Score**: Overall confidence percentage
- **Processing Time**: How fast the AI analyzed it
- **Detailed Breakdown**: OCR confidence, QR results, visual analysis
- **Fraud Indicators**: Any suspicious patterns found
- **Confidence Factors**: What made the AI confident in its assessment

## 🧪 Test Scenarios

### ✅ **Valid Certificate Test**
Upload a real certificate from:
- Coursera, edX, Udacity
- University transcripts/diplomas
- Professional certifications (Google, Microsoft, AWS)
- **Expected**: High trust score (85%+), "Valid" status

### ⚠️ **Suspicious Certificate Test**
Upload certificates with:
- Poor image quality
- Missing information
- Unusual formatting
- **Expected**: Medium trust score (30-84%), "Suspicious" status

### ❌ **Fake Certificate Test**
Upload obviously fake certificates:
- Templates with placeholder text
- Poor quality scans
- Misspelled institution names
- **Expected**: Low trust score (<30%), "Fake" status

## 🔧 Troubleshooting

### If Upload Fails:
1. Check file size (max 10MB)
2. Verify file format (PNG, JPG, PDF, TIFF)
3. Ensure you're logged in
4. Try refreshing the page

### If No Certificates Show:
1. Refresh the browser page
2. Check browser console for errors (F12)
3. Verify both servers are running:
   - Backend: http://localhost:8000/health
   - Frontend: http://localhost:3000

### If AI Verification Stalls:
1. Wait up to 30 seconds for processing
2. Refresh the certificates list
3. Check backend logs for errors

## 🎉 Success Indicators

You'll know the AI verification is working when you see:
1. ✅ **Fast Upload**: Files upload within seconds
2. 🔄 **Status Changes**: Pending → Processing → Valid/Suspicious/Fake
3. 📊 **Trust Scores**: Numerical confidence percentages
4. 🔍 **Detailed Analysis**: OCR results, QR detection, fraud analysis
5. ⚡ **Quick Processing**: Results within 1-5 seconds

## 📱 Real-World Testing Tips

1. **Use High-Quality Images**: Clear, well-lit photos work best
2. **Test Different Types**: Try various certificate formats
3. **Compare Results**: Upload similar certificates to see consistency
4. **Check Edge Cases**: Test with partially visible or rotated certificates

**The AI Certificate Verification System is ready to analyze your real certificates!** 🚀