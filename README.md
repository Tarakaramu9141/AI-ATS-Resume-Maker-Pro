# AI ATS Resume Maker Pro

AI ATS Resume Maker Pro is a Streamlit-based tool that optimizes resumes for Applicant Tracking Systems (ATS) by analyzing keyword matches and content relevance. It offers professional resume generation with customizable templates and real-time improvement suggestions.

## Features
- **ATS Resume Checker**: Evaluates resumes against job descriptions, providing ATS scores, keyword analysis, and content metrics.
- **Resume Maker**: Generates professional PDF resumes using five customizable templates (Professional, Classic, Modern, Simple, Creative).
- Supports PDF and DOCX resume uploads for analysis.
- Real-time suggestions for improving keyword usage, content, and style.
- Photo upload and default avatar support for personalized resumes.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/AI-ATS-Resume-Maker-System.git
   cd AI-ATS-Resume-Maker-System
   ```
2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Install spaCy Model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```
5. **Install wkhtmltopdf** (required for PDF generation):
   - Download and install from [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html).
   - Ensure `wkhtmltopdf` is added to your system PATH.

## Usage
1. **Run the Application**:
   ```bash
   streamlit run app.py
   ```
   Open the provided URL (e.g., `http://localhost:8501`) in your browser.

2. **ATS Resume Checker**:
   - Upload a resume (PDF or DOCX) and paste a job description.
   - Add optional skills, certifications, or requirements.
   - View ATS score, keyword analysis, content metrics, and improvement suggestions.

3. **Resume Maker**:
   - Enter personal information, work experience, education, skills, projects, certifications, and languages.
   - Choose a template (Professional, Classic, Modern, Simple, Creative).
   - Optionally upload a photo or use a default avatar.
   - Generate and download a professional PDF resume.

## Requirements
Dependencies are listed in `requirements.txt`. Key packages include:
- `streamlit`
- `pandas`
- `PyPDF2`
- `python-docx`
- `spacy`
- `scikit-learn`
- `nltk`
- `textstat`
- `numpy`
- `pdfkit`
- `jinja2`

Ensure `wkhtmltopdf` is installed for PDF generation.

## Directory Structure
```
AI-ATS-Resume-Maker-System/
├── .gitignore
├── README.md
├── requirements.txt
├── app.py
├── utils/
│   ├── ats_checker.py
│   ├── resume_generator.py
├── templates/
│   ├── classic.html
│   ├── creative.html
│   ├── modern.html
│   ├── professional.html
│   ├── simple.html
├── static/
│   ├── default_avatar.png
```

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please open an issue to discuss proposed changes or report bugs.

## License
[MIT License](LICENSE)

## Acknowledgments
- Built with [Streamlit](https://streamlit.io/) for the web interface.
- Uses [spaCy](https://spacy.io/) and [NLTK](https://www.nltk.org/) for natural language processing.
- PDF generation powered by [pdfkit](https://github.com/JazzCore/python-pdfkit) and [wkhtmltopdf](https://wkhtmltopdf.org/).

---

**Author**: [Your Name]  
**Contact**: [Your Email or GitHub Profile]  
**Date**: April 2025