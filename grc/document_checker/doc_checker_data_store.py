import jsonpickle
from flask import session
from grc.document_checker.doc_checker_state import DocCheckerState

DOCUMENT_CHECKER_STATE_SESSION_KEY = 'documentCheckerState'


class DocCheckerDataStore:
    @staticmethod
    def load_doc_checker_state() -> DocCheckerState:
        if DOCUMENT_CHECKER_STATE_SESSION_KEY not in session:
            doc_checker_state = DocCheckerState()
            DocCheckerDataStore.save_doc_checker_state(doc_checker_state)
            return doc_checker_state

        json_text: str = session[DOCUMENT_CHECKER_STATE_SESSION_KEY]
        doc_checker_state: DocCheckerState = jsonpickle.decode(json_text)
        return doc_checker_state

    @staticmethod
    def save_doc_checker_state(doc_checker_state: DocCheckerState) -> None:
        json_text: str = jsonpickle.encode(doc_checker_state)
        session[DOCUMENT_CHECKER_STATE_SESSION_KEY] = json_text
