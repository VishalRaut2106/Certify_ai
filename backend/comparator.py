from fuzzywuzzy import fuzz
from datetime import datetime, timedelta
import re

def normalize_dates(date_str):
    if not date_str:
        return []

    dates = []
    # Try ISO
    try:
        dates.append(datetime.strptime(date_str[:10], '%Y-%m-%d'))
    except:
        pass

    # Try common formats
    formats = ['%B %d, %Y', '%B %d,%Y', '%d %B %Y', '%d %b %Y', '%Y/%m/%d', '%d/%m/%Y']
    for f in formats:
        try:
            dates.append(datetime.strptime(date_str.strip(), f))
        except:
            pass

    return dates

def compare_fields(ocr_data, qr_data):
    raw_text = ocr_data.get('raw_text', '').lower()
    
    results = {
        'name':    {'ocr': ocr_data.get('name'),   'qr': qr_data.get('name'),   'match': False},
        'course':  {'ocr': ocr_data.get('course'), 'qr': qr_data.get('course'), 'match': False},
        'date':    {'ocr': ocr_data.get('date'),   'qr': qr_data.get('date'),   'match': False},
        'verdict': None
    }

    # Name matching
    if qr_data.get('name'):
        qr_name = qr_data['name'].lower().strip()
        ocr_name = (ocr_data.get('name') or '').lower().strip()
        if qr_name in raw_text or fuzz.partial_ratio(qr_name, raw_text) >= 85 or (ocr_name and fuzz.ratio(qr_name, ocr_name) >= 85):
            results['name']['match'] = True

    # Course matching
    if qr_data.get('course'):
        qr_course = qr_data['course'].lower().strip()
        ocr_course = (ocr_data.get('course') or '').lower().strip()
        if qr_course in raw_text or fuzz.partial_ratio(qr_course, raw_text) >= 85 or (ocr_course and fuzz.ratio(qr_course, ocr_course) >= 85):
            results['course']['match'] = True

    # Date matching
    if qr_data.get('date'):
        qr_dates = normalize_dates(qr_data['date'])
        
        # 1. Fuzzy match formatted dates inside raw text
        if qr_dates:
            target_date = qr_dates[0]
            # Try to match string forms of target_date, target_date - 1, target_date + 1
            for d in [target_date, target_date - timedelta(days=1), target_date + timedelta(days=1)]:
                # Formats like "April 27, 2026"
                # Note: Windows might not support %-d for stripping leading zero, so use string replace
                day_num = str(d.day)
                date_strings = [
                    d.strftime('%B %d, %Y').lower(),
                    d.strftime(f'%B {day_num}, %Y').lower(),
                    d.strftime('%d %B %Y').lower(),
                    d.strftime(f'{day_num} %B %Y').lower(),
                    d.strftime('%Y-%m-%d').lower()
                ]
                for ds in date_strings:
                    if ds in raw_text or fuzz.partial_ratio(ds, raw_text) >= 90:
                        results['date']['match'] = True
                        break
                if results['date']['match']:
                    break

        # 2. If string fuzzy match fails, try parsing OCR date and compare with tolerance
        if not results['date']['match'] and ocr_data.get('date'):
            ocr_dates = normalize_dates(ocr_data['date'])
            for q_d in qr_dates:
                for o_d in ocr_dates:
                    if abs((q_d - o_d).days) <= 1:
                        results['date']['match'] = True
                        break
                if results['date']['match']:
                    break

    # Determine Verdict
    if not qr_data.get('name') or not qr_data.get('course') or not qr_data.get('date'):
        results['verdict'] = 'Manual Review - Missing Data'
    else:
        all_match = (
            results['name']['match'] and
            results['course']['match'] and
            results['date']['match']
        )
        if all_match:
            results['verdict'] = 'Verified'
        else:
            if len(raw_text.strip()) < 20:
                results['verdict'] = 'Manual Review - Unreadable OCR'
            else:
                results['verdict'] = 'Fraud'

    return results