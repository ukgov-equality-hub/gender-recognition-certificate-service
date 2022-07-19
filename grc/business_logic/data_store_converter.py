import datetime
from grc.business_logic.data_structures.application_data import ApplicationData
from grc.business_logic.data_structures.birth_registration_data import AdoptedInTheUkEnum
from grc.business_logic.data_structures.partnership_details_data import CurrentlyInAPartnershipEnum
from grc.business_logic.data_structures.personal_details_data import AffirmedGender
from grc.business_logic.data_structures.submit_and_pay_data import HelpWithFeesType
from grc.business_logic.data_structures.uploads_data import EvidenceFile


def convert_weakly_typed_to_strongly_typed(user_input) -> ApplicationData:
    application_data = ApplicationData()

    application_data.reference_number = user_input['reference_number']
    application_data.email_address = user_input['email']

    if 'overseasCheck' in user_input['confirmation'] and user_input['confirmation']['overseasCheck'] != 'None':
        application_data.confirmation_data.gender_recognition_outside_uk = \
            user_input['confirmation']['overseasCheck'] == 'Yes'
    if 'overseasApprovedCheck' in user_input['confirmation'] and user_input['confirmation']['overseasApprovedCheck'] != 'None':
        application_data.confirmation_data.gender_recognition_from_approved_country = \
            user_input['confirmation']['overseasApprovedCheck'] == 'Yes'
    if 'declaration' in user_input['confirmation'] and user_input['confirmation']['declaration'] != 'None':
        application_data.confirmation_data.consent_to_GRO_contact = \
            user_input['confirmation']['declaration']

    if 'title' in user_input['personalDetails']:
        application_data.personal_details_data.title = user_input['personalDetails']['title']
    if 'first_name' in user_input['personalDetails']:
        application_data.personal_details_data.first_names = user_input['personalDetails']['first_name']
    if 'last_name' in user_input['personalDetails']:
        application_data.personal_details_data.last_name = user_input['personalDetails']['last_name']

    if 'affirmed_gender' in user_input['personalDetails']:
        application_data.personal_details_data.affirmed_gender = (
            AffirmedGender.MALE if user_input['personalDetails']['affirmed_gender'] == 'MALE'
            else AffirmedGender.FEMALE
        )

    if ('transition_date_month' in user_input['personalDetails'] and
            'transition_date_year' in user_input['personalDetails']):
        application_data.personal_details_data.transition_date = datetime.date(
            int(user_input['personalDetails']['transition_date_year']),
            int(user_input['personalDetails']['transition_date_month']),
            1
        )

    if ('statutory_declaration_date_day' in user_input['personalDetails'] and
            'statutory_declaration_date_month' in user_input['personalDetails'] and
            'statutory_declaration_date_year' in user_input['personalDetails']):
        application_data.personal_details_data.statutory_declaration_date = datetime.date(
            int(user_input['personalDetails']['statutory_declaration_date_year']),
            int(user_input['personalDetails']['statutory_declaration_date_month']),
            int(user_input['personalDetails']['statutory_declaration_date_day'])
        )

    if 'previousNamesCheck' in user_input['personalDetails']:
        application_data.personal_details_data.changed_name_to_reflect_gender = \
            user_input['personalDetails']['previousNamesCheck'] == 'Yes'

    if 'address' in user_input['personalDetails']:
        if 'address_line_one' in user_input['personalDetails']['address']:
            application_data.personal_details_data.address_line_one = \
                user_input['personalDetails']['address']['address_line_one']
        if 'address_line_two' in user_input['personalDetails']['address']:
            application_data.personal_details_data.address_line_two = \
                user_input['personalDetails']['address']['address_line_two']
        if 'town' in user_input['personalDetails']['address']:
            application_data.personal_details_data.address_town_city = \
                user_input['personalDetails']['address']['town']
        if 'country' in user_input['personalDetails']['address']:
            application_data.personal_details_data.address_country = \
                user_input['personalDetails']['address']['country']
        if 'postcode' in user_input['personalDetails']['address']:
            application_data.personal_details_data.address_postcode = \
                user_input['personalDetails']['address']['postcode']

    if 'contactPreferences' in user_input['personalDetails']:
        if 'email' in user_input['personalDetails']['contactPreferences']:
            application_data.personal_details_data.contact_email_address = \
                user_input['personalDetails']['contactPreferences']['email']
        if 'phone' in user_input['personalDetails']['contactPreferences']:
            application_data.personal_details_data.contact_phone_number = \
                user_input['personalDetails']['contactPreferences']['phone']
        if 'post' in user_input['personalDetails']['contactPreferences']:
            application_data.personal_details_data.contact_by_post = \
                len(user_input['personalDetails']['contactPreferences']['post']) > 0

    if 'contactDates' in user_input['personalDetails']:
        if 'answer' in user_input['personalDetails']['contactDates']:
            application_data.personal_details_data.contact_dates_should_avoid = \
                user_input['personalDetails']['contactDates']['answer'] == 'Yes'
        if 'dates' in user_input['personalDetails']['contactDates']:
            application_data.personal_details_data.contact_dates_to_avoid = \
                user_input['personalDetails']['contactDates']['dates']

    if 'hmrc' in user_input['personalDetails']:
        if 'answer' in user_input['personalDetails']['hmrc']:
            application_data.personal_details_data.tell_hmrc = \
                user_input['personalDetails']['hmrc']['answer'] == 'Yes'
        if 'national_insurance_number' in user_input['personalDetails']['hmrc']:
            application_data.personal_details_data.national_insurance_number = \
                user_input['personalDetails']['hmrc']['national_insurance_number']

    if 'first_name' in user_input['birthRegistration']:
        application_data.birth_registration_data.first_name = \
            user_input['birthRegistration']['first_name']
    if 'middle_names' in user_input['birthRegistration']:
        application_data.birth_registration_data.middle_names = \
            user_input['birthRegistration']['middle_names']
    if 'last_name' in user_input['birthRegistration']:
        application_data.birth_registration_data.last_name = \
            user_input['birthRegistration']['last_name']

    if 'dob' in user_input['birthRegistration']:
        if ('day' in user_input['birthRegistration']['dob'] and
            'month' in user_input['birthRegistration']['dob'] and
            'year' in user_input['birthRegistration']['dob']):
            application_data.birth_registration_data.date_of_birth = datetime.date(
                int(user_input['birthRegistration']['dob']['year']),
                int(user_input['birthRegistration']['dob']['month']),
                int(user_input['birthRegistration']['dob']['day'])
            )

    if 'ukCheck' in user_input['birthRegistration']:
        application_data.birth_registration_data.birth_registered_in_uk = \
            user_input['birthRegistration']['ukCheck'] == 'Yes'

    if 'country' in user_input['birthRegistration']:
        application_data.birth_registration_data.country_of_birth = \
            user_input['birthRegistration']['country']

    if 'place_of_birth' in user_input['birthRegistration']:
        application_data.birth_registration_data.town_city_of_birth = \
            user_input['birthRegistration']['place_of_birth']

    if 'mothers_first_name' in user_input['birthRegistration']:
        application_data.birth_registration_data.mothers_first_name = \
            user_input['birthRegistration']['mothers_first_name']
    if 'mothers_last_name' in user_input['birthRegistration']:
        application_data.birth_registration_data.mothers_last_name = \
            user_input['birthRegistration']['mothers_last_name']
    if 'mothers_maiden_name' in user_input['birthRegistration']:
        application_data.birth_registration_data.mothers_maiden_name = \
            user_input['birthRegistration']['mothers_maiden_name']

    if 'fathersNameCheck' in user_input['birthRegistration']:
        application_data.birth_registration_data.fathers_name_on_birth_certificate = \
            user_input['birthRegistration']['fathersNameCheck'] == 'Yes'

    if 'fathers_first_name' in user_input['birthRegistration']:
        application_data.birth_registration_data.fathers_first_name = \
            user_input['birthRegistration']['fathers_first_name']
    if 'fathers_last_name' in user_input['birthRegistration']:
        application_data.birth_registration_data.fathers_last_name = \
            user_input['birthRegistration']['fathers_last_name']

    if 'adopted' in user_input['birthRegistration']:
        application_data.birth_registration_data.adopted = \
            user_input['birthRegistration']['adopted'] == 'Yes'

    if 'adopted_uk' in user_input['birthRegistration']:
        if user_input['birthRegistration']['adopted_uk'] == 'Yes':
            application_data.birth_registration_data.adopted_in_the_uk = AdoptedInTheUkEnum.ADOPTED_IN_THE_UK_YES
        if user_input['birthRegistration']['adopted_uk'] == 'No':
            application_data.birth_registration_data.adopted_in_the_uk = AdoptedInTheUkEnum.ADOPTED_IN_THE_UK_NO
        if user_input['birthRegistration']['adopted_uk'] == 'DO_NOT_KNOW':
            application_data.birth_registration_data.adopted_in_the_uk = AdoptedInTheUkEnum.ADOPTED_IN_THE_UK_DO_NOT_KNOW

    if 'forces' in user_input['birthRegistration']:
        application_data.birth_registration_data.forces_registration = \
            user_input['birthRegistration']['forces'] == 'Yes'

    if 'marriageCivilPartnership' in user_input['partnershipDetails']:
        if user_input['partnershipDetails']['marriageCivilPartnership'] == 'Married':
            application_data.partnership_details_data.currently_in_a_partnership = CurrentlyInAPartnershipEnum.MARRIED
        if user_input['partnershipDetails']['marriageCivilPartnership'] == 'Civil partnership':
            application_data.partnership_details_data.currently_in_a_partnership = CurrentlyInAPartnershipEnum.CIVIL_PARTNERSHIP
        if user_input['partnershipDetails']['marriageCivilPartnership'] == 'Neither':
            application_data.partnership_details_data.currently_in_a_partnership = CurrentlyInAPartnershipEnum.NEITHER

    if 'stayTogether' in user_input['partnershipDetails']:
        application_data.partnership_details_data.plan_to_remain_in_a_partnership = \
            user_input['partnershipDetails']['stayTogether'] == 'Yes'

    if 'partnerAgrees' in user_input['partnershipDetails']:
        application_data.partnership_details_data.partner_agrees = \
            user_input['partnershipDetails']['partnerAgrees'] == 'Yes'

    if 'interimCheck' in user_input['partnershipDetails']:
        application_data.partnership_details_data.confirm_understood_interim_certificate = \
            user_input['partnershipDetails']['interimCheck'] == 'Yes'

    if 'partnerDied' in user_input['partnershipDetails']:
        application_data.partnership_details_data.previous_partnership_partner_died = \
            user_input['partnershipDetails']['partnerDied'] == 'Yes'

    if 'endedCheck' in user_input['partnershipDetails']:
        application_data.partnership_details_data.previous_partnership_ended = \
            user_input['partnershipDetails']['endedCheck'] == 'Yes'

    if 'files' in user_input['medicalReports'] and user_input['medicalReports']['files'] is not None:
        for aws_file_name in user_input['medicalReports']['files']:
            evidence_file = EvidenceFile()
            evidence_file.aws_file_name = aws_file_name
            evidence_file.original_file_name = aws_file_name.replace(application_data.reference_number + '__medicalReports__', '')
            application_data.uploads_data.medical_reports.append(evidence_file)

    if 'files' in user_input['genderEvidence'] and user_input['genderEvidence']['files'] is not None:
        for aws_file_name in user_input['genderEvidence']['files']:
            evidence_file = EvidenceFile()
            evidence_file.aws_file_name = aws_file_name
            evidence_file.original_file_name = aws_file_name.replace(application_data.reference_number + '__genderEvidence__', '')
            application_data.uploads_data.evidence_of_living_in_gender.append(evidence_file)

    if 'files' in user_input['nameChange'] and user_input['nameChange']['files'] is not None:
        for aws_file_name in user_input['nameChange']['files']:
            evidence_file = EvidenceFile()
            evidence_file.aws_file_name = aws_file_name
            evidence_file.original_file_name = aws_file_name.replace(application_data.reference_number + '__nameChange__', '')
            application_data.uploads_data.name_change_documents.append(evidence_file)

    if 'files' in user_input['marriageDocuments'] and user_input['marriageDocuments']['files'] is not None:
        for aws_file_name in user_input['marriageDocuments']['files']:
            evidence_file = EvidenceFile()
            evidence_file.aws_file_name = aws_file_name
            evidence_file.original_file_name = aws_file_name.replace(application_data.reference_number + '__marriageDocuments__', '')
            application_data.uploads_data.partnership_documents.append(evidence_file)

    if 'files' in user_input['overseasCertificate'] and user_input['overseasCertificate']['files'] is not None:
        for aws_file_name in user_input['overseasCertificate']['files']:
            evidence_file = EvidenceFile()
            evidence_file.aws_file_name = aws_file_name
            evidence_file.original_file_name = aws_file_name.replace(application_data.reference_number + '__overseasCertificate__', '')
            application_data.uploads_data.overseas_documents.append(evidence_file)

    if 'files' in user_input['statutoryDeclarations'] and user_input['statutoryDeclarations']['files'] is not None:
        for aws_file_name in user_input['statutoryDeclarations']['files']:
            evidence_file = EvidenceFile()
            evidence_file.aws_file_name = aws_file_name
            evidence_file.original_file_name = aws_file_name.replace(application_data.reference_number + '__statutoryDeclarations__', '')
            application_data.uploads_data.statutory_declarations.append(evidence_file)

    if 'method' in user_input['submitAndPay']:
        application_data.submit_and_pay_data.applying_for_help_with_fee = \
            user_input['submitAndPay']['method'] == 'Help'

    if 'helpType' in user_input['submitAndPay']:
        if user_input['submitAndPay']['helpType'] == 'Using the online service':
            application_data.submit_and_pay_data.how_applying_for_help_with_fees = HelpWithFeesType.USING_ONLINE_SERVICE
        if user_input['submitAndPay']['helpType'] == 'Using the EX160 form':
            application_data.submit_and_pay_data.how_applying_for_help_with_fees = HelpWithFeesType.USING_EX160_FORM

    if 'referenceNumber' in user_input['submitAndPay']:
        application_data.submit_and_pay_data.help_with_fees_reference_number = \
            user_input['submitAndPay']['referenceNumber']

    if 'declaration' in user_input['submitAndPay']:
        application_data.submit_and_pay_data.declaration = \
            user_input['submitAndPay']['declaration']

    if 'payment_id' in user_input['submitAndPay']:
        application_data.submit_and_pay_data.gov_pay_payment_id = \
            user_input['submitAndPay']['payment_id']

    if 'uuid' in user_input['submitAndPay']:
        application_data.submit_and_pay_data.gov_pay_uuid = \
            user_input['submitAndPay']['uuid']

    if 'paymentDetails' in user_input['submitAndPay']:
        application_data.submit_and_pay_data.gov_pay_payment_details = \
            user_input['submitAndPay']['paymentDetails']

    if 'is_submitted' in user_input['submitAndPay']:
        application_data.submit_and_pay_data.is_submitted = \
            user_input['submitAndPay']['is_submitted']

    return application_data


