from flask import request, url_for
from grc.business_logic.data_structures.application_data import ApplicationData
from grc.list_status import ListStatus
from grc.utils.redirect import local_redirect


def get_next_page_global(next_page_in_journey: str,
                         section_check_your_answers_page: str,
                         section_status: ListStatus,
                         application_data: ApplicationData):
    check_source = request.args.get('check_source', default=None)
    pages_from_check = request.args.get('pages_from_check', default=None, type=int)

    if check_source is None:
        next_page = next_page_in_journey
        propagate_check_source = False
    elif section_status not in [ListStatus.IN_REVIEW, ListStatus.COMPLETED]:
        next_page = next_page_in_journey
        propagate_check_source = True
    elif check_source == 'section' and section_check_your_answers_page is not None:
        next_page = section_check_your_answers_page
        propagate_check_source = False
    elif check_source == 'submit_and_pay':
        if application_data.section_status_submit_and_pay_data == ListStatus.IN_REVIEW:
            next_page = 'submitAndPay.checkYourAnswers'
        else:
            next_page = 'taskList.index'
        propagate_check_source = False
    else:
        # This shouldn't be possible
        # But, if we're not sure what's going on, just take the user to the next page in the journey
        next_page = next_page_in_journey
        propagate_check_source = False

    if check_source in ['section', 'submit_and_pay'] and propagate_check_source:
        # If we've come from a Check Your Answers page,
        #   and we're NOT going back to a Check Your Answers page
        #   (i.e. we're continuing the section journey because a follow-on question needs answering)
        #   then propagate the check_source query parameter,
        #   so that we go back to the Check Your Answers page as soon as we've finished
        #   answering the follow-on questions
        url = url_for(next_page, check_source=check_source, pages_from_check=(pages_from_check+1))
    else:
        url = url_for(next_page)

    return local_redirect(url)


def get_previous_page_global(previous_page_in_journey: str,
                         section_check_your_answers_page: str,
                         section_status: ListStatus,
                         application_data: ApplicationData):
    check_source = request.args.get('check_source', default=None)
    pages_from_check = request.args.get('pages_from_check', default=0, type=int)

    if check_source is None:
        previous_page = previous_page_in_journey
        propagate_check_source = False
    elif pages_from_check > 1:
        previous_page = previous_page_in_journey
        propagate_check_source = True
    elif pages_from_check == 1:
        if section_status not in [ListStatus.IN_REVIEW, ListStatus.COMPLETED]:
            previous_page = 'taskList.index'
            propagate_check_source = False
        elif check_source == 'section' and section_check_your_answers_page is not None:
            previous_page = section_check_your_answers_page
            propagate_check_source = False
        elif check_source == 'submit_and_pay':
            if application_data.section_status_submit_and_pay_data == ListStatus.IN_REVIEW:
                previous_page = 'submitAndPay.checkYourAnswers'
            else:
                previous_page = 'taskList.index'
            propagate_check_source = False
        else:
            # This shouldn't be possible
            # But, if we're not sure what's going on, just take the user to the previous page in the journey
            previous_page = previous_page_in_journey
            propagate_check_source = False
    else:
        # This shouldn't be possible
        # But, if we're not sure what's going on, just take the user to the previous page in the journey
        previous_page = previous_page_in_journey
        propagate_check_source = False

    if check_source in ['section', 'submit_and_pay'] and propagate_check_source:
        # If we've come from a Check Your Answers page,
        #   and we're NOT going back to a Check Your Answers page
        #   (i.e. we're continuing the section journey because a follow-on question needs answering)
        #   then propagate the check_source query parameter,
        #   so that we go back to the Check Your Answers page as soon as we've finished
        #   answering the follow-on questions
        url = url_for(previous_page, check_source=check_source, pages_from_check=(pages_from_check-1))
    else:
        url = url_for(previous_page)

    return url
