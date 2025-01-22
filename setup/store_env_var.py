import subprocess

def store_env_var(key, value):
    with open('.env', 'r') as file:
        content = file.readlines()

    env_var_found = False
    for i, line in enumerate(content):
        if line.startswith(f"{key}="):
            if line.strip() != f"{key}={value}":
                content[i] = f"{key}={value}\n"
            env_var_found = True
            break

    if not env_var_found:
        content.append(f"\n{key}={value}")

    with open('.env', 'w') as file:
        file.writelines(content)
