import re
from typing import Dict, List, Optional, Any


class SyllabusExtractor:
    """
    Core component for extracting structured data from raw syllabus text.
    It builds the initial 'knowledge base' (kb).
    """
    def __init__(self, document_content: str):
        self.document = document_content
        # self.knowledge_base acts as the structured representation of the syllabus
        self.knowledge_base = self._process_document_to_key_value_pairs()

    def _clean_value(self, val: Optional[str]) -> str:
        if not val:
            return 'N/A'
        return re.sub(r'\s+', ' ', val).strip()

    def _extract_field_raw(self, start_tag: str, end_tag_pattern: str) -> Optional[str]:
        # [ ... original _extract_field_raw logic ... ]
        start_pattern = re.escape(start_tag) + r'\s*(.*?)'
        match = re.search(start_pattern + end_tag_pattern, self.document, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
        match_fallback = re.search(start_pattern + r'\s*$', self.document, re.DOTALL | re.IGNORECASE)
        if match_fallback:
             return match_fallback.group(1).strip()
        return None

    def _parse_course_outcomes(self, raw_outcomes: str) -> List[Dict[str, str]]:
        # [ ... original _parse_course_outcomes logic ... ]
        if not raw_outcomes:
            return []
        outcomes_list = []
        outcomes = re.split(r'[\▪\s]*CO(\d):', raw_outcomes, flags=re.IGNORECASE)
        for i in range(1, len(outcomes) - 1, 2):
            co_number = outcomes[i]
            co_text_raw = outcomes[i+1]
            desc_match = re.search(r'Description:\s*(.*?)\s*- Mapping:', co_text_raw, re.DOTALL | re.IGNORECASE)
            if desc_match:
                description = desc_match.group(1).strip()
                mapping = re.search(r'Mapping:\s*(.*)', co_text_raw, re.DOTALL | re.IGNORECASE)
                mapping_text = mapping.group(1).strip() if mapping else 'N/A'
            else:
                description = co_text_raw.strip()
                mapping_text = 'N/A'
            outcomes_list.append({
                "CO": f"CO{co_number}",
                "Description": re.sub(r'\s+', ' ', description).strip(),
                "Mapping": re.sub(r'\s+', ' ', mapping_text).strip()
            })
        return outcomes_list

    def _parse_unit_details(self, raw_units: str) -> List[Dict[str, str]]:
        # [ ... original _parse_unit_details logic ... ]
        if not raw_units:
            return []
        units_list = []
        unit_splits = re.split(r'---\s*(?:Unit |CO)?\s*([IVXLCDM\d]+)\s*\(.*?\)\s*---', raw_units, flags=re.IGNORECASE)
        unit_splits = unit_splits[1:]
        for i in range(0, len(unit_splits) - 1, 2):
            unit_num = unit_splits[i].strip()
            details_raw = unit_splits[i+1].strip()
            details = re.sub(r'^Details:\s*', '', details_raw, flags=re.IGNORECASE)
            details = re.sub(r'\s+', ' ', details).strip()
            units_list.append({
                "Unit": f"Unit {unit_num}",
                "Content": details
            })
        return units_list

    def _parse_learning_resources(self, raw_resources: str) -> Dict[str, List[str]]:
        # [ ... original _parse_learning_resources logic ... ]
        resources_dict = {'TEXT BOOKS': [], 'Reference Books': [], 'Web Resources': []}
        if not raw_resources:
            return resources_dict

        text_books_raw = re.search(r'TEXT BOOKS:\s*(.*?)\s*(Reference Books:|Web Resources:|$)', raw_resources, re.DOTALL | re.IGNORECASE)
        if text_books_raw:
            books = re.split(r'\s*[\▪\-\u2022]\s*', text_books_raw.group(1).strip())
            resources_dict['TEXT BOOKS'] = [self._clean_value(b) for b in books if b.strip()]

        ref_books_raw = re.search(r'Reference Books:\s*(.*?)\s*(Web Resources:|$)', raw_resources, re.DOTALL | re.IGNORECASE)
        if ref_books_raw:
            books = re.split(r'\s*[\▪\-\u2022]\s*', ref_books_raw.group(1).strip())
            resources_dict['Reference Books'] = [self._clean_value(b) for b in books if b.strip()]

        web_res_raw = re.search(r'Web Resources:\s*(.*)', raw_resources, re.DOTALL | re.IGNORECASE)
        if web_res_raw:
            urls = [url.strip() for url in re.split(r'\s+', web_res_raw.group(1)) if url.startswith('http')]
            resources_dict['Web Resources'] = urls

        return resources_dict

    def _extract_overall_objectives(self, unit_details: List[Dict[str, str]]) -> str:
        # [ ... original _extract_overall_objectives logic ... ]
        if not unit_details:
            return 'Overall Course Objectives not explicitly listed.'
        combined = " ".join([u['Content'] for u in unit_details])
        return combined if combined else 'Overall Course Objectives not explicitly listed.'

    def _process_document_to_key_value_pairs(self) -> Dict[str, Any]:
        # [ ... original _process_document_to_key_value_pairs logic ... ]
        kb: Dict[str, Any] = {}
        kb['Subject Name'] = self._extract_field_raw("Subject Name:", r'Course Code:') or 'N/A'
        kb['Course Code'] = self._extract_field_raw("Course Code:", r'Category:') or 'N/A'
        kb['Category'] = self._extract_field_raw("Category:", r'Credits:') or 'N/A'
        kb['Credits'] = self._clean_value(self._extract_field_raw("Credits:", r'Inst\. Hours')) or 'N/A'
        kb['Inst. Hours (LTP)'] = self._extract_field_raw("Inst. Hours", r'Marks Breakdown') or 'N/A'
        kb['CIA Marks'] = self._clean_value(self._extract_field_raw("CIA Marks:", r'External Marks:')) or 'N/A'
        kb['External Marks'] = self._clean_value(self._extract_field_raw("External Marks:", r'Total Marks:')) or 'N/A'
        kb['Total Marks'] = self._clean_value(self._extract_field_raw("Total Marks:", r'Course Outcomes')) or 'N/A'
        raw_outcomes = self._extract_field_raw("Course Outcomes", r'Unit Details')
        kb['Course Outcomes'] = self._parse_course_outcomes(raw_outcomes)
        raw_units = self._extract_field_raw("Unit Details", r'Overall Course Objectives|Evaluation and Assessment|Learning Resources')
        kb['Unit Details'] = self._parse_unit_details(raw_units)
        raw_objectives = self._extract_field_raw("Overall Course Objectives", r'Evaluation and Assessment|Learning Resources')
        kb['Overall Course Objectives'] = raw_objectives or self._extract_overall_objectives(kb['Unit Details'])
        kb['Evaluation (Internal)'] = self._extract_field_raw("Methods of Evaluation (Internal):", r'Methods of Assessment') or 'N/A'
        kb['Evaluation (External)'] = self._extract_field_raw("Methods of Assessment (External):", r'Mapping with Programme Outcomes:') or 'N/A'
        raw_resources = self._extract_field_raw("Learning Resources", r'$') or ''
        kb['Learning Resources'] = self._parse_learning_resources(raw_resources)
        return kb
