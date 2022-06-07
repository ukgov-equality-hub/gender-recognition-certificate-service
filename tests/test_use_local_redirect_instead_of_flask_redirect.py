import os
import pathlib
import re


def test_gov_uk_design_system_folders_in_sync():
    """
    Previously, we used code like this...
        return redirect(url_for('task_list.index'))

    This "redirect" method generates an HTTP 302 redirect.
    As part of the redirect, it adds a "Location: XXX" header (where XXX is the URL to be redirected to).

    When this is running on a developer's laptop, all is fine :-)
    But, when this runs on Gov.UK PaaS, it breaks :-(

    But why?...

    We have a Content Security Policy which includes the line...
        form-action 'self'
    This allows <form>s to direct the user to the same SCHEMA (e.g. https://) and the same host (e.g. www.gov.uk).
    Lots of our <form>s do a POST, which generates an HTTP 302 redirect to GET the next page.

    Gov.UK PaaS terminates our HTTPS connections for us, passing on a plain HTTP connection to our app (with the same host name).
    So, the "real" URL might be https://gov.uk
    But Gov.UK PaaS terminates the HTTPS and passes on the request as if it was to http://gov.uk (Note: http, not https)

    Flask's "redirect" method, then generates an HTTP 302 redirect with a header like this:
        Location: http://gov.uk/some-other-page
    Whereas we would have expected a redirect like this:
        Location: https://gov.uk/some-other-page (Note: https)

    Google Chrome rejects this redirect as not conforming to the Content Security Policy.
    This behaviour is debated, but this is the option Google Chrome have gone for.
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/form-action

    To fix this, we can use "Location" headers which specify relative URLs, rather than absolute URLs
    e.g.:
        Location: /some-other-page
    Relative locations have been valid since 2014
    https://www.rfc-editor.org/rfc/rfc7231#section-7.1.2

    It's not easy to ask Flask to generate relative URLs, so the simples way is to create our own "local_redirect" method.
    "local_redirect" copies code from Flask's "redirect", except it allows relative Locations
    """

    all_files = get_all_python_files_in_grc_and_admin_apps()

    pattern = re.compile('\Wredirect\(')

    for full_filename in all_files:
        grc_file = open(full_filename, 'r')
        grc_file_text = grc_file.read()
        grc_file.close()

        if pattern.search(grc_file_text) != None:
            error_message = f"Found a use of 'redirect()' in file ({full_filename}). redirect() is not allowed in this codebase. Use local_redirect instead."
            raise Exception(error_message)

def get_all_python_files_in_grc_and_admin_apps():
    path_to_this_file = pathlib.Path(__file__).parent.absolute()
    path_to_grc_code = os.path.join(path_to_this_file.parent, 'grc')
    path_to_admin_code = os.path.join(path_to_this_file.parent, 'admin')

    dir_list = [path_to_grc_code, path_to_admin_code]
    files = []

    while len(dir_list) > 0:
        current_dir_path = dir_list.pop()
        with os.scandir(current_dir_path) as dir_child_items:
            for dir_child_item in dir_child_items:
                if dir_child_item.is_file():
                    files.append(dir_child_item.path)
                elif dir_child_item.is_dir():
                    dir_list.append(dir_child_item.path)

    print_now(f"Found ({len(files)}) files")
    python_files = list(filter(lambda file: file.endswith('.py'), files))
    print_now(f"Found ({len(python_files)}) python files")

    return python_files

def print_now(message):
    print(message, flush=True)
