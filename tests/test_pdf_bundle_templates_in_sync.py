import os
import pathlib


def test_pdf_bundle_templates_in_sync():
    """
    The /grc app and the /admin app both contain a template for the PDF bundle
    These two files should be kept in-sync
    """

    path_to_this_file = pathlib.Path(__file__).parent.absolute()
    path_to_grc_template = os.path.join(path_to_this_file.parent, 'grc', 'templates', 'applications', 'application.html')
    path_to_admin_template = os.path.join(path_to_this_file.parent, 'admin', 'templates', 'applications', 'application.html')

    grc_template_file = open(path_to_grc_template, 'r')
    grc_template_text = grc_template_file.read()
    grc_template_file.close()

    admin_template_file = open(path_to_admin_template, 'r')
    admin_template_text = admin_template_file.read()
    admin_template_file.close()

    print(f"Comparing GRC vs ADMIN applications/application.html")
    if grc_template_text != admin_template_text:
        error_message = f"PDF bundle templates do not match between GRC and ADMIN folders."
        raise Exception(error_message)