def convert_strongly_typed_to_weakly_typed(application_data: ApplicationData):
    user_input = {}

    user_input['reference_number'] = application_data.reference_number
    user_input['email'] = application_data.email_address

    user_input['confirmation'] = {}

    if application_data.confirmation_data.gender_recognition_outside_uk is None:
        user_input['confirmation']['overseasCheck'] = 'None'
    else:
        user_input['confirmation']['overseasCheck'] = (
            'Yes' if application_data.confirmation_data.gender_recognition_outside_uk
            else 'No'
        )

    if application_data.confirmation_data.gender_recognition_from_approved_country is None:
        user_input['confirmation']['overseasApprovedCheck'] = 'None'
    else:
        user_input['confirmation']['overseasApprovedCheck'] = (
            'Yes' if application_data.confirmation_data.gender_recognition_from_approved_country
            else 'No'
        )

    if application_data.confirmation_data.consent_to_GRO_contact is None:
        user_input['confirmation']['declaration'] = 'None'
    else:
        user_input['confirmation']['declaration'] = application_data.confirmation_data.consent_to_GRO_contact

    user_input['confirmation']['progress'] = application_data.confirmation_data.section_status.name

    user_input['personalDetails'] = {}

    if application_data.personal_details_data.title is not None:
        user_input['personalDetails']['title'] = application_data.personal_details_data.title
    if application_data.personal_details_data.first_names is not None:
        user_input['personalDetails']['first_name'] = application_data.personal_details_data.first_names
    if application_data.personal_details_data.last_name is not None:
        user_input['personalDetails']['last_name'] = application_data.personal_details_data.last_name

    if application_data.personal_details_data.affirmed_gender is not None:
        user_input['personalDetails']['affirmed_gender'] = (
            'MALE' if application_data.personal_details_data.affirmed_gender == AffirmedGender.MALE
            else 'FEMALE'
        )

    if application_data.personal_details_data.transition_date is not None:
        user_input['personalDetails']['transition_date_year'] = \
            application_data.personal_details_data.transition_date.year
        user_input['personalDetails']['transition_date_month'] = \
            application_data.personal_details_data.transition_date.month

    if application_data.personal_details_data.statutory_declaration_date is not None:
        user_input['personalDetails']['statutory_declaration_date_year'] = \
            application_data.personal_details_data.statutory_declaration_date.year
        user_input['personalDetails']['statutory_declaration_date_month'] = \
            application_data.personal_details_data.statutory_declaration_date.month
        user_input['personalDetails']['statutory_declaration_date_day'] = \
            application_data.personal_details_data.statutory_declaration_date.day

    if application_data.personal_details_data.changed_name_to_reflect_gender is not None:
        user_input['personalDetails']['previousNamesCheck'] = (
            'Yes' if application_data.personal_details_data.changed_name_to_reflect_gender
            else 'No'
        )

    if (application_data.personal_details_data.address_line_one is not None or
        application_data.personal_details_data.address_line_two is not None or
        application_data.personal_details_data.address_town_city is not None or
        application_data.personal_details_data.address_country is not None or
        application_data.personal_details_data.address_postcode is not None):
        user_input['personalDetails']['address'] = {}
        user_input['personalDetails']['address']['address_line_one'] = \
            application_data.personal_details_data.address_line_one
        user_input['personalDetails']['address']['address_line_two'] = \
            application_data.personal_details_data.address_line_two
        user_input['personalDetails']['address']['town'] = \
            application_data.personal_details_data.address_town_city
        user_input['personalDetails']['address']['country'] = \
            application_data.personal_details_data.address_country
        user_input['personalDetails']['address']['postcode'] = \
            application_data.personal_details_data.address_postcode

    if (application_data.personal_details_data.contact_email_address is not None or
        application_data.personal_details_data.contact_phone_number is not None or
        application_data.personal_details_data.contact_by_post is not None):
        user_input['personalDetails']['contactPreferences'] = {}
        user_input['personalDetails']['contactPreferences']['email'] = \
            application_data.personal_details_data.contact_email_address
        user_input['personalDetails']['contactPreferences']['phone'] = \
            application_data.personal_details_data.contact_phone_number
        if application_data.personal_details_data.contact_by_post:
            user_input['personalDetails']['contactPreferences']['post'] = (
                    application_data.personal_details_data.address_line_one + ', ' +
                    (application_data.personal_details_data.address_line_two + ', ' if application_data.personal_details_data.address_line_two else '') +
                    application_data.personal_details_data.address_town_city + ', ' +
                    (application_data.personal_details_data.address_country + ', ' if application_data.personal_details_data.address_country else '') +
                    application_data.personal_details_data.address_postcode
                ).replace(', , ', ', ')

    if application_data.personal_details_data.contact_dates_should_avoid is not None:
        user_input['personalDetails']['contactDates'] = {}
        user_input['personalDetails']['contactDates']['answer'] = (
            'Yes' if application_data.personal_details_data.contact_dates_should_avoid
            else 'No'
        )
        user_input['personalDetails']['contactDates']['dates'] = \
            application_data.personal_details_data.contact_dates_to_avoid

    if application_data.personal_details_data.tell_hmrc is not None:
        user_input['personalDetails']['hmrc'] = {}
        user_input['personalDetails']['hmrc']['answer'] = (
            'Yes' if application_data.personal_details_data.tell_hmrc
            else 'No'
        )
        user_input['personalDetails']['hmrc']['national_insurance_number'] = \
            application_data.personal_details_data.national_insurance_number

    user_input['personalDetails']['progress'] = application_data.personal_details_data.section_status.name

    user_input['birthRegistration'] = {}

    if application_data.birth_registration_data.first_name is not None:
        user_input['birthRegistration']['first_name'] = application_data.birth_registration_data.first_name
    if application_data.birth_registration_data.middle_names is not None:
        user_input['birthRegistration']['middle_names'] = application_data.birth_registration_data.middle_names
    if application_data.birth_registration_data.last_name is not None:
        user_input['birthRegistration']['last_name'] = application_data.birth_registration_data.last_name

    if application_data.birth_registration_data.date_of_birth is not None:
        user_input['birthRegistration']['dob'] = {}
        user_input['birthRegistration']['dob']['year'] = application_data.birth_registration_data.date_of_birth.year
        user_input['birthRegistration']['dob']['month'] = application_data.birth_registration_data.date_of_birth.month
        user_input['birthRegistration']['dob']['day'] = application_data.birth_registration_data.date_of_birth.day

    if application_data.birth_registration_data.birth_registered_in_uk is not None:
        user_input['birthRegistration']['ukCheck'] = (
            'Yes' if application_data.birth_registration_data.birth_registered_in_uk
            else 'No'
        )

    if application_data.birth_registration_data.country_of_birth is not None:
        user_input['birthRegistration']['country'] = application_data.birth_registration_data.country_of_birth
    if application_data.birth_registration_data.town_city_of_birth is not None:
        user_input['birthRegistration']['place_of_birth'] = application_data.birth_registration_data.town_city_of_birth

    if application_data.birth_registration_data.mothers_first_name is not None:
        user_input['birthRegistration']['mothers_first_name'] = application_data.birth_registration_data.mothers_first_name
    if application_data.birth_registration_data.mothers_last_name is not None:
        user_input['birthRegistration']['mothers_last_name'] = application_data.birth_registration_data.mothers_last_name
    if application_data.birth_registration_data.mothers_maiden_name is not None:
        user_input['birthRegistration']['mothers_maiden_name'] = application_data.birth_registration_data.mothers_maiden_name

    if application_data.birth_registration_data.fathers_name_on_birth_certificate is not None:
        user_input['birthRegistration']['fathersNameCheck'] = (
            'Yes' if application_data.birth_registration_data.fathers_name_on_birth_certificate
            else 'No'
        )

    if application_data.birth_registration_data.fathers_first_name is not None:
        user_input['birthRegistration']['fathers_first_name'] = application_data.birth_registration_data.fathers_first_name
    if application_data.birth_registration_data.fathers_last_name is not None:
        user_input['birthRegistration']['fathers_last_name'] = application_data.birth_registration_data.fathers_last_name

    if application_data.birth_registration_data.adopted is not None:
        user_input['birthRegistration']['adopted'] = (
            'Yes' if application_data.birth_registration_data.adopted
            else 'No'
        )

    if application_data.birth_registration_data.adopted_in_the_uk == AdoptedInTheUkEnum.ADOPTED_IN_THE_UK_YES:
        user_input['birthRegistration']['adopted_uk'] = 'Yes'
    if application_data.birth_registration_data.adopted_in_the_uk == AdoptedInTheUkEnum.ADOPTED_IN_THE_UK_NO:
        user_input['birthRegistration']['adopted_uk'] = 'No'
    if application_data.birth_registration_data.adopted_in_the_uk == AdoptedInTheUkEnum.ADOPTED_IN_THE_UK_DO_NOT_KNOW:
        user_input['birthRegistration']['adopted_uk'] = 'DO_NOT_KNOW'

    if application_data.birth_registration_data.forces_registration is not None:
        user_input['birthRegistration']['forces'] = (
            'Yes' if application_data.birth_registration_data.forces_registration
            else 'No'
        )

    user_input['birthRegistration']['progress'] = application_data.birth_registration_data.section_status.name

    user_input['partnershipDetails'] = {}

    if application_data.partnership_details_data.currently_in_a_partnership == CurrentlyInAPartnershipEnum.MARRIED:
        user_input['partnershipDetails']['marriageCivilPartnership'] = 'Married'
    if application_data.partnership_details_data.currently_in_a_partnership == CurrentlyInAPartnershipEnum.CIVIL_PARTNERSHIP:
        user_input['partnershipDetails']['marriageCivilPartnership'] = 'Civil partnership'
    if application_data.partnership_details_data.currently_in_a_partnership == CurrentlyInAPartnershipEnum.NEITHER:
        user_input['partnershipDetails']['marriageCivilPartnership'] = 'Neither'

    if application_data.partnership_details_data.plan_to_remain_in_a_partnership is not None:
        user_input['partnershipDetails']['stayTogether'] = (
            'Yes' if application_data.partnership_details_data.plan_to_remain_in_a_partnership
            else 'No'
        )

    if application_data.partnership_details_data.partner_agrees is not None:
        user_input['partnershipDetails']['partnerAgrees'] = (
            'Yes' if application_data.partnership_details_data.partner_agrees
            else 'No'
        )

    if application_data.partnership_details_data.confirm_understood_interim_certificate is not None:
        user_input['partnershipDetails']['interimCheck'] = (
            'Yes' if application_data.partnership_details_data.confirm_understood_interim_certificate
            else 'No'
        )

    if application_data.partnership_details_data.previous_partnership_partner_died is not None:
        user_input['partnershipDetails']['partnerDied'] = (
            'Yes' if application_data.partnership_details_data.previous_partnership_partner_died
            else 'No'
        )

    if application_data.partnership_details_data.previous_partnership_ended is not None:
        user_input['partnershipDetails']['endedCheck'] = (
            'Yes' if application_data.partnership_details_data.previous_partnership_ended
            else 'No'
        )

    user_input['partnershipDetails']['progress'] = application_data.partnership_details_data.section_status.name

    user_input['medicalReports'] = {'files': []}
    for evidence_file in application_data.uploads_data.medical_reports:
        user_input['medicalReports']['files'].append(evidence_file.aws_file_name)
    user_input['medicalReports']['progress'] = application_data.section_status_medical_reports.name

    user_input['genderEvidence'] = {'files': []}
    for evidence_file in application_data.uploads_data.evidence_of_living_in_gender:
        user_input['genderEvidence']['files'].append(evidence_file.aws_file_name)
    user_input['genderEvidence']['progress'] = application_data.section_status_evidence_of_living_in_gender.name

    user_input['nameChange'] = {'files': []}
    for evidence_file in application_data.uploads_data.name_change_documents:
        user_input['nameChange']['files'].append(evidence_file.aws_file_name)
    user_input['nameChange']['progress'] = application_data.section_status_name_change_documents.name

    user_input['marriageDocuments'] = {'files': []}
    for evidence_file in application_data.uploads_data.partnership_documents:
        user_input['marriageDocuments']['files'].append(evidence_file.aws_file_name)
    user_input['marriageDocuments']['progress'] = application_data.section_status_partnership_documents.name

    user_input['overseasCertificate'] = {'files': []}
    for evidence_file in application_data.uploads_data.overseas_documents:
        user_input['overseasCertificate']['files'].append(evidence_file.aws_file_name)
    user_input['overseasCertificate']['progress'] = application_data.section_status_overseas_documents.name

    user_input['statutoryDeclarations'] = {'files': []}
    for evidence_file in application_data.uploads_data.statutory_declarations:
        user_input['statutoryDeclarations']['files'].append(evidence_file.aws_file_name)
    user_input['statutoryDeclarations']['progress'] = application_data.section_status_statutory_declarations.name

    user_input['submitAndPay'] = {}

    if application_data.submit_and_pay_data.applying_for_help_with_fee is not None:
        user_input['submitAndPay']['method'] = (
            'Help' if application_data.submit_and_pay_data.applying_for_help_with_fee
            else 'Online'
        )

    if application_data.submit_and_pay_data.how_applying_for_help_with_fees == HelpWithFeesType.USING_ONLINE_SERVICE:
        user_input['submitAndPay']['helpType'] = 'Using the online service'
    if application_data.submit_and_pay_data.how_applying_for_help_with_fees == HelpWithFeesType.USING_EX160_FORM:
        user_input['submitAndPay']['helpType'] = 'Using the EX160 form'

    if application_data.submit_and_pay_data.help_with_fees_reference_number is not None:
        user_input['submitAndPay']['referenceNumber'] = application_data.submit_and_pay_data.help_with_fees_reference_number

    if application_data.submit_and_pay_data.declaration is not None:
        user_input['submitAndPay']['declaration'] = application_data.submit_and_pay_data.declaration

    if application_data.submit_and_pay_data.gov_pay_payment_id is not None:
        user_input['submitAndPay']['payment_id'] = application_data.submit_and_pay_data.gov_pay_payment_id

    if application_data.submit_and_pay_data.gov_pay_uuid is not None:
        user_input['submitAndPay']['uuid'] = application_data.submit_and_pay_data.gov_pay_uuid

    if application_data.submit_and_pay_data.gov_pay_payment_details is not None:
        user_input['submitAndPay']['paymentDetails'] = application_data.submit_and_pay_data.gov_pay_payment_details

    if application_data.submit_and_pay_data.is_submitted is not None:
        user_input['submitAndPay']['is_submitted'] = application_data.submit_and_pay_data.is_submitted

    user_input['submitAndPay']['progress'] = application_data.section_status_submit_and_pay_data.name

    return user_input
