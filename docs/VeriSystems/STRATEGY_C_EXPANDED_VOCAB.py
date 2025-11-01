# STRATEGY C: EXPANDED DISTINCTIVE VOCABULARY
# This file contains the expanded vocabulary for Cat 2 and Cat 6
# To be integrated into Step 4.1 of the notebook

# ============================================================================
# CAT 2: DATA MINIMIZATION - EXPANDED TO 50+ MARKERS
# Focus: QUANTITY/AMOUNT of data collected (not purpose/timing)
# ============================================================================
CAT2_DISTINCTIVE_PHRASES = {
    'amount_focus': [
        # Original 8 phrases
        'du lieu du thua',           # excess/redundant data
        'so luong du lieu toi thieu', # minimum amount of data
        'chi thu thap phan can thiet', # only collect necessary portion
        'giam thieu thu thap',        # reduce collection
        'khong yeu cau qua nhieu',    # don't request too much
        'gioi han pham vi thu thap',  # limit collection scope
        'chi lay nhung gi can',       # only take what's needed
        'tranh thu thap qua muc',     # avoid excessive collection
        # NEW: 10 additional phrases (total 18)
        'chi yeu cau thong tin toi thieu',  # only request minimum information
        'han che so luong du lieu',         # limit data amount
        'khong thu thap qua nhieu thong tin', # don't collect too much info
        'gioi han luong thong tin thu thap', # limit information volume collected
        'chi lay phan du lieu can thiet',   # only take necessary data portion
        'tranh yeu cau qua nhieu du lieu',  # avoid requesting excessive data
        'so luong thong tin phai toi thieu', # information amount must be minimum
        'chi thu thap muc can thiet',       # only collect necessary level
        'khong thu nhieu hon can thiet',    # don't collect more than necessary
        'gioi han khoi luong du lieu'       # limit data volume
    ],
    'minimization_verbs': [
        # Original 5 verbs
        'toi thieu hoa',  # minimize
        'giam thieu',     # reduce
        'gioi han',       # limit (in context of amount)
        'cat giam',       # cut down
        'loai bo phan du thua',  # remove excess
        # NEW: 8 additional verbs (total 13)
        'han che',        # restrict
        'thu hep',        # narrow down
        'rut gon',        # shorten/reduce
        'giam bot',       # decrease
        'loai tru',       # eliminate
        'tiet giam',      # economize
        'cat bot',        # cut off
        'giam sat'        # reduce strictly
    ],
    'unnecessary_markers': [
        # Original 5 markers
        'khong can thiet',   # unnecessary
        'du thua',           # redundant
        'qua muc',           # excessive
        'khong lien quan',   # unrelated
        'ngoai pham vi',     # out of scope
        # NEW: 10 additional markers (total 15)
        'thua',              # excess
        'qua nhieu',         # too much
        'vuot qua muc',      # beyond limit
        'khong thich hop',   # inappropriate
        'khong phu hop',     # not suitable
        'khong thiet yeu',   # not essential
        'khong quan trong',  # not important
        'co the bo qua',     # can be skipped
        'khong bat buoc',    # not mandatory
        'khong he can'       # not needed at all
    ],
    # NEW CATEGORY: Quantity comparisons (8 phrases)
    'quantity_comparisons': [
        'it hon',            # less than
        'toi da',            # maximum
        'toi thieu',         # minimum
        'vua du',            # just enough
        'dung muc',          # right amount
        'khong qua',         # not exceeding
        'chi muc',           # only level
        'gioi han muc'       # limit level
    ]
}

# ============================================================================
# CAT 6: ACCOUNTABILITY - EXPANDED TO 50+ MARKERS
# Focus: PROVING compliance to authorities (not just transparency)
# ============================================================================
CAT6_DISTINCTIVE_PHRASES = {
    'proof_focus': [
        # Original 8 phrases
        'chung minh tuan thu',      # prove compliance
        'bao cao dinh ky',          # periodic reporting
        'luu giu ho so',            # maintain records
        'ghi chep day du',          # complete documentation
        'bao cao cho co quan',      # report to authorities
        'chung minh bang ho so',    # prove with records
        'luu tru bang chung',       # store evidence
        'kiem tra va bao cao',      # audit and report
        # NEW: 10 additional phrases (total 18)
        'xac thuc tuan thu',        # authenticate compliance
        'chung to du lieu',         # demonstrate with data
        'ghi nhan chi tiet',        # detailed recording
        'theo doi va bao cao',      # monitor and report
        'tai lieu chung minh',      # documentary proof
        'bao cao minh chung',       # evidence reporting
        'ho so kiem toan',          # audit records
        'bang chung tuan thu',      # compliance evidence
        'ghi chep kiem toan',       # audit documentation
        'tai lieu bao cao'          # reporting documents
    ],
    'accountability_verbs': [
        # Original 8 verbs
        'chung minh',      # prove
        'bao cao',         # report
        'luu giu',         # maintain/keep
        'ghi chep',        # document/record
        'kiem tra',        # audit
        'gioi trinh',      # account for
        'chung to',        # demonstrate
        'xac nhan',        # verify/confirm
        # NEW: 10 additional verbs (total 18)
        'xac thuc',        # authenticate
        'chung thuc',      # certify
        'minh chung',      # prove/evidence
        'kiem dinh',       # inspect/verify
        'giam sat',        # supervise
        'theo doi',        # track/monitor
        'xac minh',        # verify
        'dang ky',         # register/record
        'luu tru',         # archive
        'bao cao lai'      # report back
    ],
    'authority_markers': [
        # Original 8 markers
        'co quan quan ly',       # regulatory authority
        'thanh tra',             # inspection
        'kiem toan',             # audit
        'bao cao ket qua',       # report results
        'cho co quan nha nuoc',  # for state agencies
        'theo quy dinh bao cao', # as per reporting requirements
        'dinh ky bao cao',       # periodic reporting
        'luu ho so tuan thu',    # maintain compliance records
        # NEW: 8 additional markers (total 16)
        'co quan thanh tra',     # inspection authority
        'bo quan ly',            # managing ministry
        'chinh phu',             # government
        'co quan chu quan',      # competent authority
        'bo phan kiem toan',     # audit department
        'to chuc kiem dinh',     # verification organization
        'ban thanh tra',         # inspection board
        'uy ban giam sat'        # supervisory committee
    ]
}

# ============================================================================
# VALIDATION: Dynamic counts
# ============================================================================
cat2_total = sum(len(v) for v in CAT2_DISTINCTIVE_PHRASES.values())
cat6_total = sum(len(v) for v in CAT6_DISTINCTIVE_PHRASES.values())

print("="*70)
print("STRATEGY C: EXPANDED DISTINCTIVE VOCABULARY")
print("="*70)
print(f"\nCat 2 (Data Minimization) - QUANTITY/AMOUNT focus:")
print(f"  Total markers: {cat2_total}")
for key, phrases in CAT2_DISTINCTIVE_PHRASES.items():
    print(f"  - {key}: {len(phrases)} phrases")

print(f"\nCat 6 (Accountability) - PROOF/REPORTING focus:")
print(f"  Total markers: {cat6_total}")
for key, phrases in CAT6_DISTINCTIVE_PHRASES.items():
    print(f"  - {key}: {len(phrases)} phrases")

print(f"\nTemplate diversity calculation:")
print(f"  Cat 2 markers can generate: ~{cat2_total * 4} unique phrase combinations")
print(f"  Cat 6 markers can generate: ~{cat6_total * 4} unique phrase combinations")
print("="*70)
