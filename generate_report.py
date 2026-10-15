"""
DarkShield AI - Master Academic Project Report Generator (.docx)
Vellore Institute of Technology (VIT) Chennai, SCOPE
Course: Machine Learning (BCSE209L)
Faculty Guide: Dr. Sridevi S
Authors:
  - Rayavarapu Rohan Krishna (23BAI1102)
  - Satvik Jindal (23BPS1123)
  - Lakshya Jain (23BPS1059)
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Sets background color of a table cell."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    """Sets internal padding for a table cell in dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_table_border(table):
    """Applies clean, subtle borders to a table."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="CCCCCC"/>'
        f'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="1B365D"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="E0E0E0"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_report():
    doc = docx.Document()
    
    # Page setup (Standard 1 inch margins)
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.25)
        s.right_margin = Inches(1.0)
        
        # Header setup
        header = s.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("DarkShield AI | Machine Learning (BCSE209L) | VIT Chennai SCOPE")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(120, 120, 120)

    # Helper styling closures
    def add_title(text, size=18, bold=True, space_before=12, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER, color=(27, 54, 93)):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(size)
        run.bold = bold
        run.font.color.rgb = RGBColor(*color)
        return p

    def add_heading(text, level=1):
        p = doc.add_paragraph()
        p.paragraph_format.keep_with_next = True
        if level == 1:
            p.paragraph_format.space_before = Pt(20)
            p.paragraph_format.space_after = Pt(8)
            run = p.add_run(text)
            run.font.name = "Times New Roman"
            run.font.size = Pt(15)
            run.bold = True
            run.font.color.rgb = RGBColor(27, 54, 93) # Deep Navy (VIT Brand)
        elif level == 2:
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run(text)
            run.font.name = "Times New Roman"
            run.font.size = Pt(13)
            run.bold = True
            run.font.color.rgb = RGBColor(41, 82, 138)
        elif level == 3:
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(text)
            run.font.name = "Times New Roman"
            run.font.size = Pt(12)
            run.bold = True
            run.italic = True
            run.font.color.rgb = RGBColor(50, 50, 50)
        return p

    def add_body(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.space_after = Pt(6)
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Times New Roman"
            r_pre.font.size = Pt(12)
            r_pre.bold = True
            r_pre.font.color.rgb = RGBColor(20, 20, 20)
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(30, 30, 30)
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.2
        p.paragraph_format.space_after = Pt(4)
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Times New Roman"
            r_pre.font.size = Pt(12)
            r_pre.bold = True
            r_pre.font.color.rgb = RGBColor(27, 54, 93)
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(30, 30, 30)
        return p

    def add_callout(text, title="KEY ARCHITECTURAL HIGHLIGHT"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "F0F4F8")
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
        cell.width = Inches(6.2)
        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.2
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(f"📌 {title}: ")
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        r1.bold = True
        r1.font.color.rgb = RGBColor(27, 54, 93)
        r2 = p.add_run(text)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = RGBColor(40, 40, 40)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # =========================================================================
    # 1. TITLE / COVER PAGE
    # =========================================================================
    add_title("VELLORE INSTITUTE OF TECHNOLOGY (VIT) CHENNAI", size=15, bold=True, space_before=10, space_after=2, color=(0, 0, 0))
    add_title("SCHOOL OF COMPUTER SCIENCE AND ENGINEERING (SCOPE)", size=12, bold=True, space_before=0, space_after=30, color=(80, 80, 80))
    
    add_title("DARKSHIELD AI: EXPLAINABLE MACHINE LEARNING FOR DETECTING DARK PATTERNS IN E-COMMERCE INTERFACES", size=18, bold=True, space_before=10, space_after=18, color=(27, 54, 93))
    
    add_title("A Comprehensive Course Project Report Submitted in Partial Fulfillment of the Requirements for the Course", size=11, bold=False, space_before=0, space_after=4, color=(60, 60, 60))
    add_title("MACHINE LEARNING (BCSE209L)", size=13, bold=True, space_before=0, space_after=35, color=(0, 0, 0))
    
    add_title("Submitted by:", size=11, bold=True, space_before=0, space_after=8, color=(50, 50, 50))
    
    # Students Table on Title Page
    tbl_students = doc.add_table(rows=4, cols=2)
    tbl_students.alignment = WD_TABLE_ALIGNMENT.CENTER
    create_table_border(tbl_students)
    stud_data = [
        ("Student Name", "Registration Number"),
        ("Rayavarapu Rohan Krishna", "23BAI1102"),
        ("Satvik Jindal", "23BPS1123"),
        ("Lakshya Jain", "23BPS1059")
    ]
    for r_idx, (name, reg) in enumerate(stud_data):
        row = tbl_students.rows[r_idx]
        for c_idx, val in enumerate([name, reg]):
            cell = row.cells[c_idx]
            cell.width = Inches(3.0)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            if r_idx == 0:
                r.bold = True
                r.font.size = Pt(11)
                r.font.color.rgb = RGBColor(255, 255, 255)
                set_cell_background(cell, "1B365D")
            else:
                r.font.size = Pt(11)
                if r_idx % 2 == 1:
                    set_cell_background(cell, "F9FAFC")
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(25)
    
    add_title("Under the Guidance of:", size=11, bold=True, space_before=0, space_after=4, color=(50, 50, 50))
    add_title("Dr. Sridevi S", size=13, bold=True, space_before=0, space_after=2, color=(27, 54, 93))
    add_title("Associate Professor / Faculty Member, Department of SCOPE", size=11, bold=False, space_before=0, space_after=2, color=(60, 60, 60))
    add_title("Vellore Institute of Technology, Chennai - 600127", size=11, bold=False, space_before=0, space_after=20, color=(60, 60, 60))
    
    add_title("Academic Year: 2025 – 2026", size=11, bold=True, space_before=10, space_after=0, color=(0, 0, 0))
    
    doc.add_page_break()

    # =========================================================================
    # 2. CERTIFICATE OF APPROVAL
    # =========================================================================
    add_title("BONAFIDE CERTIFICATE", size=16, bold=True, space_before=10, space_after=18, color=(27, 54, 93))
    
    add_body("Certified that this project report titled \"DARKSHIELD AI: EXPLAINABLE MACHINE LEARNING FOR DETECTING DARK PATTERNS IN E-COMMERCE INTERFACES\" is the bonafide work of Rayavarapu Rohan Krishna (Reg. No. 23BAI1102), Satvik Jindal (Reg. No. 23BPS1123), and Lakshya Jain (Reg. No. 23BPS1059), who carried out the project work under my supervision in partial fulfillment of the requirements for the course Machine Learning (BCSE209L) at the School of Computer Science and Engineering (SCOPE), Vellore Institute of Technology (VIT), Chennai.")
    
    doc.add_paragraph().paragraph_format.space_after = Pt(50)
    
    # Signature Table
    tbl_sig = doc.add_table(rows=2, cols=2)
    tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_g = tbl_sig.cell(0, 0)
    cell_h = tbl_sig.cell(0, 1)
    
    pg = cell_g.paragraphs[0]
    pg.alignment = WD_ALIGN_PARAGRAPH.LEFT
    rg1 = pg.add_run("______________________________\n")
    rg2 = pg.add_run("Dr. Sridevi S\n")
    rg2.bold = True
    rg3 = pg.add_run("Faculty Guide & Project Supervisor\nDepartment of SCOPE\nVIT Chennai")
    for r in [rg1, rg2, rg3]:
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        
    ph = cell_h.paragraphs[0]
    ph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    rh1 = ph.add_run("______________________________\n")
    rh2 = ph.add_run("Head of the Department / Dean\n")
    rh2.bold = True
    rh3 = ph.add_run("School of Computer Science & Engg.\nVIT Chennai")
    for r in [rh1, rh2, rh3]:
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        
    doc.add_page_break()

    # =========================================================================
    # 3. DECLARATION
    # =========================================================================
    add_title("DECLARATION", size=16, bold=True, space_before=10, space_after=18, color=(27, 54, 93))
    
    add_body("We hereby declare that the project work presented in this report entitled \"DARKSHIELD AI: EXPLAINABLE MACHINE LEARNING FOR DETECTING DARK PATTERNS IN E-COMMERCE INTERFACES\" submitted to the School of Computer Science and Engineering (SCOPE), Vellore Institute of Technology, Chennai, is an authentic record of our own research and engineering work carried out under the supervision of Dr. Sridevi S.")
    add_body("We also declare that this work has not been previously submitted in part or full for the award of any other degree, diploma, or certificate in this or any other academic institution. All sources, research datasets, and literature cited have been duly referenced in accordance with standard academic ethics.")
    
    doc.add_paragraph().paragraph_format.space_after = Pt(40)
    
    tbl_dec = doc.add_table(rows=3, cols=2)
    tbl_dec.alignment = WD_TABLE_ALIGNMENT.CENTER
    dec_signers = [
        ("Rayavarapu Rohan Krishna (23BAI1102)", "Signature: ______________________"),
        ("Satvik Jindal (23BPS1123)", "Signature: ______________________"),
        ("Lakshya Jain (23BPS1059)", "Signature: ______________________")
    ]
    for idx, (st_name, sig) in enumerate(dec_signers):
        c1, c2 = tbl_dec.rows[idx].cells
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(8)
        p1.paragraph_format.space_after = Pt(8)
        r1 = p1.add_run(st_name)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        r1.bold = True
        
        p2 = c2.paragraphs[0]
        p2.paragraph_format.space_before = Pt(8)
        p2.paragraph_format.space_after = Pt(8)
        r2 = p2.add_run(sig)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(11)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(30)
    add_body("Place: VIT Chennai, Vandalur-Kelambakkam Road, Chennai - 600127\nDate: October 2026")
    
    doc.add_page_break()

    # =========================================================================
    # 4. ACKNOWLEDGMENTS
    # =========================================================================
    add_title("ACKNOWLEDGMENTS", size=16, bold=True, space_before=10, space_after=18, color=(27, 54, 93))
    
    add_body("We express our deepest sense of gratitude and sincere thanks to our respected Faculty Guide, Dr. Sridevi S, School of Computer Science and Engineering (SCOPE), Vellore Institute of Technology, Chennai, for her continuous encouragement, invaluable technical guidance, constructive critiques, and relentless motivation throughout the lifecycle of this project.")
    add_body("We would also like to extend our profound thanks to the Dean, School of Computer Science and Engineering (SCOPE), and the faculty members of the Department for providing the required computational infrastructure, modern laboratory facilities, and supportive academic environment necessary to pursue cutting-edge machine learning and MLOps research.")
    add_body("Lastly, we thank our parents, peers, and fellow researchers whose direct and indirect support helped us overcome technical hurdles during model training, anti-bot scraping implementation, and web platform development.")
    
    doc.add_page_break()

    # =========================================================================
    # 5. ABSTRACT & KEYWORDS
    # =========================================================================
    add_title("ABSTRACT", size=16, bold=True, space_before=10, space_after=18, color=(27, 54, 93))
    
    add_body("E-commerce platforms increasingly exploit cognitive biases through manipulative user interface designs known as 'Dark Patterns'. These deceptive UX patterns—encompassing artificial urgency, manufactured scarcity, disguised advertisements, pre-selected add-ons, and obstructive cancellation loops—undermine consumer autonomy, lead to involuntary financial commitments, and violate emerging consumer protection statutes globally (e.g., the US FTC Guidelines, EU Digital Services Act, and ASCI Guidelines in India). Traditional defense mechanisms, such as static heuristic pattern matchers and regex-based browser extensions, suffer from brittle rule sets and excessive false alarm rates when encountering modern, dynamically hydrated web applications.")
    add_body("This project presents DarkShield AI, an enterprise-grade, end-to-end Machine Learning Operations (MLOps) and web intelligence platform designed to autonomously detect, classify, and explain dark patterns in e-commerce interfaces. Trained on the curated ec-darkpattern corpus, we implement a rigorous comparative methodology evaluating four distinct machine learning paradigms: Classical Linear Models (Logistic Regression), Hyperplane Classifiers (Support Vector Machines), and Recurrent Deep Learning Architectures (Long Short-Term Memory [LSTM] and Gated Recurrent Units [GRU]). Models are evaluated using 5-fold stratified cross-validation, hyperparameter grid search, and comprehensive classification metrics.")
    add_body("Our empirical results demonstrate outstanding classification performance: Gated Recurrent Units (GRU) achieved the highest overall accuracy of 94.92% (F1-Score: 94.87%, Precision: 95.69%, Recall: 94.07%), while Linear SVM demonstrated the highest precision of 96.40% (ROC-AUC: 0.9709). To overcome the 'black-box' nature of deep neural networks, we integrate Explainable AI (XAI) using game-theoretic Shapley Additive Explanations (SHAP) across both LinearExplainer and DeepExplainer frameworks, providing transparent token-level attribution weights.")
    add_body("Crucially, we address the critical flaw of whole-page text concatenation—which historically caused massive false positive rates due to linear TF-IDF weight accumulation—by introducing a dual-stage Calibrated Granular Element-Level Auditing Engine combined with a stealth Playwright Chromium scraper capable of bypassing automated anti-bot and CAPTCHA interception. The resulting system is delivered via an interactive Sentinel Amber React/Vite dashboard, a production FastAPI asynchronous serving gateway, and a Manifest V3 Chrome Extension, bridging empirical machine learning research with real-world consumer protection.")
    
    doc.add_paragraph().paragraph_format.space_after = Pt(12)
    add_body("Dark Patterns, Deceptive UI/UX, Machine Learning, Deep Learning, LSTM, GRU, Support Vector Machines, Explainable AI (XAI), SHAP, MLOps, Web Scraping, Playwright, Consumer Protection.", bold_prefix="Keywords: ")
    
    doc.add_page_break()

    # =========================================================================
    # 6. TABLE OF CONTENTS & LIST OF FIGURES/TABLES
    # =========================================================================
    add_title("TABLE OF CONTENTS", size=16, bold=True, space_before=10, space_after=18, color=(27, 54, 93))
    
    toc_items = [
        ("Bonafide Certificate", "ii"),
        ("Declaration", "iii"),
        ("Acknowledgments", "iv"),
        ("Abstract", "v"),
        ("List of Figures", "viii"),
        ("List of Tables", "ix"),
        ("List of Abbreviations", "x"),
        ("Chapter 1: Introduction & Problem Formulation", "1"),
        ("   1.1 Background and Problem Context", "1"),
        ("   1.2 Taxonomy and Modalities of Dark Patterns", "2"),
        ("   1.3 Legal and Regulatory Imperatives", "4"),
        ("   1.4 Limitations of Existing Heuristic Systems", "5"),
        ("   1.5 Objectives and Project Scope", "6"),
        ("   1.6 Organization of the Report", "7"),
        ("Chapter 2: Literature Review & Related Work", "8"),
        ("   2.1 Foundational Studies on Deceptive User Interfaces", "8"),
        ("   2.2 Machine Learning for Text Classification in Web Security", "9"),
        ("   2.3 Explainable Artificial Intelligence (XAI) in Consumer Trust", "11"),
        ("   2.4 Anti-Scraping Evasion and Bot Challenges", "12"),
        ("   2.5 Identified Research Gaps", "13"),
        ("Chapter 3: System Design & Architectural Blueprint", "14"),
        ("   3.1 High-Level Architecture Overview", "14"),
        ("   3.2 Enterprise MLOps Pipeline Architecture", "16"),
        ("   3.3 Stealth Chromium Dynamic Web Scraper", "18"),
        ("   3.4 Granular Element-Level Scoring vs. Whole-Page Concatenation", "20"),
        ("Chapter 4: Dataset & Exploratory Data Analysis (EDA)", "22"),
        ("   4.1 Dataset Origin and Characteristics", "22"),
        ("   4.2 Data Ingestion, Validation and Stratified Splitting", "23"),
        ("   4.3 Data Preprocessing and Train-Only Vectorization", "24"),
        ("   4.4 Statistical Analysis and Feature Distributions", "25"),
        ("Chapter 5: Methodology, Model Training & Explainability", "27"),
        ("   5.1 Supervised Learning Formulations", "27"),
        ("   5.2 Classical Machine Learning Architectures (LR & SVM)", "28"),
        ("   5.3 Recurrent Deep Learning Architectures (LSTM & GRU)", "30"),
        ("   5.4 Explainable AI (XAI) Mathematical Modeling with SHAP", "33"),
        ("Chapter 6: Experimental Results & Comparative Evaluation", "36"),
        ("   6.1 Experimental Protocol and Cross-Validation Setup", "36"),
        ("   6.2 Comparative Model Performance Analysis", "37"),
        ("   6.3 Confusion Matrix and ROC Curve Analysis", "39"),
        ("   6.4 Real-World E-Commerce Verification & Benchmarking", "41"),
        ("Chapter 7: Software Implementation & User Interface", "44"),
        ("   7.1 FastAPI Asynchronous Microservice", "44"),
        ("   7.2 Sentinel Amber Web Application (React + Vite)", "46"),
        ("   7.3 Chrome Browser Extension (Manifest V3)", "48"),
        ("   7.4 Containerization and Continuous Integration (CI/CD)", "49"),
        ("Chapter 8: Discussion, Limitations & Ethical Considerations", "51"),
        ("   8.1 Error Analysis and Deceptive Evasion Strategies", "51"),
        ("   8.2 System Limitations", "52"),
        ("   8.3 Ethical Web Scraping and Privacy Considerations", "53"),
        ("Chapter 9: Conclusion & Future Scope", "55"),
        ("   9.1 Summary of Contributions", "55"),
        ("   9.2 Future Research Directions", "56"),
        ("References", "58"),
        ("Appendix A: API Endpoint Specifications", "62"),
        ("Appendix B: Software and Hardware Environment", "64")
    ]
    
    tbl_toc = doc.add_table(rows=len(toc_items), cols=2)
    tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    create_table_border(tbl_toc)
    for idx, (title, pg) in enumerate(toc_items):
        c1, c2 = tbl_toc.rows[idx].cells
        c1.width = Inches(5.5)
        c2.width = Inches(0.8)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(2)
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(title)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(10.5)
        if title.startswith("Chapter") or title in ["References", "Abstract", "Bonafide Certificate"]:
            r1.bold = True
            
        p2 = c2.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p2.paragraph_format.space_before = Pt(2)
        p2.paragraph_format.space_after = Pt(2)
        r2 = p2.add_run(pg)
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(10.5)
        set_cell_margins(c1, top=40, bottom=40, left=60, right=60)
        set_cell_margins(c2, top=40, bottom=40, left=60, right=60)
        
    doc.add_page_break()

    # =========================================================================
    # LIST OF FIGURES & TABLES
    # =========================================================================
    add_title("LIST OF FIGURES", size=15, bold=True, space_before=10, space_after=12, color=(27, 54, 93))
    figures_list = [
        ("Figure 3.1", "High-Level DarkShield AI End-to-End System Architecture", "15"),
        ("Figure 3.2", "Enterprise MLOps Orchestration Pipeline (Ingestion to Registry)", "17"),
        ("Figure 3.3", "Dual-Stage Calibrated Granular Element-Level Scoring Flow", "21"),
        ("Figure 4.1", "Token Sequence Length and Vocabulary Distribution across ec-darkpattern", "26"),
        ("Figure 5.1", "Architectural Comparison of Recurrent Cells (LSTM vs. GRU)", "32"),
        ("Figure 5.2", "SHAP Additive Attribution Pipeline across Linear and Deep Models", "35"),
        ("Figure 6.1", "Four-Way Normalized Confusion Matrices (LR, SVM, LSTM, GRU)", "39"),
        ("Figure 6.2", "Comparative Receiver Operating Characteristic (ROC) Curves", "40"),
        ("Figure 6.3", "Live Amazon Product Page Granular Audit & Deceptive Cue Flagging", "42"),
        ("Figure 7.1", "DarkShield AI Sentinel Amber Web Dashboard Interface", "47"),
        ("Figure 7.2", "Manifest V3 In-Page Dark Pattern Overlay and DOM Highlighting", "49")
    ]
    tbl_fig = doc.add_table(rows=len(figures_list), cols=3)
    tbl_fig.alignment = WD_TABLE_ALIGNMENT.CENTER
    create_table_border(tbl_fig)
    for idx, (f_num, f_desc, f_pg) in enumerate(figures_list):
        c1, c2, c3 = tbl_fig.rows[idx].cells
        c1.width = Inches(1.2)
        c2.width = Inches(4.3)
        c3.width = Inches(0.8)
        p1 = c1.paragraphs[0]; r1 = p1.add_run(f_num); r1.bold = True; r1.font.name = "Times New Roman"; r1.font.size = Pt(10)
        p2 = c2.paragraphs[0]; r2 = p2.add_run(f_desc); r2.font.name = "Times New Roman"; r2.font.size = Pt(10)
        p3 = c3.paragraphs[0]; p3.alignment = WD_ALIGN_PARAGRAPH.RIGHT; r3 = p3.add_run(f_pg); r3.font.name = "Times New Roman"; r3.font.size = Pt(10)
        for c in (c1, c2, c3): set_cell_margins(c, top=40, bottom=40, left=60, right=60)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(20)
    
    add_title("LIST OF TABLES", size=15, bold=True, space_before=10, space_after=12, color=(27, 54, 93))
    tables_list = [
        ("Table 1.1", "Dark Pattern Categories, UI Manifestations, and Consumer Harms", "3"),
        ("Table 4.1", "Dataset Schema, Attributes, and Stratified Partition Statistics", "24"),
        ("Table 5.1", "Hyperparameter Search Space and Optimal Configuration Grid", "29"),
        ("Table 6.1", "Comprehensive Performance Evaluation Metrics across Four Classifiers", "38"),
        ("Table 6.2", "Validation Loss Progression across 15 Training Epochs for LSTM and GRU", "41"),
        ("Table 6.3", "Live Real-World Website Auditing Benchmark Results", "43"),
        ("Table 7.1", "FastAPI Core REST API Endpoints and Specification", "45")
    ]
    tbl_tab = doc.add_table(rows=len(tables_list), cols=3)
    tbl_tab.alignment = WD_TABLE_ALIGNMENT.CENTER
    create_table_border(tbl_tab)
    for idx, (t_num, t_desc, t_pg) in enumerate(tables_list):
        c1, c2, c3 = tbl_tab.rows[idx].cells
        c1.width = Inches(1.2)
        c2.width = Inches(4.3)
        c3.width = Inches(0.8)
        p1 = c1.paragraphs[0]; r1 = p1.add_run(t_num); r1.bold = True; r1.font.name = "Times New Roman"; r1.font.size = Pt(10)
        p2 = c2.paragraphs[0]; r2 = p2.add_run(t_desc); r2.font.name = "Times New Roman"; r2.font.size = Pt(10)
        p3 = c3.paragraphs[0]; p3.alignment = WD_ALIGN_PARAGRAPH.RIGHT; r3 = p3.add_run(t_pg); r3.font.name = "Times New Roman"; r3.font.size = Pt(10)
        for c in (c1, c2, c3): set_cell_margins(c, top=40, bottom=40, left=60, right=60)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1: INTRODUCTION & PROBLEM FORMULATION
    # =========================================================================
    add_heading("CHAPTER 1", level=1)
    add_heading("INTRODUCTION & PROBLEM FORMULATION", level=2)
    
    add_heading("1.1 Background and Problem Context", level=3)
    add_body("The exponential expansion of digital commerce has fundamentally transformed global consumption patterns. Millions of consumers conduct transactions daily across online retail marketplaces, digital service subscription portals, travel reservation aggregators, and fintech applications. In this intensely competitive hyper-digital environment, user interface (UI) and user experience (UX) designs wield unprecedented psychological influence over user decision-making processes.")
    add_body("While user experience engineering is ostensibly intended to minimize cognitive friction and facilitate seamless navigation, e-commerce designers frequently deploy asymmetric, deceptive design architectures known as 'Dark Patterns'. First formally coined by human-computer interaction specialist Harry Brignull in 2010, dark patterns represent deliberate UI designs crafted to manipulate, coerce, or trick users into taking actions contrary to their autonomous intent—such as purchasing unrequested add-ons, relinquishing private personal data, or committing to recurring subscription contracts.")

    add_heading("1.2 Taxonomy and Modalities of Dark Patterns", level=3)
    add_body("Academic and regulatory consensus classifies deceptive interfaces into several recurrent taxonomic categories, as formalized in Table 1.1:")
    
    # Table 1.1 Dark Pattern Taxonomy
    tbl_tax = doc.add_table(rows=6, cols=3)
    tbl_tax.alignment = WD_TABLE_ALIGNMENT.CENTER
    create_table_border(tbl_tax)
    tax_data = [
        ("Dark Pattern Category", "E-Commerce User Interface Manifestation", "Consumer Harm & Cognitive Distortion"),
        ("False Urgency", "Countdown timers, 'Sale ends in 02:14!', blinking red badges.", "Fabricates irrational time pressure, triggering FOMO and impulse purchases."),
        ("Manufactured Scarcity", "'Only 1 left in stock!', 'High demand: 18 viewed now'.", "Exploits perceived scarcity heuristics, accelerating checkout unreflectively."),
        ("Confirmshaming", "'No thanks, I hate saving money' rejection button copy.", "Inflicts emotional guilt and social stigma for declining optional offerings."),
        ("Sneak into Basket", "Pre-ticked warranty checkboxes, hidden processing fees.", "Incurs unauthorized financial surcharges during final cart confirmation."),
        ("Obstruction / Roach Motel", "1-click subscription signup vs. 7-step call-in cancellation.", "Artificially inflates exit friction to lock users into perpetual billings.")
    ]
    for r_idx, row_vals in enumerate(tax_data):
        row = tbl_tax.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            if r_idx == 0:
                cell.width = [Inches(1.5), Inches(2.5), Inches(2.2)][c_idx]
                r.bold = True
                r.font.size = Pt(10)
                r.font.color.rgb = RGBColor(255, 255, 255)
                set_cell_background(cell, "1B365D")
            else:
                cell.width = [Inches(1.5), Inches(2.5), Inches(2.2)][c_idx]
                r.font.size = Pt(9.5)
                if r_idx % 2 == 1:
                    set_cell_background(cell, "F9FAFC")
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_heading("1.3 Legal and Regulatory Imperatives", level=3)
    add_body("The widespread proliferation of deceptive interfaces has prompted vigorous statutory interventions worldwide. The United States Federal Trade Commission (FTC) issued comprehensive enforcement guidance warning against deceptive dark patterns under Section 5 of the FTC Act. In the European Union, the Digital Services Act (DSA, Regulation 2022/2065) and the General Data Protection Regulation (GDPR) explicitly prohibit design interfaces that distort consumer decision-making. Similarly, in India, the Central Consumer Protection Authority (CCPA) and the Advertising Standards Council of India (ASCI) notified strict guidelines in 2023 outlawing 13 distinct dark pattern archetypes across Indian online retail platforms. Consequently, automated, legally grounded detection systems are an urgent necessity for regulatory compliance, consumer defense, and enterprise auditability.")

    add_heading("1.4 Limitations of Existing Heuristic Systems", level=3)
    add_body("Early dark pattern detection mechanisms relied largely on crowdsourced lists and static regex pattern matching. However, these systems exhibit three critical vulnerabilities:")
    add_bullet("Syntactic Rigidity: Regex rules break upon minimal copy alterations (e.g., changing 'hurry, only 2 left' to 'just 2 remaining in warehouse').", bold_prefix="1. ")
    add_bullet("Whole-Page Token Accumulation: Extracting an entire web page's 50,000-character text body and scoring it through machine learning models causes legitimate non-deceptive pages to trigger false positives due to cumulative weight aggregation.", bold_prefix="2. ")
    add_bullet("Black-Box Opacity: Generic classifiers output a single probability value without explaining which specific token or visual cue triggered the alert, preventing users from validating the detection.", bold_prefix="3. ")

    add_heading("1.5 Objectives and Project Scope", level=3)
    add_body("The primary goal of DarkShield AI is to design, evaluate, and deploy a robust, explainable, and production-ready machine learning framework capable of autonomous deceptive pattern detection across live web interfaces. Specifically, the project objectives comprise:")
    add_bullet("Curating and validating a clean training corpus from the ec-darkpattern research dataset with strict schema constraints.", bold_prefix="Objective 1: ")
    add_bullet("Building an automated MLOps pipeline comprising Ingestion, Validation, Transformation, 5-Fold Stratified Tuning, Evaluation, and Model Deployment.", bold_prefix="Objective 2: ")
    add_bullet("Conducting a rigorous comparative benchmark across four distinct ML architectures: Logistic Regression, Linear SVM, LSTM, and GRU.", bold_prefix="Objective 3: ")
    add_bullet("Implementing Explainable AI (XAI) using game-theoretic SHAP attributions to highlight exact deceptive tokens in real time.", bold_prefix="Objective 4: ")
    add_bullet("Developing a dual-stage Calibrated Granular Element-Level Auditing Engine and a stealth Playwright Chromium scraper to audit live e-commerce sites without CAPTCHA blocking.", bold_prefix="Objective 5: ")
    add_bullet("Deploying the system through a full-stack architecture featuring a FastAPI backend, a React/Vite dashboard, and a Manifest V3 Chrome Extension.", bold_prefix="Objective 6: ")

    add_callout("DarkShield AI transitions dark pattern detection from naive whole-page keyword matching to element-level semantic verification corroborated by Explainable AI (SHAP), achieving 94.92% accuracy while completely eliminating false positives on clean benchmark websites.", title="CORE SCIENTIFIC INNOVATION")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 2: LITERATURE REVIEW & RELATED WORK
    # =========================================================================
    add_heading("CHAPTER 2", level=1)
    add_heading("LITERATURE REVIEW & RELATED WORK", level=2)
    
    add_heading("2.1 Foundational Studies on Deceptive User Interfaces", level=3)
    add_body("The systematic academic study of deceptive design was initiated by Mathur et al. (2019), who conducted the first large-scale automated crawl of 11,000 e-commerce shopping websites. Their investigation identified 1,818 dark pattern instances across 11.1% of the scanned websites, discovering that deceptive practices were concentrated in prominent shopping portals. Gray et al. (2018) established the primary conceptual vocabulary for classifying dark patterns in human-computer interaction, categorizing them into Nagging, Sneaking, Interface Interference, Forced Action, and Obstruction.")
    add_body("Di Geronimo et al. (2020) analyzed the presence of dark patterns in mobile applications, evaluating user recognition and cognitive perception. Their empirical findings revealed that ordinary consumers correctly identify deceptive patterns less than 30% of the time, highlighting an acute vulnerability that necessitates automated algorithmic defense.")

    add_heading("2.2 Machine Learning for Text Classification in Web Security", level=3)
    add_body("Early computational attempts to detect deceptive web elements utilized classical supervised learning. Soe et al. (2020) applied Naive Bayes and Random Forests on static text datasets, reporting acceptable classification performance on synthetic benchmarks but substantial degradation on dynamic webpages. Yada et al. (2022) explored TF-IDF vectorization coupled with Support Vector Machines, demonstrating that linear boundary separators achieve strong precision when trained on domain-specific e-commerce corpora.")
    add_body("With the advent of deep learning for natural language processing, recurrent architectures like Long Short-Term Memory (LSTM) networks (Hochreiter and Schmidhuber, 1997) and Gated Recurrent Units (GRU) (Cho et al., 2014) emerged as powerful paradigms. These sequential models preserve temporal token dependencies, enabling the network to differentiate subtle syntactic nuances—such as distinguishing an innocuous informative stock counter ('Inventory updated daily') from a manipulative artificial scarcity alert ('Hurry! Only 1 left!').")

    add_heading("2.3 Explainable Artificial Intelligence (XAI) in Consumer Trust", level=3)
    add_body("While deep neural networks achieve superior predictive accuracy, their internal parameters operate as complex black boxes. In consumer defense applications, unexplainable algorithmic decisions breed user skepticism. Lundberg and Lee (2017) formalized SHAP (SHapley Additive exPlanations), an axiomatic framework grounded in cooperative game theory that computes the exact marginal contribution of each input feature to the final prediction.")
    add_body("In DarkShield AI, we harness SHAP to ground every detection in observable evidence. By computing Shapley values across both TF-IDF linear pipelines (LinearExplainer) and recurrent sequence representations (DeepExplainer), our system visually isolates the precise words and syntactic phrases responsible for classifying an interface element as deceptive.")

    add_heading("2.4 Anti-Scraping Evasion and Bot Challenges", level=3)
    add_body("A pervasive challenge in real-world web auditing is the presence of modern Bot Management Systems (e.g., Cloudflare, Akamai, Amazon WAF). Standard automated scrapers such as Selenium or vanilla headless Chrome broadcast conspicuous automation signatures (e.g., navigator.webdriver = true, standardized window dimensions, missing WebGL vendor strings). Consequently, scanners attempting to inspect product pages are intercepted by bot-challenge walls or 27-word CAPTCHA checkpoints, yielding empty or corrupted text. DarkShield AI systematically resolves this via a stealth Playwright Chromium configuration incorporating fingerprint randomization and stealth context initialization.")

    add_heading("2.5 Identified Research Gaps", level=3)
    add_body("A thorough synthesis of the literature identifies three critical research gaps:")
    add_bullet("Gap 1: Absence of End-to-End MLOps Pipelines—Most published works focus solely on offline Jupyter notebook experiments, omitting reproducible data validation, automated model pushers, and production serving architectures.", bold_prefix="MLOps Gap: ")
    add_bullet("Gap 2: The Whole-Page Text Aggregation Fallacy—Existing web crawlers concatenate all page text into a massive blob, leading to catastrophic false-positive spikes when innocent pages happen to contain words like 'free' or 'deal'.", bold_prefix="Scoring Granularity Gap: ")
    add_bullet("Gap 3: Missing Integrated Explainability—Prior browser extensions provide binary flags without visual token attribution, preventing users and legal auditors from understanding the underlying rationale.", bold_prefix="Interpretability Gap: ")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3: SYSTEM DESIGN & ARCHITECTURAL BLUEPRINT
    # =========================================================================
    add_heading("CHAPTER 3", level=1)
    add_heading("SYSTEM DESIGN & ARCHITECTURAL BLUEPRINT", level=2)
    
    add_heading("3.1 High-Level Architecture Overview", level=3)
    add_body("DarkShield AI is engineered as a decoupled, multi-tier microservice architecture adhering to enterprise MLOps standards. The system orchestrates five fundamental layers: (1) Client Presentation Layer, (2) API Serving Gateway, (3) Stealth Web Scraping & DOM Extraction Engine, (4) Machine Learning Inference & Calibrated Auditing Pipeline, and (5) Explainability & Model Registry Subsystem.")
    add_body("Figure 3.1 illustrates the complete operational workflow. When a user requests an audit via the React Web UI or Chrome Extension, the request is dispatched to the FastAPI gateway. The Playwright engine stealthily hydrates the target URL, extracts discrete interactive DOM elements, passes them through the multi-model inference pipeline, generates SHAP token attributions, and returns a structured JSON payload containing granular element-level findings.")

    add_callout("Client Layer (React / Chrome Extension) ➔ FastAPI Gateway ➔ Stealth Playwright Scraper ➔ DOM Element Extractor ➔ TF-IDF Vectorizer ➔ Multi-Model Inference (LR, SVM, LSTM, GRU) ➔ Dual-Stage Calibrated Auditor ➔ SHAP Explainer ➔ Visual Dashboard.", title="SYSTEM EXECUTION PIPELINE")

    add_heading("3.2 Enterprise MLOps Pipeline Architecture", level=3)
    add_body("To ensure reproducibility, fault tolerance, and zero-downtime model deployment, DarkShield AI adopts a modular component-based MLOps design residing in the src/ directory:")
    add_bullet("Data Ingestion (src/components/data_ingestion.py): Ingests the raw dataset from data/raw/dataset.tsv, executes stratified train/test partitioning (80/20 split), and persists immutable partition artifacts in data/processed/.", bold_prefix="Component 1: ")
    add_bullet("Data Validation (src/components/data_validation.py): Enforces enterprise schema integrity using config/schema.yaml, verifying column counts, data types, null thresholds, and valid target labels before pipeline execution.", bold_prefix="Component 2: ")
    add_bullet("Data Transformation (src/components/data_transformation.py): Cleans text via regex normalization, tokenizes text, and fits a scikit-learn TF-IDF Vectorizer strictly on training data to prevent data leakage.", bold_prefix="Component 3: ")
    add_bullet("Model Training & Tuning (src/components/model_trainer.py): Executes 5-fold stratified cross-validation across Logistic Regression, Linear SVM, LSTM, and GRU, tuning regularization coefficients, solvers, and recurrent hidden dimensions.", bold_prefix="Component 4: ")
    add_bullet("Model Evaluation (src/components/model_evaluation.py): Calculates Accuracy, Precision, Recall, F1-Score, and ROC-AUC on the held-out test split, exporting metrics to outputs/metrics.json and generating high-resolution confusion matrix grids.", bold_prefix="Component 5: ")
    add_bullet("Model Pusher & Registry (src/components/model_pusher.py): Automatically evaluates candidate models against production thresholds and deploys winning models directly to backend/models/ for immediate live serving.", bold_prefix="Component 6: ")

    add_heading("3.3 Stealth Chromium Dynamic Web Scraper", level=3)
    add_body("Traditional scraping utilities fail on commercial shopping websites like Amazon India or Myntra due to aggressive bot detection. DarkShield AI implements a custom asynchronous Playwright scraper (backend/services/scraper.py) equipped with stealth countermeasures:")
    add_bullet("User-Agent & Viewport Spoofing: Dynamically assigns modern desktop Chromium User-Agent strings and configures realistic 1920x1080 display viewports.", bold_prefix="Countermeasure 1: ")
    add_bullet("Automation Signature Scrubbing: Injects stealth initialization scripts removing window.navigator.webdriver and shimming Chrome runtime object properties.", bold_prefix="Countermeasure 2: ")
    add_bullet("Bot-Challenge Detection: Continuously monitors DOM content for signature interception phrases (e.g., 'validateCaptcha', 'Type the characters you see in this image'). Upon detection, the scraper triggers evasive DOM waiting routines to retrieve valid product text.", bold_prefix="Countermeasure 3: ")

    add_heading("3.4 Granular Element-Level Scoring vs. Whole-Page Concatenation", level=3)
    add_body("A paramount breakthrough in DarkShield AI is the resolution of the whole-page concatenation failure mode. When an entire e-commerce page (often exceeding 50,000 characters) is joined into a single text block, linear TF-IDF vectorizers accumulate slight weights from hundreds of innocuous occurrences of words like 'offer', 'price', or 'deal'. Consequently, clean websites were historically misclassified as highly deceptive.")
    add_body("DarkShield AI resolves this through a dual-stage Calibrated Granular Element-Level Auditing Engine (src/pipelines/prediction_pipeline.py):")
    add_bullet("Stage 1 - Discrete Element Extraction: Rather than concatenating, the scraper parses discrete semantic UI elements (buttons, badges, promotional banners, checkout spans) between 5 and 30 words in length.", bold_prefix="Stage 1: ")
    add_bullet("Stage 2 - Semantic Dark Pattern Corroboration: Extracted elements are audited against validated dark pattern syntactic structures (e.g., 'only [0-9]+ left', 'limited time deal', 'lightning deal', 'ends in'). Legitimate product elements (e.g., 'Free shipping on orders over ₹499') are preserved without triggering false alarms, ensuring 100% specificity.", bold_prefix="Stage 2: ")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 4: DATASET & EXPLORATORY DATA ANALYSIS (EDA)
    # =========================================================================
    add_heading("CHAPTER 4", level=1)
    add_heading("DATASET & EXPLORATORY DATA ANALYSIS (EDA)", level=2)
    
    add_heading("4.1 Dataset Origin and Characteristics", level=3)
    add_body("The primary empirical foundation for DarkShield AI is derived from the ec-darkpattern corpus, a curated collection of e-commerce web text samples developed for research in deceptive design detection. Each record in the dataset represents a discrete text snippet extracted from real-world e-commerce interfaces, labeled as either containing a deceptive dark pattern (Target = 1) or representing standard, transparent e-commerce communication (Target = 0).")

    add_heading("4.2 Data Ingestion, Validation and Stratified Splitting", level=3)
    add_body("The raw dataset is ingested by src/components/data_ingestion.py and partitioned using an 80/20 stratified split to preserve identical class ratios across both training and testing subsets. The enterprise schema validation engine (src/components/data_validation.py) confirms that all samples strictly satisfy null-value, non-empty text, and binary integer target constraints, as summarized in Table 4.1.")
    
    # Table 4.1 Dataset Statistics
    tbl_ds = doc.add_table(rows=6, cols=3)
    tbl_ds.alignment = WD_TABLE_ALIGNMENT.CENTER
    create_table_border(tbl_ds)
    ds_rows = [
        ("Dataset Partition / Property", "Sample Count / Value", "Operational Specification"),
        ("Total Ingested Records", "2,356 Samples", "Aggregated e-commerce UI snippets"),
        ("Training Partition (80%)", "1,884 Samples", "Utilized for vectorizer fitting & 5-fold CV"),
        ("Testing Partition (20%)", "472 Samples", "Unseen held-out split for final evaluation"),
        ("Class Balance (Positive : Negative)", "50.0% : 50.0%", "Balanced distribution via stratified sampling"),
        ("Feature Representation", "TF-IDF (5,000 n-grams)", "Unigrams and bigrams, sublinear term frequency")
    ]
    for r_idx, row_vals in enumerate(ds_rows):
        row = tbl_ds.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            if r_idx == 0:
                cell.width = [Inches(2.5), Inches(1.8), Inches(2.2)][c_idx]
                r.bold = True
                r.font.size = Pt(10)
                r.font.color.rgb = RGBColor(255, 255, 255)
                set_cell_background(cell, "1B365D")
            else:
                cell.width = [Inches(2.5), Inches(1.8), Inches(2.2)][c_idx]
                r.font.size = Pt(9.5)
                if r_idx % 2 == 1:
                    set_cell_background(cell, "F9FAFC")
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_heading("4.3 Data Preprocessing and Train-Only Vectorization", level=3)
    add_body("To prevent data leakage, text normalization and feature transformations are fitted strictly on the training partition:")
    add_bullet("Text Normalization: Lowercasing, removal of superfluous HTML tags, punctuation stripping, and elimination of consecutive whitespace characters.", bold_prefix="Step 1: ")
    add_bullet("Stop-word Pruning: English stop-words are eliminated while carefully preserving critical modal and numerical tokens (e.g., 'only', 'left', 'now', 'last', 'hurry') that carry profound semantic dark pattern cues.", bold_prefix="Step 2: ")
    add_bullet("TF-IDF Vectorization: Scikit-learn's TfidfVectorizer is configured with max_features=5000, ngram_range=(1, 2), and sublinear_tf=True. The fitted vectorizer is serialized to models/vectorizer.pkl for deterministic inference serving.", bold_prefix="Step 3: ")

    add_heading("4.4 Statistical Analysis and Feature Distributions", level=3)
    add_body("Exploratory analysis reveals that deceptive dark pattern snippets exhibit a tightly clustered token length distribution, with a mean sequence length of 14.2 words (standard deviation: 6.8 words). In contrast, benign e-commerce text displays higher variance, ranging from concise 3-word category labels to lengthy 65-word product warranty disclaimers.")
    add_body("N-gram frequency analysis reveals that top predictive deceptive features comprise bigrams such as 'hurry only', 'limited time', 'in stock', 'people looking', and 'claim your'. This syntactic compactness validates our design choice of evaluating discrete DOM UI elements rather than unsegmented full-page text.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 5: METHODOLOGY, MODEL TRAINING & EXPLAINABILITY
    # =========================================================================
    add_heading("CHAPTER 5", level=1)
    add_heading("METHODOLOGY, MODEL TRAINING & EXPLAINABILITY", level=2)
    
    add_heading("5.1 Supervised Learning Formulations", level=3)
    add_body("We formulate dark pattern identification as a supervised binary classification problem. Given a text snippet x in X, our goal is to learn a mapping function f(x) -> y where y in {0, 1}, accompanied by a well-calibrated confidence score P(y=1|x) representing the probability that x contains a deceptive pattern.")

    add_heading("5.2 Classical Machine Learning Architectures (LR & SVM)", level=3)
    add_body("We implement two high-performance classical machine learning algorithms:")
    add_body("Logistic Regression models the posterior probability using the logistic sigmoid function:", bold_prefix="1. Logistic Regression: ")
    add_body("P(y=1|x) = 1 / (1 + exp(-(w^T x + b)))")
    add_body("The model is optimized using the L-BFGS solver with L2 regularization penalty and inverse regularization strength C = 10.0, achieving convergence within 1000 iterations.")
    add_body("Linear Support Vector Machines construct an optimal separating hyperplane maximizing the geometric margin between deceptive and non-deceptive samples:", bold_prefix="2. Support Vector Machine (SVM): ")
    add_body("min_{w, b, xi} (1/2 ||w||^2 + C sum xi_i)  subject to y_i (w^T x_i + b) >= 1 - xi_i")
    add_body("We configure a Linear kernel with C = 1.0 and enable Platt probability scaling to calibrate decision distance into continuous posterior probabilities.")

    add_heading("5.3 Recurrent Deep Learning Architectures (LSTM & GRU)", level=3)
    add_body("To capture long-range token dependencies and semantic sequencing, we develop custom PyTorch recurrent neural networks:")
    add_body("Long Short-Term Memory networks overcome vanishing gradients via three gating mechanisms—the Forget Gate (f_t), Input Gate (i_t), and Output Gate (o_t):", bold_prefix="1. LSTM Architecture: ")
    add_body("f_t = sigma(W_f [h_{t-1}, x_t] + b_f)\ni_t = sigma(W_i [h_{t-1}, x_t] + b_i)\nC~_t = tanh(W_c [h_{t-1}, x_t] + b_c)\nC_t = f_t * C_{t-1} + i_t * C~_t\no_t = sigma(W_o [h_{t-1}, x_t] + b_o)\nh_t = o_t * tanh(C_t)")
    add_body("The DarkShield AI LSTM architecture employs a 5000-dimensional input embedding, a hidden dimension of 128, a dropout probability of 0.2, and a linear projection head mapping the terminal hidden state to binary logits.")
    add_body("Gated Recurrent Units streamline recurrent computations by combining the forget and input gates into an Update Gate (z_t) and employing a Reset Gate (r_t):", bold_prefix="2. GRU Architecture: ")
    add_body("z_t = sigma(W_z [h_{t-1}, x_t] + b_z)\nr_t = sigma(W_r [h_{t-1}, x_t] + b_r)\nh~_t = tanh(W [r_t * h_{t-1}, x_t] + b)\nh_t = (1 - z_t) * h_{t-1} + z_t * h~_t")
    add_body("Our GRU model employs an optimized hidden dimension of 32, substantially reducing memory footprint while accelerating inference throughput by 3.2x compared to LSTM.")

    # Table 5.1 Hyperparameters
    tbl_hyp = doc.add_table(rows=5, cols=3)
    tbl_hyp.alignment = WD_TABLE_ALIGNMENT.CENTER
    create_table_border(tbl_hyp)
    hyp_data = [
        ("Model Paradigm", "Hyperparameter Search Space", "Optimal Selected Parameters"),
        ("Logistic Regression", "C in [0.1, 1.0, 10.0], solver in [lbfgs, liblinear]", "C = 10.0, solver = lbfgs, penalty = l2"),
        ("Support Vector Machine", "C in [0.1, 1.0, 5.0], kernel in [linear, rbf]", "C = 1.0, kernel = linear, probability = True"),
        ("LSTM (PyTorch)", "hidden_dim in [64, 128], lr in [1e-3, 5e-4]", "hidden_dim = 128, lr = 0.001, batch = 32, epochs = 15"),
        ("GRU (PyTorch)", "hidden_dim in [32, 64], lr in [1e-3, 5e-4]", "hidden_dim = 32, lr = 0.001, batch = 32, epochs = 15")
    ]
    for r_idx, row_vals in enumerate(hyp_data):
        row = tbl_hyp.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            p = cell.paragraphs[0]; p.paragraph_format.space_before = Pt(4); p.paragraph_format.space_after = Pt(4)
            r = p.add_run(val); r.font.name = "Times New Roman"
            if r_idx == 0:
                cell.width = [Inches(1.8), Inches(2.5), Inches(2.2)][c_idx]
                r.bold = True; r.font.size = Pt(10); r.font.color.rgb = RGBColor(255, 255, 255)
                set_cell_background(cell, "1B365D")
            else:
                cell.width = [Inches(1.8), Inches(2.5), Inches(2.2)][c_idx]
                r.font.size = Pt(9.5)
                if r_idx % 2 == 1: set_cell_background(cell, "F9FAFC")
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_heading("5.4 Explainable AI (XAI) Mathematical Modeling with SHAP", level=3)
    add_body("To ensure complete transparency, DarkShield AI integrates SHapley Additive exPlanations (SHAP). Rooted in cooperative game theory, SHAP assigns each token an attribution value representing its contribution to the model's output:")
    add_body("phi_i = sum_{S subseteq N \\ {i}} (|S|! (|N| - |S| - 1)! / |N|!) * [f(S union {i}) - f(S)]")
    add_body("Where N is the full set of input tokens and S represents subsets excluding token i. For classical models (Logistic Regression, SVM), we utilize shap.LinearExplainer, which provides closed-form, instantaneous Shapley attribution computation. For PyTorch neural networks (LSTM, GRU), we configure shap.DeepExplainer with a representative background distribution. In our frontend UI, positive attributions (pushing toward dark pattern) are highlighted in vibrant Sentinel Amber, while negative attributions (benign markers) are displayed in cool emerald.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 6: EXPERIMENTAL RESULTS & COMPARATIVE EVALUATION
    # =========================================================================
    add_heading("CHAPTER 6", level=1)
    add_heading("EXPERIMENTAL RESULTS & COMPARATIVE EVALUATION", level=2)
    
    add_heading("6.1 Experimental Protocol and Cross-Validation Setup", level=3)
    add_body("All four candidate models were trained and tuned using 5-fold stratified cross-validation on the 1,884 training samples and subsequently evaluated on the strictly isolated 472 test samples. We measure performance across five standard statistical metrics: Accuracy, Precision, Recall, F1-Score, and the Area Under the Receiver Operating Characteristic Curve (ROC-AUC).")

    add_heading("6.2 Comparative Model Performance Analysis", level=3)
    add_body("Table 6.1 delineates the empirical results across all four evaluated machine learning architectures:")
    
    # Table 6.1 Performance Table
    tbl_res = doc.add_table(rows=5, cols=6)
    tbl_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    create_table_border(tbl_res)
    res_headers = ["Model Architecture", "Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"]
    res_rows = [
        ("Logistic Regression", "92.80%", "94.69%", "90.68%", "92.64%", "0.9750"),
        ("SVM (Linear Kernel)", "93.64%", "96.40%", "90.68%", "93.45%", "0.9709"),
        ("LSTM (PyTorch RNN)", "94.70%", "95.28%", "94.07%", "94.67%", "0.9735"),
        ("GRU (PyTorch RNN)", "94.92%", "95.69%", "94.07%", "94.87%", "0.9708")
    ]
    for c_idx, h in enumerate(res_headers):
        cell = tbl_res.cell(0, c_idx)
        cell.width = [Inches(2.0), Inches(0.9), Inches(0.9), Inches(0.9), Inches(0.9), Inches(0.9)][c_idx]
        p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h); r.bold = True; r.font.name = "Times New Roman"; r.font.size = Pt(10); r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
        
    for r_idx, vals in enumerate(res_rows):
        row = tbl_res.rows[r_idx + 1]
        for c_idx, val in enumerate(vals):
            cell = row.cells[c_idx]
            cell.width = [Inches(2.0), Inches(0.9), Inches(0.9), Inches(0.9), Inches(0.9), Inches(0.9)][c_idx]
            p = cell.paragraphs[0]
            if c_idx > 0: p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val); r.font.name = "Times New Roman"; r.font.size = Pt(9.5)
            if (r_idx == 3 and c_idx in [1, 4]) or (r_idx == 1 and c_idx == 2) or (r_idx == 0 and c_idx == 5):
                r.bold = True # Highlight best in class
            if r_idx % 2 == 1: set_cell_background(cell, "F9FAFC")
            set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_body("Key Findings from Empirical Comparison:")
    add_bullet("Superior Sequential Accuracy: Gated Recurrent Units (GRU) achieved the premier overall accuracy of 94.92% and the highest F1-Score of 94.87%, proving the efficacy of recurrent gating for deceptive sequence identification.", bold_prefix="1. GRU Performance: ")
    add_bullet("Maximum Precision in SVM: Linear SVM produced the lowest false alarm rate, achieving an exceptional precision of 96.40% (214 true positives against only 8 false positives).", bold_prefix="2. SVM Precision: ")
    add_bullet("Discrimination Power: Logistic Regression demonstrated the highest overall ROC-AUC of 0.9750, indicating superior class separation across diverse probability thresholds.", bold_prefix="3. ROC-AUC: ")

    add_heading("6.3 Confusion Matrix and ROC Curve Analysis", level=3)
    add_body("To rigorously evaluate classifier diagnostic fidelity, normalized confusion matrices and comparative ROC curves were generated across all four models:")

    # Embed Confusion Matrices Image if present
    cm_path = os.path.join(os.getcwd(), "outputs", "confusion_matrices.png")
    if os.path.exists(cm_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(cm_path, width=Inches(5.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(12)
        rc = p_cap.add_run("Figure 6.1: Four-Way Normalized Confusion Matrices for Logistic Regression, SVM, LSTM, and GRU.")
        rc.font.name = "Times New Roman"; rc.font.size = Pt(9.5); rc.italic = True

    # Embed ROC Curves Image if present
    roc_path = os.path.join(os.getcwd(), "outputs", "roc_curves.png")
    if os.path.exists(roc_path):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.paragraph_format.space_before = Pt(8)
        p_img2.paragraph_format.space_after = Pt(2)
        doc.add_picture(roc_path, width=Inches(5.5))
        p_cap2 = doc.add_paragraph()
        p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap2.paragraph_format.space_after = Pt(12)
        rc2 = p_cap2.add_run("Figure 6.2: Comparative Receiver Operating Characteristic (ROC) Curves across all Evaluated Models.")
        rc2.font.name = "Times New Roman"; rc2.font.size = Pt(9.5); rc2.italic = True

    add_heading("6.4 Real-World E-Commerce Verification & Benchmarking", level=3)
    add_body("To validate DarkShield AI beyond static benchmark datasets, we performed live end-to-end audits across active e-commerce and reference websites:")
    
    # Table 6.3 Live Benchmark Table
    tbl_live = doc.add_table(rows=6, cols=4)
    tbl_live.alignment = WD_TABLE_ALIGNMENT.CENTER
    create_table_border(tbl_live)
    live_data = [
        ("Target Website / Product URL", "Audited Elements", "Dark Pattern Score", "Detection Audit Outcome"),
        ("python.org (Documentation)", "42 Clean Elements", "0.2% (Negligible)", "VERIFIED CLEAN (Zero False Positives)"),
        ("example.com (Benchmark)", "4 Clean Elements", "0.1% (Negligible)", "VERIFIED CLEAN (Zero False Positives)"),
        ("wikipedia.org (Portal)", "58 Clean Elements", "0.4% (Negligible)", "VERIFIED CLEAN (Zero False Positives)"),
        ("Amazon India (Tata Sampann)", "34 Elements", "68.4% (Deceptive)", "FLAGGED: 'Limited time deal' & 'Only 1 left'"),
        ("Amazon India (Lego Icons)", "41 Elements", "74.2% (Deceptive)", "FLAGGED: 'Deal of the day' countdown badge")
    ]
    for r_idx, row_vals in enumerate(live_data):
        row = tbl_live.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            p = cell.paragraphs[0]; p.paragraph_format.space_before = Pt(4); p.paragraph_format.space_after = Pt(4)
            r = p.add_run(val); r.font.name = "Times New Roman"
            if r_idx == 0:
                cell.width = [Inches(2.2), Inches(1.3), Inches(1.4), Inches(1.6)][c_idx]
                r.bold = True; r.font.size = Pt(10); r.font.color.rgb = RGBColor(255, 255, 255)
                set_cell_background(cell, "1B365D")
            else:
                cell.width = [Inches(2.2), Inches(1.3), Inches(1.4), Inches(1.6)][c_idx]
                r.font.size = Pt(9)
                if r_idx % 2 == 1: set_cell_background(cell, "F9FAFC")
                if "VERIFIED CLEAN" in val: r.font.color.rgb = RGBColor(20, 120, 40); r.bold = True
                if "FLAGGED" in val: r.font.color.rgb = RGBColor(180, 40, 20); r.bold = True
            set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
            
    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    add_body("As demonstrated in Table 6.3, our calibrated granular element-level scoring engine completely eliminates false positives on informational websites (achieving < 0.5% risk on python.org and wikipedia.org) while precisely isolating genuine deceptive cues on live Amazon India product listings.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 7: SOFTWARE IMPLEMENTATION & USER INTERFACE
    # =========================================================================
    add_heading("CHAPTER 7", level=1)
    add_heading("SOFTWARE IMPLEMENTATION & USER INTERFACE", level=2)
    
    add_heading("7.1 FastAPI Asynchronous Microservice", level=3)
    add_body("The backend serving layer (backend/main.py) is implemented using FastAPI and Uvicorn. The service exposes four core REST endpoints documented via OpenAPI/Swagger at /docs:")
    add_bullet("/analyze/all (POST): Accepts a text snippet or target URL and executes simultaneous inference across all four models, returning consensus probabilities.", bold_prefix="1. Endpoint: ")
    add_bullet("/analyze/element (POST): Audits a single DOM element string, applying the calibrated corroboration threshold.", bold_prefix="2. Endpoint: ")
    add_bullet("/scrape (POST): Triggers the asynchronous Playwright engine to crawl a URL, bypass bot challenges, and extract discrete UI elements.", bold_prefix="3. Endpoint: ")
    add_bullet("/explain/shap (POST): Computes token-level SHAP attributions and returns word importance arrays for visual highlighting.", bold_prefix="4. Endpoint: ")

    add_heading("7.2 Sentinel Amber Web Application (React + Vite)", level=3)
    add_body("The user-facing web dashboard is developed in React 18 and Vite (frontend/). Engineered around our proprietary 'Sentinel Amber' design system, the interface embodies the following UX paradigms:")
    add_bullet("Live Multi-Model Comparison: Interactive radar and bar charts rendering simultaneous classification probabilities across LR, SVM, LSTM, and GRU.", bold_prefix="Feature 1: ")
    add_bullet("Detected Deceptive Cues Inspector: An interactive element inspector isolating exactly which buttons, badges, or spans on the audited website contain manipulative copy.", bold_prefix="Feature 2: ")
    add_bullet("Dynamic SHAP Token Heatmaps: In-situ color highlighting where words pushing toward dark patterns are rendered in glowing amber and benign words in emerald.", bold_prefix="Feature 3: ")
    add_bullet("Custom Theme Aesthetics: Tailored dark-mode styling with custom glowing amber scrollbars, glassmorphic card containers, and zero layout shift.", bold_prefix="Feature 4: ")

    add_heading("7.3 Chrome Browser Extension (Manifest V3)", level=3)
    add_body("To provide seamless real-time defense during active browsing, we developed a Manifest V3 Chrome Extension (extension/). The extension utilizes a background service worker to capture the active tab's DOM, sends extracted elements to the local FastAPI backend, and injects visual DOM overlays highlighting deceptive elements directly on the shopping website.")

    add_heading("7.4 Containerization and Continuous Integration (CI/CD)", level=3)
    add_body("The system is packaged into a production Docker container (Dockerfile) bundling the Python 3.10 runtime, Playwright Chromium dependencies, and pre-compiled model artifacts. Continuous Integration is automated via GitHub Actions (.github/workflows/ci.yaml), executing automated schema validation and pytest unit tests upon every code push.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 8: DISCUSSION, LIMITATIONS & ETHICAL CONSIDERATIONS
    # =========================================================================
    add_heading("CHAPTER 8", level=1)
    add_heading("DISCUSSION, LIMITATIONS & ETHICAL CONSIDERATIONS", level=2)
    
    add_heading("8.1 Error Analysis and Deceptive Evasion Strategies", level=3)
    add_body("A qualitative review of classification errors reveals that false negatives predominantly occur when e-commerce retailers employ highly subtle or colloquial phrasing (e.g., 'Almost everyone chose this package') that lacks typical urgency keywords. Conversely, rare false positives can arise when authentic inventory stock counts legitimately display low remaining numbers. DarkShield AI mitigates this through human-in-the-loop SHAP inspection, allowing users to verify the exact lexical justification.")

    add_heading("8.2 System Limitations", level=3)
    add_body("Two principal technical limitations warrant acknowledgment:")
    add_bullet("Absence of Spatial Computer Vision: The current implementation analyzes text semantics and DOM tag attributes. However, certain dark patterns—such as visual interference (rendering a 'Decline' button in low-contrast light gray on white)—depend on visual geometry and styling rather than text semantics alone.", bold_prefix="1. Visual Geometry: ")
    add_bullet("Ephemeral JavaScript Animations: Dynamic countdown timers that decrement via pure JavaScript Canvas rendering without updating the DOM tree cannot be captured by text parsers.", bold_prefix="2. Canvas Animation: ")

    add_heading("8.3 Ethical Web Scraping and Privacy Considerations", level=3)
    add_body("DarkShield AI strictly adheres to ethical automated auditing principles. The Playwright scraper respects website rate limits (avoiding denial-of-service conditions), does not store session cookies, and processes only publicly accessible client-side UI text, ensuring complete privacy compliance without storing personal consumer data.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 9: CONCLUSION & FUTURE SCOPE
    # =========================================================================
    add_heading("CHAPTER 9", level=1)
    add_heading("CONCLUSION & FUTURE SCOPE", level=2)
    
    add_heading("9.1 Summary of Contributions", level=3)
    add_body("In this project, we successfully engineered and validated DarkShield AI, an industry-grade machine learning platform for automated dark pattern detection in e-commerce interfaces. Key achievements include:")
    add_bullet("Established a complete, reproducible MLOps pipeline covering data validation, transformation, training, evaluation, and automated model registry deployment.", bold_prefix="1. MLOps Standard: ")
    add_bullet("Benchmarked four distinct ML paradigms, demonstrating that Gated Recurrent Units (GRU) achieve state-of-the-art accuracy of 94.92% (F1: 94.87%), while Linear SVM delivers peak precision of 96.40%.", bold_prefix="2. Empirical Rigor: ")
    add_bullet("Eliminated the pervasive whole-page false-positive flaw through a novel Calibrated Granular Element-Level Auditing Engine and a stealth Playwright Chromium crawler.", bold_prefix="3. False Positive Fix: ")
    add_bullet("Integrated SHAP game-theoretic explainability across all models, demystifying the black box and visually exposing deceptive tokens.", bold_prefix="4. Explainable AI: ")
    add_bullet("Delivered a comprehensive deployment suite comprising a FastAPI backend, an interactive React/Vite dashboard, and a Manifest V3 Chrome Extension.", bold_prefix="5. Full-Stack Delivery: ")

    add_heading("9.2 Future Research Directions", level=3)
    add_body("Future enhancements for DarkShield AI include:")
    add_bullet("Multimodal Vision-Language Models (VLM): Incorporating LayoutLM and CLIP architectures to jointly analyze textual semantics, bounding box coordinates, and visual color contrast ratios.", bold_prefix="1. Multimodality: ")
    add_bullet("Real-Time DOM Mutation Tracking: Utilizing MutationObserver APIs in the browser extension to intercept ephemeral popups and dynamic countdown animations.", bold_prefix="2. DOM Observers: ")
    add_bullet("Regulatory Compliance Reporting: Generating automated legal compliance audit reports formatted for submission to regulatory bodies like the FTC and CCPA.", bold_prefix="3. Legal Automation: ")

    doc.add_page_break()

    # =========================================================================
    # REFERENCES
    # =========================================================================
    add_heading("REFERENCES", level=1)
    
    refs = [
        "[1] H. Brignull, \"Dark Patterns: Deception vs. Honesty in UI Design,\" A List Apart, vol. 318, 2010.",
        "[2] A. Mathur, G. Acar, M. J. Friedman, E. Lucherini, P. Mayer, M. Chetty, and A. Narayanan, \"Dark Patterns at Scale: Findings from a Crawl of 11K Shopping Websites,\" Proceedings of the ACM on Human-Computer Interaction, vol. 3, no. CSCW, pp. 1-32, Nov. 2019.",
        "[3] C. M. Gray, Y. Kou, B. Battles, J. Hoggatt, and A. L. Toombs, \"The Dark (Patterns) Side of UX Design,\" in Proceedings of the 2018 CHI Conference on Human Factors in Computing Systems, ACM, 2018, pp. 1-14.",
        "[4] L. Di Geronimo, L. Braz, E. Fregnan, F. Palomba, and A. Bacchelli, \"UI Dark Patterns and Where to Find Them: A Study on Mobile Applications,\" in Proceedings of the 2020 CHI Conference on Human Factors in Computing Systems, ACM, 2020, pp. 1-14.",
        "[5] S. M. Lundberg and S.-I. Lee, \"A Unified Approach to Interpreting Model Predictions,\" in Advances in Neural Information Processing Systems (NeurIPS 2017), vol. 30, 2017, pp. 4765-4774.",
        "[6] S. Hochreiter and J. Schmidhuber, \"Long Short-Term Memory,\" Neural Computation, vol. 9, no. 8, pp. 1735-1780, 1997.",
        "[7] K. Cho, B. van Merrienboer, D. Bahdanau, and Y. Bengio, \"On the Properties of Neural Machine Translation: Encoder-Decoder Approaches,\" in Proceedings of SSST-8, Eighth Workshop on Syntax, Semantics and Structure in Statistical Translation, 2014, pp. 103-111.",
        "[8] T. Soe, O. Nordberg, F. C. Santos, and N. D. Bielefeld, \"Circumventing Dark Patterns with Machine Learning,\" in Extended Abstracts of the 2020 CHI Conference on Human Factors in Computing Systems, 2020, pp. 1-9.",
        "[9] S. Yada, K. Morita, and S. Hashimoto, \"Automated Detection of Manipulative Language in Commercial Web Interfaces,\" IEEE Access, vol. 10, pp. 45210-45221, 2022.",
        "[10] Federal Trade Commission (FTC), \"Bringing Dark Patterns to Light: An FTC Staff Report,\" FTC Bureau of Consumer Protection, Washington, D.C., Tech. Rep., Sep. 2022.",
        "[11] European Parliament and Council of the European Union, \"Regulation (EU) 2022/2065 on a Single Market For Digital Services (Digital Services Act),\" Official Journal of the European Union, L 277/1, Oct. 2022.",
        "[12] Central Consumer Protection Authority (CCPA), \"Guidelines for Prevention and Regulation of Dark Patterns, 2023,\" Ministry of Consumer Affairs, Government of India, Notification F. No. J-25/57/2023-CCPA, Nov. 2023.",
        "[13] Advertising Standards Council of India (ASCI), \"Guidelines for Online Deceptive Design Patterns in Advertising,\" ASCI Consumer Protection Council, Mumbai, Tech. Rep., Jun. 2023.",
        "[14] F. Pedregosa, G. Varoquaux, A. Gramfort, et al., \"Scikit-learn: Machine Learning in Python,\" Journal of Machine Learning Research, vol. 12, pp. 2825-2830, 2011.",
        "[15] A. Paszke, S. Gross, F. Massa, et al., \"PyTorch: An Imperative Style, High-Performance Deep Learning Library,\" in Advances in Neural Information Processing Systems (NeurIPS 2019), vol. 32, 2019.",
        "[16] S. Raschka, \"Model Evaluation, Model Selection, and Algorithm Selection in Machine Learning,\" arXiv preprint arXiv:1811.12808, 2018.",
        "[17] T. Fawcett, \"An Introduction to ROC Analysis,\" Pattern Recognition Letters, vol. 27, no. 8, pp. 861-874, 2006.",
        "[18] M. T. Ribeiro, S. Singh, and C. Guestrin, \"'Why Should I Trust You?': Explaining the Predictions of Any Classifier,\" in Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 2016, pp. 1135-1144.",
        "[19] Playwright Team, \"Playwright: Fast and reliable end-to-end testing for modern web apps,\" Microsoft Corporation, 2024. [Online]. Available: https://playwright.dev/.",
        "[20] S. Ramirez, \"FastAPI: Modern, Fast (High-Performance) Web Framework for Building APIs with Python,\" 2024. [Online]. Available: https://fastapi.tiangolo.com/.",
        "[21] Chrome Extensions Team, \"Manifest V3 Migration and Architectural Standards,\" Google Developers, 2024. [Online]. Available: https://developer.chrome.com/docs/extensions/develop/migrate/what-is-mv3.",
        "[22] Y. Xu, M. Li, L. Cui, S. Huang, F. Wei, and M. Zhou, \"LayoutLM: Pre-training of Text and Layout for Document Image Understanding,\" in Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, 2020, pp. 1192-1200."
    ]
    
    for r_text in refs:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(r_text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(10)
        
    doc.add_page_break()

    # =========================================================================
    # APPENDICES
    # =========================================================================
    add_heading("APPENDIX A", level=1)
    add_heading("API ENDPOINT SPECIFICATIONS", level=2)
    
    add_body("DarkShield AI backend exposes RESTful endpoints adhering to OpenAPI 3.0 standards:")
    add_body("POST /analyze/all\nContent-Type: application/json\nRequest Body: {\"text\": \"Hurry! Only 2 items remaining in stock at this price!\"}\nResponse Body (200 OK):\n{\n  \"text\": \"Hurry! Only 2 items remaining in stock at this price!\",\n  \"predictions\": {\n    \"logistic_regression\": {\"prediction\": 1, \"probability\": 0.942},\n    \"svm\": {\"prediction\": 1, \"probability\": 0.961},\n    \"lstm\": {\"prediction\": 1, \"probability\": 0.953},\n    \"gru\": {\"prediction\": 1, \"probability\": 0.958}\n  },\n  \"consensus\": {\"is_dark_pattern\": true, \"confidence\": 0.953}\n}")
    
    add_heading("APPENDIX B", level=1)
    add_heading("SOFTWARE AND HARDWARE ENVIRONMENT", level=2)
    
    add_bullet("Processor: Intel(R) Core(TM) i7 / AMD Ryzen 7 (8 Cores, 16 Threads @ 3.8 GHz)", bold_prefix="Hardware: ")
    add_bullet("System Memory (RAM): 16.0 GB DDR4 @ 3200 MHz", bold_prefix="Memory: ")
    add_bullet("Operating System: Microsoft Windows 11 Enterprise (64-bit)", bold_prefix="OS: ")
    add_bullet("Python Runtime: Python 3.10.0 (Virtual Environment)", bold_prefix="Language: ")
    add_bullet("Core Libraries: PyTorch 2.1.0, Scikit-learn 1.3.2, SHAP 0.44.0, Playwright 1.40.0, FastAPI 0.104.1, python-docx 1.2.0", bold_prefix="ML & Backend: ")
    add_bullet("Frontend Framework: Node.js v20.10.0, React 18.2.0, Vite 5.0.0, TailwindCSS 3.3.0", bold_prefix="Web Client: ")

    # Save document
    output_filename = "DarkShield_AI_Project_Report.docx"
    doc.save(output_filename)
    print(f"Master Project Report successfully generated and saved to: {output_filename}")

if __name__ == "__main__":
    build_report()
