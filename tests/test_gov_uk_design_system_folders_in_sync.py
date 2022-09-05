import os
import pathlib


def test_gov_uk_design_system_folders_in_sync():
    """
    The /grc app and the /admin app both contain a templates sub-folder called /govuk-design-system-templates
    Check that these two files are in-sync
    """

    path_to_this_file = pathlib.Path(__file__).parent.absolute()
    path_to_grc_templates = os.path.join(path_to_this_file.parent, 'grc', 'templates', 'govuk-design-system-templates')
    path_to_admin_templates = os.path.join(path_to_this_file.parent, 'admin', 'templates', 'govuk-design-system-templates')
    path_to_dashboard_templates = os.path.join(path_to_this_file.parent, 'dashboard', 'templates', 'govuk-design-system-templates')

    grc_files = os.listdir(path_to_grc_templates)
    grc_files.sort()
    admin_files = os.listdir(path_to_admin_templates)
    admin_files.sort()
    dashboard_files = os.listdir(path_to_admin_templates)
    dashboard_files.sort()

    assert grc_files == admin_files
    assert grc_files == dashboard_files

    for filename in grc_files:
        grc_filename = os.path.join(path_to_grc_templates, filename)
        admin_filename = os.path.join(path_to_admin_templates, filename)
        dashboard_filename = os.path.join(path_to_dashboard_templates, filename)

        grc_file = open(grc_filename, 'r')
        grc_file_text = grc_file.read()
        grc_file.close()

        admin_file = open(admin_filename, 'r')
        admin_file_text = admin_file.read()
        admin_file.close()

        print(f"Comparing GRC vs ADMIN govuk-design-system-templates file ({filename})")
        if grc_file_text != admin_file_text:
            error_message = f"Gov.UK Design System template files do not match between GRC and ADMIN folders. Mis-matching file is ({filename})"
            raise Exception(error_message)

        dashboard_file = open(dashboard_filename, 'r')
        dashboard_file_text = dashboard_file.read()
        dashboard_file.close()

        print(f"Comparing GRC vs DASHBOARD govuk-design-system-templates file ({filename})")
        if grc_file_text != dashboard_file_text:
            error_message = f"Gov.UK Design System template files do not match between GRC and DASHBOARD folders. Mis-matching file is ({filename})"
            raise Exception(error_message)
