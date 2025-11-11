import sublime
import sublime_plugin
import os
import fnmatch

EXCLUDED_FOLDERS = ['node_modules', 'build', 'dist', '.git', 'coverage']
FILE_PATTERNS = ['*.js', '*.ts', '*.svelte']

class OpenFilesMentioningCurrentCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        if not view or not view.file_name():
            sublime.status_message("No file open.")
            return

        filename = os.path.basename(view.file_name())
        module_name = os.path.splitext(filename)[0]

        folders = self.window.folders()
        if not folders:
            sublime.status_message("No project open.")
            return

        candidate_files = []
        for folder in folders:
            for root, dirs, filenames in os.walk(folder):
                # Prune excluded folders
                dirs[:] = [d for d in dirs if not any(ex in d for ex in EXCLUDED_FOLDERS)]
                
                for pattern in FILE_PATTERNS:
                    for fname in fnmatch.filter(filenames, pattern):
                        fpath = os.path.join(root, fname)
                        candidate_files.append(fpath)

        # Debug: Log candidates
        print(f"Candidate files to search ({len(candidate_files)} total):")
        for fpath in candidate_files:
            print(fpath)

        files_to_open = []
        for fpath in candidate_files:
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if module_name in content:
                        files_to_open.append(fpath)
            except:
                pass  # Skip unreadable files

        # Debug: Log results
        print(f"\nFiles mentioning '{module_name}' ({len(files_to_open)} total):")
        for fpath in files_to_open:
            print(fpath)

        for fpath in files_to_open:
            self.window.open_file(fpath)

        sublime.status_message(f"Opened {len(files_to_open)} files mentioning '{module_name}'.")
