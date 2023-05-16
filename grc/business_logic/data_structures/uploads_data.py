from typing import List


class EvidenceFile:
    def __init__(self):
        self.original_file_name: str = None
        self.aws_file_name: str = None
        self.password_required: bool = False


class UploadsData:
    def __init__(self):
        self.medical_reports: List[EvidenceFile] = []
        self.evidence_of_living_in_gender: List[EvidenceFile] = []
        self.name_change_documents: List[EvidenceFile] = []
        self.partnership_documents: List[EvidenceFile] = []
        self.overseas_documents: List[EvidenceFile] = []
        self.statutory_declarations: List[EvidenceFile] = []
