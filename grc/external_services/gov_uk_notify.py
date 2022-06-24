from flask import current_app
from notifications_python_client.notifications import NotificationsAPIClient
from grc.utils.config_helper import ConfigHelper


class GovUkNotify:
    def __init__(self):
        gov_uk_notify_api_key = current_app.config['NOTIFY_API']
        self.space = (ConfigHelper.get_vcap_application().space_name.lower()
                      if ConfigHelper.get_vcap_application() is not None
                      else 'local')
        self.is_production = self.space == 'production'
        self.notify_override_email = current_app.config['NOTIFY_OVERRIDE_EMAIL']
        self.gov_uk_notify_client = NotificationsAPIClient(gov_uk_notify_api_key)

    def send_email_security_code(
            self,
            email_address: str,
            security_code: str,
            security_code_timeout: str,
    ):
        personalisation = {
            'security_code': security_code,
            'security_code_timeout': security_code_timeout,
        }
        return self.send_email(
            email_address=email_address,
            template_id='d93108b9-4a5b-4268-91ee-2bb59686e702',
            personalisation=personalisation
        )

    def send_email_unfinished_application(
            self,
            email_address: str,
            expiry_days: str,
            grc_return_link: str,
    ):
        personalisation = {
            'expiry_days': expiry_days,
            'grc_return_link': grc_return_link,
        }
        return self.send_email(
            email_address=email_address,
            template_id='151fce32-1f66-4efd-a875-28026e8d8d70',
            personalisation=personalisation
        )

    def send_email_completed_application(
            self,
            email_address: str,
            documents_to_be_posted: str,
    ):
        personalisation = {
            'documents_to_be_posted': documents_to_be_posted,
        }
        return self.send_email(
            email_address=email_address,
            template_id='d3a252f7-5580-4299-8889-01ac235e8de7',
            personalisation=personalisation
        )

    def send_email_documents_you_need_for_your_grc_application(
            self,
            email_address: str,
            need_to_send_name_change_documents: bool,
            need_to_send_medical_reports: bool,
            need_to_send_evidence_of_living_in_gender: bool,
            need_to_send_statutory_declaration_for_single_applicant: bool,
            need_to_send_statutory_declaration_for_married_applicant: bool,
            need_to_send_statutory_declaration_for_applicant_in_civil_partnership: bool,
            need_to_send_spouses_statutory_declaration: bool,
            need_to_send_civil_partners_statutory_declaration: bool,
            need_to_send_marriage_certificate: bool,
            need_to_send_civil_partnership_certificate: bool,
            need_to_send_death_certificate: bool,
            need_to_send_decree_absolute: bool,
            need_to_send_proof_gender_recognised_outside_uk: bool
    ):
        personalisation = {
            'need_to_send_name_change_documents': need_to_send_name_change_documents,
            'need_to_send_medical_reports': need_to_send_medical_reports,
            'need_to_send_evidence_of_living_in_gender': need_to_send_evidence_of_living_in_gender,
            'need_to_send_statutory_declaration_for_single_applicant': need_to_send_statutory_declaration_for_single_applicant,
            'need_to_send_statutory_declaration_for_married_applicant': need_to_send_statutory_declaration_for_married_applicant,
            'need_to_send_statutory_declaration_for_applicant_in_civil_partnership': need_to_send_statutory_declaration_for_applicant_in_civil_partnership,
            'need_to_send_spouses_statutory_declaration': need_to_send_spouses_statutory_declaration,
            'need_to_send_civil_partners_statutory_declaration': need_to_send_civil_partners_statutory_declaration,
            'need_to_send_marriage_certificate': need_to_send_marriage_certificate,
            'need_to_send_civil_partnership_certificate': need_to_send_civil_partnership_certificate,
            'need_to_send_death_certificate': need_to_send_death_certificate,
            'need_to_send_decree_absolute': need_to_send_decree_absolute,
            'need_to_send_proof_gender_recognised_outside_uk': need_to_send_proof_gender_recognised_outside_uk,
        }
        return self.send_email(
            email_address=email_address,
            template_id='a992b8c5-17e6-4dca-820c-5aa4bdd67b58',
            personalisation=personalisation
        )

    def send_email_feedback(
            self,
            how_easy_to_complete_application: str,
            any_questions_difficult_to_answer: str,
            which_questions_difficult_to_answer: str,
            needed_to_call_admin_team: str,
            what_did_you_need_help_with: str,
            used_doc_checker: str,
            experience_of_using_doc_checker: str,
            any_other_suggestions: str,
    ):
        personalisation = {
            'how_easy_to_complete_application': how_easy_to_complete_application,
            'any_questions_difficult_to_answer': any_questions_difficult_to_answer,
            'which_questions_difficult_to_answer': which_questions_difficult_to_answer,
            'needed_to_call_admin_team': needed_to_call_admin_team,
            'what_did_you_need_help_with': what_did_you_need_help_with,
            'used_doc_checker': used_doc_checker,
            'experience_of_using_doc_checker': experience_of_using_doc_checker,
            'any_other_suggestions': any_other_suggestions,
        }
        return self.send_email(
            email_address='grc-service-feedback@cabinetoffice.gov.uk',
            template_id='d83e561e-3620-47f5-983a-4b50bf3fc33c',
            personalisation=personalisation
        )

    def send_email_admin_login_link(
            self,
            email_address: str,
            expires: str,
            login_link: str,
    ):
        personalisation = {
            'expires': expires,
            'login_link': login_link,
        }
        return self.send_email(
            email_address=email_address,
            template_id='ddfa69ca-e89d-49d1-8311-b487732860ec',
            personalisation=personalisation
        )

    def send_email_admin_forgot_password(
            self,
            email_address: str,
            expires: str,
            reset_link: str,
    ):
        personalisation = {
            'expires': expires,
            'reset_link': reset_link,
        }
        return self.send_email(
            email_address=email_address,
            template_id='7e2ed682-d120-4937-9154-1966976e0144',
            personalisation=personalisation
        )

    def send_email_admin_new_user(
            self,
            email_address: str,
            temporary_password: str,
            application_link: str,
    ):
        personalisation = {
            'temporary_password': temporary_password,
            'application_link': application_link,
        }
        return self.send_email(
            email_address=email_address,
            template_id='0ff48a4c-601e-4cc1-b6c6-30bac012c259',
            personalisation=personalisation
        )

    def send_email(self, email_address: str, template_id: str, personalisation: dict):
        if personalisation is None:
            personalisation = {}

        if self.is_production:
            personalisation['environment_and_email_address'] = ''
        else:
            personalisation['environment_and_email_address'] = f"[{self.space} to:{email_address}] "
            if self.notify_override_email:
                email_address = self.notify_override_email

        response = self.gov_uk_notify_client.send_email_notification(
            email_address=email_address,
            template_id=template_id,
            personalisation=personalisation
        )

        return response
