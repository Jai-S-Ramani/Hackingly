import cv2
import numpy as np
import os

os.makedirs("data/samples", exist_ok=True)

def draw_face_avatar(img, center_x, center_y, scale=1.0, has_glasses=False, has_beard=False):
    """Draws a recognizable stylized face avatar with eyes, eyebrows, nose, and mouth."""
    # Head contour
    head_w = int(45 * scale)
    head_h = int(60 * scale)
    cv2.ellipse(img, (center_x, center_y), (head_w, head_h), 0, 0, 360, (190, 210, 235), -1)
    cv2.ellipse(img, (center_x, center_y), (head_w, head_h), 0, 0, 360, (120, 140, 160), 2)
    
    # Hair
    hair_color = (40, 40, 40)
    cv2.ellipse(img, (center_x, center_y - int(30 * scale)), (int(46 * scale), int(32 * scale)), 0, 180, 360, hair_color, -1)
    
    # Eyes
    eye_offset_x = int(16 * scale)
    eye_y = center_y - int(8 * scale)
    eye_r = int(5 * scale)
    cv2.circle(img, (center_x - eye_offset_x, eye_y), eye_r, (255, 255, 255), -1)
    cv2.circle(img, (center_x + eye_offset_x, eye_y), eye_r, (255, 255, 255), -1)
    cv2.circle(img, (center_x - eye_offset_x, eye_y), int(2 * scale), (20, 20, 20), -1)
    cv2.circle(img, (center_x + eye_offset_x, eye_y), int(2 * scale), (20, 20, 20), -1)
    
    # Eyebrows
    cv2.line(img, (center_x - eye_offset_x - 8, eye_y - 8), (center_x - eye_offset_x + 8, eye_y - 9), hair_color, 2)
    cv2.line(img, (center_x + eye_offset_x - 8, eye_y - 9), (center_x + eye_offset_x + 8, eye_y - 8), hair_color, 2)
    
    # Glasses if requested
    if has_glasses:
        cv2.rectangle(img, (center_x - eye_offset_x - 10, eye_y - 9), (center_x - eye_offset_x + 10, eye_y + 9), (30, 30, 30), 2)
        cv2.rectangle(img, (center_x + eye_offset_x - 10, eye_y - 9), (center_x + eye_offset_x + 10, eye_y + 9), (30, 30, 30), 2)
        cv2.line(img, (center_x - eye_offset_x + 10, eye_y), (center_x + eye_offset_x - 10, eye_y), (30, 30, 30), 2)
    
    # Nose
    cv2.line(img, (center_x, eye_y + 5), (center_x - 3, eye_y + 18), (140, 160, 180), 2)
    cv2.line(img, (center_x - 3, eye_y + 18), (center_x + 4, eye_y + 18), (140, 160, 180), 2)
    
    # Mouth
    cv2.ellipse(img, (center_x, eye_y + 30), (int(14 * scale), int(6 * scale)), 0, 0, 180, (80, 80, 160), 2)
    
    # Beard if requested
    if has_beard:
        cv2.ellipse(img, (center_x, center_y + int(40 * scale)), (int(25 * scale), int(16 * scale)), 0, 0, 180, (50, 50, 50), -1)
    
    # Torso/Shoulders
    cv2.ellipse(img, (center_x, center_y + int(115 * scale)), (int(75 * scale), int(55 * scale)), 0, 180, 360, (70, 90, 140), -1)

def draw_qr_code_mock(img, top_left_x, top_left_y, size=80):
    """Draws a synthetic QR code square with finder patterns."""
    cv2.rectangle(img, (top_left_x, top_left_y), (top_left_x + size, top_left_y + size), (255, 255, 255), -1)
    cv2.rectangle(img, (top_left_x, top_left_y), (top_left_x + size, top_left_y + size), (40, 40, 40), 2)
    # Finder corners
    for fx, fy in [(top_left_x + 5, top_left_y + 5), (top_left_x + size - 25, top_left_y + 5), (top_left_x + 5, top_left_y + size - 25)]:
        cv2.rectangle(img, (fx, fy), (fx + 20, fy + 20), (0, 0, 0), -1)
        cv2.rectangle(img, (fx + 4, fy + 4), (fx + 16, fy + 16), (255, 255, 255), -1)
        cv2.rectangle(img, (fx + 8, fy + 8), (fx + 12, fy + 12), (0, 0, 0), -1)
    # Random pattern blocks
    np.random.seed(42)
    for bx in range(top_left_x + 30, top_left_x + size - 5, 8):
        for by in range(top_left_y + 30, top_left_y + size - 5, 8):
            if np.random.rand() > 0.45:
                cv2.rectangle(img, (bx, by), (bx + 6, by + 6), (20, 20, 20), -1)

