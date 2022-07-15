from typing import List


class EvidenceFile:
    original_file_name: str
    aws_file_name: str


class UploadsData:
    medical_reports: List[EvidenceFile] = []
    evidence_of_living_in_gender: List[EvidenceFile] = []
    name_change_documents: List[EvidenceFile] = []
    partnership_documents: List[EvidenceFile] = []
    overseas_documents: List[EvidenceFile] = []
    statutory_declarations: List[EvidenceFile] = []

    def __init__(self):
        self.medical_reports = []
        self.evidence_of_living_in_gender = []
        self.name_change_documents = []
        self.partnership_documents = []
        self.overseas_documents = []
        self.statutory_declarations = []
