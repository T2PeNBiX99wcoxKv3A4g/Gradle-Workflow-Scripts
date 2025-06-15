# coding: utf-8

import typer


def main(new_version: str):
    typer.echo(f"New version: {new_version}")

    propertie_name = ''

    with open('./.github/change_version.txt', 'r+') as file:
        propertie_name = file.readline()
        file.close()

    typer.echo(f"Propertie Name: {propertie_name}")

    with open('./gradle.properties', 'r+') as file:
        old_text = ""
        new_version = new_version.replace('"', '')
        new_version = new_version[1:]
        old_version: str = ""

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


if __name__ == "__main__":
    typer.run(main)
