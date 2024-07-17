import random
from IPython.core.display import HTML

def hide_toggle(for_next=False):
    """
    Creates a toggle link to show/hide the code of the current or next cell in a Jupyter Notebook.

    Parameters:
    for_next (bool): If True, the toggle link will control the visibility of the next cell. 
                     If False, it will control the current cell. Default is False.

    Returns:
    IPython.core.display.HTML: HTML object that includes 
    the JavaScript code for toggling visibility and the toggle link.
    """
    
    # JavaScript selector for the current cell
    this_cell = """$('div.cell.code_cell.rendered.selected')"""
    
    # JavaScript selector for the next cell
    next_cell = this_cell + '.next()'
    
    # Text shown on the toggle link
    toggle_text = 'Toggle show/hide'
    
    # Determine the target cell to control with the toggle link
    target_cell = this_cell
    
    # JavaScript code to hide the current cell's input, used when toggling the next cell
    js_hide_current = ''
    
    if for_next:
        target_cell = next_cell
        toggle_text += ' next cell'
        js_hide_current = this_cell + '.find("div.input").hide();'
    
    # Generate a unique function name for the toggle action to avoid conflicts
    js_f_name = 'code_toggle_{}'.format(str(random.randint(1, 2**64)))

    # HTML template including the JavaScript function and the toggle link
    html = """
        <script>
            function {f_name}() {{
                {cell_selector}.find('div.input').toggle();
            }}
            {js_hide_current}
        </script>
        <a href="javascript:{f_name}()">{toggle_text}</a>
    """.format(
        f_name=js_f_name,
        cell_selector=target_cell,
        js_hide_current=js_hide_current,
        toggle_text=toggle_text
    )
    
    return HTML(html)
