import subprocess


class WWW:
    stop_docker = False

    def __enter__(self):
        self._get_docker()
        return self

    def _get_docker(self):
        result = subprocess.run(
            ['docker-compose', 'ps'],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise Exception('Docker is not running.')

        if 'tipsy_www' not in result.stdout:
            self.stop_docker = True
            print('Starting container...')
            subprocess.run(
                ['docker-compose', 'up', '-d', 'www'],
                capture_output=True
            )

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.stop_docker:
            print('Stopping container...')
            subprocess.run(
                ['docker-compose', 'stop'],
                capture_output=True
            )
            print('Container stopped.')

    def autopep8(self):
        staged_files = self.get_staged_files()

        if not staged_files:
            print('No staged Python files found.')
            return

        for file in staged_files:
            if not file.endswith('.py') or not file.startswith('www'):
                continue

            print(f'Formatting {file} with autopep8...')
            self.autopep8_file(file)
            self.git_add_file(file)

        print('All staged files have been formatted with autopep8.')

    def get_staged_files(self):
        """Returns a list of staged files in the current git repository."""
        result = subprocess.run(
            ['git', 'diff', '--name-only', '--cached', '--diff-filter=ACM'],
            capture_output=True,
            text=True
        )

        print(result.stdout)

        if result.returncode != 0:
            raise Exception('Error while getting staged files.')

        files = result.stdout.strip().split('\n')
        # Only include Python files
        return [file for file in files if file.endswith('.py')]

    def autopep8_file(self, file_path):
        """Runs autopep8 on the given file."""
        result = subprocess.run(
            ['make', 'autopep8', f'path={file_path}'],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise Exception(f'Error while running autopep8 on {file_path}')

    def git_add_file(self, file_path):
        """Runs git add on the given file."""
        result = subprocess.run(['git', 'add', file_path])

        if result.returncode != 0:
            raise Exception(f'Error while running git add on {file_path}')


if __name__ == '__main__':
    with WWW() as www:
        www.autopep8()