# =====================================================================
# 1. Genuine Aadhaar Card (Arjun Kumar)
# =====================================================================
def create_valid_aadhaar():
    aadhaar = np.ones((480, 750, 3), dtype=np.uint8) * 252
    cv2.rectangle(aadhaar, (8, 8), (742, 472), (210, 210, 210), 2)
    
    # Tricolor header bar
    aadhaar[12:20, 12:738] = (40, 130, 235)   # Saffron
    aadhaar[20:28, 12:738] = (245, 245, 245) # White
    aadhaar[28:36, 12:738] = (50, 150, 40)   # Green

    # Government Headers
    cv2.putText(aadhaar, "GOVERNMENT OF INDIA", (220, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.82, (180, 50, 20), 2)
    cv2.putText(aadhaar, "UNIQUE IDENTIFICATION AUTHORITY OF INDIA", (160, 98), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (80, 80, 80), 1)
    
    # Photo box with Avatar
    cv2.rectangle(aadhaar, (35, 120), (215, 340), (230, 230, 230), -1)
    cv2.rectangle(aadhaar, (35, 120), (215, 340), (160, 160, 160), 2)
    draw_face_avatar(aadhaar, 125, 215, scale=0.9)
    
    # Card details
    cv2.putText(aadhaar, "ARJUN KUMAR", (245, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (15, 15, 15), 2)
    cv2.putText(aadhaar, "DOB: 14/05/1998", (245, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.70, (40, 40, 40), 2)
    cv2.putText(aadhaar, "GENDER: MALE", (245, 255), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (50, 50, 50), 2)
    
    # QR Code
    draw_qr_code_mock(aadhaar, 620, 150, size=95)
    
    # 12-Digit Verhoeff valid Aadhaar Number
    cv2.rectangle(aadhaar, (120, 395), (630, 455), (240, 240, 240), -1)
    cv2.putText(aadhaar, "2345  6789  0124", (210, 438), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (10, 10, 10), 3)
    cv2.imwrite("data/samples/valid_aadhaar.jpg", aadhaar)

# =====================================================================
# 2. Genuine PAN Card (Priya Sharma)
# =====================================================================
def create_valid_pan():
    pan = np.ones((480, 750, 3), dtype=np.uint8) * 242
    # Cyan tint background
    pan[:, :, 0] = 245
    pan[:, :, 1] = 230
    pan[:, :, 2] = 215
    cv2.rectangle(pan, (8, 8), (742, 472), (180, 190, 200), 2)
    
    # Header strip
    cv2.rectangle(pan, (10, 10), (740, 95), (225, 240, 250), -1)
    cv2.putText(pan, "INCOME TAX DEPARTMENT", (190, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 30, 140), 2)
    cv2.putText(pan, "GOVT. OF INDIA", (285, 82), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 30, 140), 2)
    
    # Photo box
    cv2.rectangle(pan, (35, 125), (195, 335), (230, 230, 230), -1)
    cv2.rectangle(pan, (35, 125), (195, 335), (140, 140, 140), 2)
    draw_face_avatar(pan, 115, 215, scale=0.85)
    
    # Details
    cv2.putText(pan, "Permanent Account Number Card", (225, 135), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (70, 70, 70), 1)
    cv2.putText(pan, "ABCPS8492K", (225, 185), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (15, 15, 15), 3)
    cv2.putText(pan, "Name: PRIYA SHARMA", (225, 235), cv2.FONT_HERSHEY_SIMPLEX, 0.72, (20, 20, 20), 2)
    cv2.putText(pan, "Father's Name: RAMESH SHARMA", (225, 278), cv2.FONT_HERSHEY_SIMPLEX, 0.60, (50, 50, 50), 2)
    cv2.putText(pan, "Date of Birth: 22/08/2001", (225, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.68, (30, 30, 30), 2)
    
    # Signature line
    cv2.rectangle(pan, (225, 375), (420, 430), (255, 255, 255), -1)
    cv2.putText(pan, "Priya S.", (250, 415), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1.0, (30, 30, 90), 2)
    cv2.imwrite("data/samples/valid_pan.jpg", pan)

# =====================================================================
# 3. Genuine College ID Card (Rahul Verma)
# =====================================================================
def create_valid_college_id():
    cid = np.ones((500, 750, 3), dtype=np.uint8) * 255
    cv2.rectangle(cid, (8, 8), (742, 492), (180, 180, 210), 2)
    
    # Top banner in royal blue
    cv2.rectangle(cid, (10, 10), (740, 105), (160, 60, 20), -1)
    cv2.putText(cid, "INDIAN INSTITUTE OF TECHNOLOGY", (110, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (255, 255, 255), 2)
    cv2.putText(cid, "STUDENT IDENTITY CARD", (240, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (220, 220, 255), 2)
    
    # Photo box
    cv2.rectangle(cid, (40, 135), (210, 355), (240, 240, 240), -1)
    cv2.rectangle(cid, (40, 135), (210, 355), (140, 140, 140), 2)
    draw_face_avatar(cid, 125, 230, scale=0.88, has_glasses=True)
    
    # Student Details
    cv2.putText(cid, "Name: RAHUL VERMA", (235, 175), cv2.FONT_HERSHEY_SIMPLEX, 0.80, (15, 15, 15), 2)
    cv2.putText(cid, "Roll No: 2021CS10452", (235, 225), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (20, 20, 20), 2)
    cv2.putText(cid, "Branch: B.Tech Computer Science", (235, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (40, 40, 40), 2)
    cv2.putText(cid, "DOB: 03/11/2002", (235, 315), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (40, 40, 40), 2)
    cv2.putText(cid, "Valid Upto: 2026", (235, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.70, (20, 110, 30), 2)
    
    # Barcode representation
    for x in range(235, 680, 6):
        if (x // 6) % 3 != 0:
            cv2.line(cid, (x, 410), (x, 465), (20, 20, 20), 2)
    cv2.imwrite("data/samples/valid_college_id.jpg", cid)

# =====================================================================
# 4. Genuine Voter ID Card (Kavita Patel)
# =====================================================================
def create_valid_voter_id():
    voter = np.ones((480, 750, 3), dtype=np.uint8) * 248
    cv2.rectangle(voter, (8, 8), (742, 472), (200, 200, 200), 2)
    
    # Header
    cv2.putText(voter, "ELECTION COMMISSION OF INDIA", (150, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.82, (20, 20, 20), 2)
    cv2.putText(voter, "ELECTOR PHOTO IDENTITY CARD", (190, 88), cv2.FONT_HERSHEY_SIMPLEX, 0.62, (80, 80, 80), 2)
    
    # Photo box
    cv2.rectangle(voter, (35, 120), (205, 340), (235, 235, 235), -1)
    cv2.rectangle(voter, (35, 120), (205, 340), (150, 150, 150), 2)
    draw_face_avatar(voter, 120, 215, scale=0.85)
    
    # EPIC Number
    cv2.rectangle(voter, (235, 125), (480, 168), (235, 245, 255), -1)
    cv2.putText(voter, "WKP4928174", (250, 157), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (100, 20, 10), 2)
    
    # Details
    cv2.putText(voter, "Name: KAVITA PATEL", (235, 215), cv2.FONT_HERSHEY_SIMPLEX, 0.78, (15, 15, 15), 2)
    cv2.putText(voter, "Date of Birth: 30/07/1999", (235, 265), cv2.FONT_HERSHEY_SIMPLEX, 0.70, (40, 40, 40), 2)
    cv2.putText(voter, "Gender: FEMALE", (235, 310), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (50, 50, 50), 2)
    draw_qr_code_mock(voter, 610, 180, size=90)
    cv2.imwrite("data/samples/valid_voter_id.jpg", voter)

# =====================================================================
# 5. Underage ID (Rohan Das, Age 16)
# =====================================================================
def create_underage_id():
    underage = np.ones((480, 750, 3), dtype=np.uint8) * 250
    cv2.rectangle(underage, (8, 8), (742, 472), (210, 210, 210), 2)
    cv2.putText(underage, "GOVERNMENT OF INDIA", (220, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.82, (180, 50, 20), 2)
    
    # Photo box
    cv2.rectangle(underage, (35, 120), (215, 340), (230, 230, 230), -1)
    draw_face_avatar(underage, 125, 215, scale=0.80)
    
    # Details showing 2010 birth date
    cv2.putText(underage, "ROHAN DAS", (245, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (15, 15, 15), 2)
    cv2.putText(underage, "DOB: 12/09/2010", (245, 215), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (20, 20, 20), 2)
    cv2.putText(underage, "GENDER: MALE", (245, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (50, 50, 50), 2)
    cv2.putText(underage, "7829  4018  2741", (210, 435), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (10, 10, 10), 3)
    cv2.imwrite("data/samples/underage_id.jpg", underage)

# =====================================================================
# 6. Tampered Document (Digital Splice Artifacts)
# =====================================================================
def create_tampered_doc():
    tampered = np.ones((480, 750, 3), dtype=np.uint8) * 250
    cv2.rectangle(tampered, (8, 8), (742, 472), (210, 210, 210), 2)
    cv2.putText(tampered, "GOVERNMENT OF INDIA", (220, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.82, (180, 50, 20), 2)
    
    # Base details
    cv2.rectangle(tampered, (35, 120), (215, 340), (230, 230, 230), -1)
    draw_face_avatar(tampered, 125, 215, scale=0.85)
    
    # Spliced rectangle over Name area with distinct high noise & altered color to trigger ELA
    patch = np.ones((60, 420, 3), dtype=np.uint8) * 230
    noise = np.random.randint(-40, 40, patch.shape, dtype=np.int16)
    patch_noisy = np.clip(patch.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    tampered[130:190, 240:660] = patch_noisy
    
    cv2.putText(tampered, "DEVENDRA MEHTA", (255, 172), cv2.FONT_HERSHEY_TRIPLEX, 0.82, (0, 0, 0), 2)
    cv2.putText(tampered, "DOB: 19/04/1995", (245, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.70, (40, 40, 40), 2)
    cv2.putText(tampered, "4920  1948  2910", (210, 435), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (10, 10, 10), 3)
    cv2.imwrite("data/samples/tampered_doc.jpg", tampered)

# =====================================================================
# 7. Blurry Document (Heavy Gaussian Blur)
# =====================================================================
def create_blurry_doc():
    clean = np.ones((480, 750, 3), dtype=np.uint8) * 250
    cv2.putText(clean, "GOVERNMENT OF INDIA", (220, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.82, (180, 50, 20), 2)
    cv2.putText(clean, "SUNITA RAO", (245, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (15, 15, 15), 2)
    cv2.putText(clean, "DOB: 05/12/2000", (245, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.70, (40, 40, 40), 2)
    cv2.putText(clean, "SRAPN2910M", (245, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (30, 30, 30), 2)
    draw_face_avatar(clean, 125, 215, scale=0.85)
    
    blurry = cv2.GaussianBlur(clean, (61, 61), 0)
    cv2.imwrite("data/samples/blurry_doc.jpg", blurry)

# =====================================================================
# 8. Genuine Participant Selfie (Arjun Kumar match)
# =====================================================================
def create_sample_selfie():
    selfie = np.ones((500, 500, 3), dtype=np.uint8) * 242
    # Subtle indoor wall background
    cv2.circle(selfie, (250, 230), 160, (238, 238, 245), -1)
    draw_face_avatar(selfie, 250, 210, scale=1.5)
    cv2.imwrite("data/samples/sample_selfie.jpg", selfie)

# =====================================================================
# 9. Mismatched Selfie (Different Person with Beard & Glasses)
# =====================================================================
def create_mismatch_selfie():
    selfie_mismatch = np.ones((500, 500, 3), dtype=np.uint8) * 235
    draw_face_avatar(selfie_mismatch, 250, 210, scale=1.5, has_glasses=True, has_beard=True)
    cv2.imwrite("data/samples/mismatch_selfie.jpg", selfie_mismatch)

if __name__ == "__main__":
    create_valid_aadhaar()
    create_valid_pan()
    create_valid_college_id()
    create_valid_voter_id()
    create_underage_id()
    create_tampered_doc()
    create_blurry_doc()
    create_sample_selfie()
    create_mismatch_selfie()
    print("[SUCCESS] Successfully generated 9 brand-new synthetic test documents & selfies in data/samples/:")
    for f in os.listdir("data/samples"):
        print(f"  - data/samples/{f}")
