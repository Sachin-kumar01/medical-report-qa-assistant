import re


def extract_medical_values(documents):

    extracted_data = []

    patterns = {

        "Hemoglobin": r"(?i)hemoglobin\s*[:\-]?\s*(\d+(?:\.\d+)?)",

        "WBC": r"(?i)(?:wbc|white blood cell count)\s*[:\-]?\s*(\d+(?:\.\d+)?)",

        "RBC": r"(?i)(?:rbc|red blood cell count)\s*[:\-]?\s*(\d+(?:\.\d+)?)",

        "Platelets": r"(?i)platelets?\s*[:\-]?\s*(\d+(?:\.\d+)?)",

        "Glucose": r"(?i)(?:blood glucose|glucose|fasting glucose)\s*[:\-]?\s*(\d+(?:\.\d+)?)",

        "Total Cholesterol": r"(?i)total cholesterol\s*[:\-]?\s*(\d+(?:\.\d+)?)",

        "HDL": r"(?i)HDL\s*[:\-]?\s*(\d+(?:\.\d+)?)",

        "LDL": r"(?i)LDL\s*[:\-]?\s*(\d+(?:\.\d+)?)",

        "Triglycerides": r"(?i)triglycerides?\s*[:\-]?\s*(\d+(?:\.\d+)?)",

        "TSH": r"(?i)TSH\s*[:\-]?\s*(\d+(?:\.\d+)?)"
    }


    for document in documents:

        text = document.page_content

        page = document.metadata.get(
            "page",
            "Unknown"
        )

        for name, pattern in patterns.items():

            matches = re.findall(
                pattern,
                text
            )

            for value in matches:

                extracted_data.append(
                    {
                        "Test": name,
                        "Value": value,
                        "Page": page + 1
                    }
                )

    return extracted_data