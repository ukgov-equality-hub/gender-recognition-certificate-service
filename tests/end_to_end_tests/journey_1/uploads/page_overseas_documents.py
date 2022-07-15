from playwright.async_api import Page
from tests.helpers.e2e_assert_helpers import AssertHelpers
from tests.helpers.e2e_page_helpers import PageHelpers
import tests.end_to_end_tests.journey_1.data as data


TASK_LIST_BUTTON_NAME = 'Overseas certificate documents'
PAGE_URL = '/upload/overseas-certificate'
PAGE_H1 = 'Overseas gender recognition certificate documents'


async def run_checks_on_page(page: Page, asserts: AssertHelpers, helpers: PageHelpers):

    # ------------------------------------------------
    # ---- Task List page
    # ------------------------------------------------
    await asserts.url('/task-list')
    await asserts.accessibility()
    await asserts.h1('Your application')
    await asserts.number_of_errors(0)

    # Click "Overseas certificate documents" to go to the "Overseas certificate Documents" page
    await helpers.click_button(TASK_LIST_BUTTON_NAME)

    # ------------------------------------------------
    # ---- Overseas Documents page
    # ------------------------------------------------
    await asserts.url(PAGE_URL)
    await asserts.accessibility()
    await asserts.h1(PAGE_H1)
    await asserts.number_of_errors(0)

    # "Back" should take us to the Task List page
    await helpers.click_button('Back')

    # ------------------------------------------------
    # ---- Task List page
    # ------------------------------------------------
    await asserts.url('/task-list')
    await asserts.accessibility()
    await asserts.h1('Your application')
    await asserts.number_of_errors(0)

    # Continue to the "Overseas certificate Documents" page again
    await helpers.click_button(TASK_LIST_BUTTON_NAME)

    # ------------------------------------------------
    # ---- Overseas Documents page
    # ------------------------------------------------
    await asserts.url(PAGE_URL)
    await asserts.accessibility()
    await asserts.h1(PAGE_H1)
    await asserts.number_of_errors(0)
    await asserts.documents_uploaded(0)

    # Don't upload any documents, click "Save and continue"
    await helpers.click_button('Save and continue')
    await asserts.url(PAGE_URL)
    await asserts.accessibility()
    await asserts.h1(PAGE_H1)
    await asserts.number_of_errors(1)
    await asserts.error(field='documents', message='Select a JPG, BMP, PNG, TIF or PDF file smaller than 10MB')
    await asserts.documents_uploaded(0)

    # Don't upload any documents, click "Upload file"
    await helpers.click_button('Upload file')
    await asserts.url(PAGE_URL)
    await asserts.accessibility()
    await asserts.h1(PAGE_H1)
    await asserts.number_of_errors(1)
    await asserts.error(field='documents', message='Select a JPG, BMP, PNG, TIF or PDF file smaller than 10MB')
    await asserts.documents_uploaded(0)

    # Try to upload a document of the wrong type
    await helpers.upload_file_invalid_file_type(field='documents')
    await helpers.click_button('Upload file')
    await asserts.url(PAGE_URL)
    await asserts.accessibility()
    await asserts.h1(PAGE_H1)
    await asserts.number_of_errors(1)
    await asserts.error(field='documents', message='Select a JPG, BMP, PNG, TIF or PDF file smaller than 10MB')
    await asserts.documents_uploaded(0)

    # Try to upload an empty file
    await helpers.upload_file_invalid_zero_bytes(field='documents')
    await helpers.click_button('Upload file')
    await asserts.url(PAGE_URL)
    await asserts.accessibility()
    await asserts.h1(PAGE_H1)
    await asserts.number_of_errors(1)
    await asserts.error(field='documents', message='The selected file is empty. Check that the file you are uploading has the content you expect')
    await asserts.documents_uploaded(0)

    # Try to upload a document that is too large
    page.set_default_timeout(data.TIMEOUT_FOR_SLOW_OPERATIONS)  # This is a slow operation, so increase the maximum wait time
    await helpers.upload_file_invalid_too_large(field='documents')
    await helpers.click_button('Upload file')
    await asserts.url(PAGE_URL)
    page.set_default_timeout(data.DEFAULT_TIMEOUT)  # We're done with the slow part - set the timeout back to its usual value
    await asserts.accessibility()
    await asserts.h1(PAGE_H1)
    await asserts.number_of_errors(1)
    await asserts.error(field='documents', message='The selected file must be smaller than 10MB')
    await asserts.documents_uploaded(0)

    DOCUMENT_ONE_NAME = 'document_1.bmp'

    # Upload a valid document
    await helpers.upload_file_valid(field='documents', file_name=DOCUMENT_ONE_NAME)
    await helpers.click_button('Upload file')
    await asserts.url(PAGE_URL)
    await asserts.accessibility()
    await asserts.h1(PAGE_H1)
    await asserts.number_of_errors(0)
    await asserts.documents_uploaded(1)
    await asserts.document_uploaded(file_name=DOCUMENT_ONE_NAME)

    # Remove the uploaded document
    await helpers.click_button(f"Remove {DOCUMENT_ONE_NAME} file")
    await asserts.url(PAGE_URL)
    await asserts.accessibility()
    await asserts.h1(PAGE_H1)
    await asserts.number_of_errors(0)
    await asserts.documents_uploaded(0)

    # Return to Task List page
    # "Overseas certificate documents" section should be marked as "NOT STARTED"
    await helpers.click_button('Return to task list')

    # ------------------------------------------------
    # ---- Task List page
    # ------------------------------------------------
    await asserts.url('/task-list')
    await asserts.accessibility()
    await asserts.h1('Your application')
    await asserts.number_of_errors(0)

    # Status of "Overseas certificate documents" section should be "NOT STARTED"
    await asserts.task_list_sections(9)
    await asserts.task_list_section(section='Confirmation', expected_status='COMPLETED')
    await asserts.task_list_section(section='Your personal details', expected_status='COMPLETED')
    await asserts.task_list_section(section='Your birth registration information', expected_status='COMPLETED')
    await asserts.task_list_section(section='Marriage or civil partnership details', expected_status='COMPLETED')
    await asserts.task_list_section(section='Name change documents', expected_status='COMPLETED')
    await asserts.task_list_section(section='Marriage and civil partnership documents', expected_status='COMPLETED')
    await asserts.task_list_section(section='Overseas certificate documents', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Statutory declarations', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Submit and pay', expected_status='CANNOT START YET')

    # Click "Overseas certificate documents" to go back to the "Overseas certificate Documents" page
    await helpers.click_button(TASK_LIST_BUTTON_NAME)

    # ------------------------------------------------
    # ---- Overseas Documents page
    # ------------------------------------------------
    await asserts.url(PAGE_URL)
    await asserts.accessibility()
    await asserts.h1(PAGE_H1)
    await asserts.number_of_errors(0)
    await asserts.documents_uploaded(0)

    # Upload a valid document
    await helpers.upload_file_valid(field='documents', file_name=DOCUMENT_ONE_NAME)
    await helpers.click_button('Upload file')
    await asserts.url(PAGE_URL)
    await asserts.accessibility()
    await asserts.h1(PAGE_H1)
    await asserts.number_of_errors(0)
    await asserts.documents_uploaded(1)
    await asserts.document_uploaded(file_name=DOCUMENT_ONE_NAME)

    # Click "Save and continue"
    # Now that there is a file uploaded, we should be taken to the Task List page
    # "Overseas certificate documents" section should be marked as "COMPLETED"
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Task List page
    # ------------------------------------------------
    await asserts.url('/task-list')
    await asserts.accessibility()
    await asserts.h1('Your application')
    await asserts.number_of_errors(0)

    # Status of "Overseas certificate documents" section should be "COMPLETED"
    await asserts.task_list_sections(9)
    await asserts.task_list_section(section='Confirmation', expected_status='COMPLETED')
    await asserts.task_list_section(section='Your personal details', expected_status='COMPLETED')
    await asserts.task_list_section(section='Your birth registration information', expected_status='COMPLETED')
    await asserts.task_list_section(section='Marriage or civil partnership details', expected_status='COMPLETED')
    await asserts.task_list_section(section='Name change documents', expected_status='COMPLETED')
    await asserts.task_list_section(section='Marriage and civil partnership documents', expected_status='COMPLETED')
    await asserts.task_list_section(section='Overseas certificate documents', expected_status='COMPLETED')
    await asserts.task_list_section(section='Statutory declarations', expected_status='NOT STARTED')
    await asserts.task_list_section(section='Submit and pay', expected_status='CANNOT START YET')

    # Click "Overseas certificate documents" to go back to the "Overseas certificate Documents" page
    await helpers.click_button(TASK_LIST_BUTTON_NAME)

    # ------------------------------------------------
    # ---- Overseas Documents page
    # ------------------------------------------------
    await asserts.url(PAGE_URL)
    await asserts.accessibility()
    await asserts.h1(PAGE_H1)
    await asserts.number_of_errors(0)
    await asserts.documents_uploaded(1)
    await asserts.document_uploaded(file_name=DOCUMENT_ONE_NAME)

    # Click "Save and continue" without uploading a file
    # Now that there is a file uploaded, we should be taken to the Task List page
    await helpers.click_button('Save and continue')

    # ------------------------------------------------
    # ---- Task List page
    # ------------------------------------------------
    await asserts.url('/task-list')
    await asserts.accessibility()
    await asserts.h1('Your application')
    await asserts.number_of_errors(0)
