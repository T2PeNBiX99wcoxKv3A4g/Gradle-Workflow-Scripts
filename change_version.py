# coding: utf-8
import os
import typer
import yaml

old_config_path: str = './.github/change_version.txt'
new_config_path: str = './.github/change_version.yml'
gradle_file_path: str = './gradle.properties'
readme_file_path: str = './README.md'


def main(new_version: str):
    propertie_name: str = ''
    rename_readme: bool = False
    has_old_config: bool = False

    if os.path.isfile(new_config_path):
        with open(new_config_path, 'r+') as file:
            config = yaml.load(file, Loader=yaml.SafeLoader)
            propertie_name = config['name']
            rename_readme = config['change-readme']
            file.close()

    if os.path.isfile(old_config_path):
        with open(old_config_path, 'r+') as file:
            propertie_name = file.readline()
            rename_readme = False
            has_old_config = True
            file.close()

    if has_old_config:
        yaml_list = {
            "name": propertie_name,
            "change-readme": False
        }

        os.remove(old_config_path)

        if not os.path.exists(new_config_path):
            with open(new_config_path, 'w+') as file:
                yaml.dump(yaml_list, file)
                file.close()

    typer.echo(f"Propertie Name: {propertie_name}")

    new_version = new_version.replace('"', '')
    new_version = new_version[1:]
    old_version: str = ""

    if os.path.isfile(gradle_file_path):
        with open(gradle_file_path, 'r+') as file:
            old_text = ""

            for line in file.readlines():
                start = line.find(propertie_name)

                if start != 0:
                    old_text += line
                    continue

                old_version = line[start + (len(propertie_name) + 1):-1]
                typer.echo(f'Old version: {old_version}, New version: {new_version}')
                old_text += line
            old_keyword = f'{propertie_name}={old_version}'
            new_keyword = f'{propertie_name}={new_version}'
            new_text = old_text.replace(old_keyword, new_keyword)

            file.seek(0)
            file.truncate(0)
            file.write(new_text)
            file.close()

    if rename_readme and old_version and os.path.isfile(readme_file_path):
        with open(readme_file_path, 'r+') as file:
            old_text = ""

            for line in file.readlines():
                old_text += line

            new_text = old_text.replace(old_version, new_version)
            typer.echo(new_text)
            file.seek(0)
            file.truncate(0)
            file.write(new_text)
            file.close()


if __name__ == "__main__":
    typer.run(main)
