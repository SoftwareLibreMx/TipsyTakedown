import subprocess


def get_staged_files():
    """Returns a list of staged files in the current git repository."""
    result = subprocess.run(
        ['git', 'diff', '--name-only', '--cached'],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception('Error while getting staged files.')

    files = result.stdout.strip().split('\n')
    # Only include Python files
    return [file for file in files if file.endswith('.py')]


def autopep8_file(file_path):
    """Runs autopep8 on the given file."""
    result = subprocess.run(
        ['make', 'autopep8', f'path={file_path}'])

    if result.returncode != 0:
        raise Exception(f'Error while running autopep8 on {file_path}')


def git_add_file(file_path):
    """Runs git add on the given file."""
    result = subprocess.run(['git', 'add', file_path])

    if result.returncode != 0:
        raise Exception(f'Error while running git add on {file_path}')


def main():
    try:
        staged_files = get_staged_files()
        if not staged_files:
            print('No staged Python files found.')
            return

        for file in staged_files:
            if not file.endswith('.py'):
                continue

            print(f'Formatting {file} with autopep8...')
            autopep8_file(file)
            git_add_file(file)

        print('All staged files have been formatted with autopep8.')

    except Exception as e:
        print(f'An error occurred: {e}')


if __name__ == '__main__':
    main()
