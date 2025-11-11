import sublime
import sublime_plugin
import os
import fnmatch

EXCLUDED_FOLDERS = [
  'node_modules', 'build', 'dist', '.git', 'coverage', '.svelte-kit',
]

class OpenFilesMentioningCurrentCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        if not view or not view.file_name():
            sublime.status_message("No file open.")
            return

        # Extract module name (e.g., "some-module" from "some-module.js")
        filename = os.path.basename(view.file_name())
        module_name = os.path.splitext(filename)[0]

        # Get project folders
        folders = self.window.folders()
        if not folders:
            sublime.status_message("No project open.")
            return

        files_to_open = []
        for folder in folders:
            for root, dirs, filenames in os.walk(folder):
                # Prune excluded folders
                dirs[:] = [d for d in dirs if d not in EXCLUDED_FOLDERS]
                
                for fname in fnmatch.filter(filenames, "*.js"):
                    fpath = os.path.join(root, fname)
                    try:
                        with open(fpath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if module_name in content:
                                files_to_open.append(fpath)
                    except:
                        pass

        # Log full list to console
        print("Files mentioning '{}' ({} total):".format(module_name, len(files_to_open)))
        for fpath in files_to_open:
            print(fpath)

        # Open found files
        for fpath in files_to_open:
            self.window.open_file(fpath)

        sublime.status_message(f"Opened {len(files_to_open)} files mentioning '{module_name}'.")
