import subprocess


def apply_terraform():
    print("\nApplying terraform, this will take approximately 1 hour  🏗️")
    subprocess.run(['bash', '-c', './setup/cloud_setup.sh'])
    print('\nApplied!')
    result = subprocess.run(['bash', '-c', './setup/cloud_output.sh'],
                            capture_output=True,
                            text=True,
                            check=True)
    return result.stdout.strip().split('\n')
