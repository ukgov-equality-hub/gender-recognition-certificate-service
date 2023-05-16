from typing import List


class EvidenceFile:
    def __new__(cls, *args, **kwargs):
        # This method has been added to address a limitation of jsonpickle.decode
        # We use the jsonpickle library to convert these python classes to/from JSON to store in the database
        # The instance-level fields are declared in the __init__ method
        # When jsonpickle.decode re-creates a class, it calls __new__, but it does not call __init__
        # We need it to call __init__ to make sure we have set up all the instance-level fields, so we call __init__ here manually
        new_instance = super().__new__(cls)
        new_instance.__init__()
        return new_instance

    def __init__(self):
        self.original_file_name: str = None
        self.aws_file_name: str = None
        self.password_required: bool = False


class UploadsData:
    def __new__(cls, *args, **kwargs):
        # This method has been added to address a limitation of jsonpickle.decode
        # We use the jsonpickle library to convert these python classes to/from JSON to store in the database
        # The instance-level fields are declared in the __init__ method
        # When jsonpickle.decode re-creates a class, it calls __new__, but it does not call __init__
        # We need it to call __init__ to make sure we have set up all the instance-level fields, so we call __init__ here manually
        new_instance = super().__new__(cls)
        new_instance.__init__()
        return new_instance

    def __init__(self):
        self.medical_reports: List[EvidenceFile] = []
        self.evidence_of_living_in_gender: List[EvidenceFile] = []
        self.name_change_documents: List[EvidenceFile] = []
        self.partnership_documents: List[EvidenceFile] = []
        self.overseas_documents: List[EvidenceFile] = []
        self.statutory_declarations: List[EvidenceFile] = []
        self.birth_or_adoption_certificates: List[EvidenceFile] = []
