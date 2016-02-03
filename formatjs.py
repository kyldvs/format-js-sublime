import sublime, sublime_plugin
import subprocess

def get_setting(name):
  # WARNING: Ugly hack to workaround Sublime API limitations
  #
  # We would like to get project-specific settings first to see if the option
  # we are looking for is overriden. But the only way to do so is to call
  # `settings()` method on a *view* (tab).
  #
  # If user opens a project that contains no views, we still need somehow figure
  # out correct settings. Yes, it is ugly, but in order to do so we create
  # new empty file in active window. There is no way to close that file afterwards.
  #
  # Another gotcha: new empty view is not returned in `active_view`.
  active_window = sublime.active_window()
  if active_window:
      active_view = active_window.active_view()
      if not active_view:
          views = active_window.views()
          if views:
              active_view = views[0]
          else:
              active_view = active_window.new_file()

      proj_setting = active_view.settings().get(name)
      if proj_setting is not None:
          return proj_setting

  global_settings = sublime.load_settings('FormatJS.sublime-settings')
  return global_settings.get(name)

class formatJsCommand(sublime_plugin.TextCommand):
  def run(self, edit):

    formatJSPath = get_setting('formatjs_path')
    if not formatJSPath:
      print("formatjs_path setting is not set")
      return

    r = sublime.Region(0, self.view.size())
    
    sel = self.view.sel()
    startRegion = next(iter(sel))
    startRow, startColumn = self.view.rowcol(startRegion.begin())
    startSource = self.view.substr(r)

    input = str(startRow) + " " + str(startColumn) + "\n" + startSource

    # Run the command!
    stdin = bytes(input, "UTF-8")
    proc = subprocess.Popen(
      [formatJSPath],
      stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      shell=True)
    stdout, stderr = proc.communicate(stdin)
    output = stdout.decode("utf-8").rstrip()
    errors = stderr.decode("utf-8")

    if errors:
      print("format_js command had errors:")
      print(errors)
      return

    # Parse the output
    outputLines = output.splitlines()

    # No clue why this happens...
    if outputLines[-1] == "0 0":
      endSource = "\n".join(outputLines[1:-1]) + "\n"
    else:
      endSource = "\n".join(outputLines[1:])
    
    self.view.replace(edit, r, endSource)

    # Then update the cursor
    endCursorRaw = outputLines[0].split(" ")
    endTextPoint = self.view.text_point(
      int(endCursorRaw[0]),
      int(endCursorRaw[1]),
    )
    endRegion = sublime.Region(endTextPoint, endTextPoint)
    sel.clear()
    sel.add(endRegion)
