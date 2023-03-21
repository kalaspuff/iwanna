import re

from termcolor import colored


def format_response(input_: str) -> str:
    result = ""

    if "```bash" in input_ or "```sh" in input_ or "```" in input_:
        codeblocks = re.findall(r"[ ]*```(?:bash|sh|)[ ]*\n((?:(?:[^`\n]+[^\n]*)?\n)+)[ ]*```", input_)
        if codeblocks:
            for codeblock in codeblocks:
                codeblock = codeblock.strip()
                result += f"{codeblock}\n\n"

    if not result:
        result = input_.strip() + "\n\n"

    output_lines = []
    for line in result.splitlines():
        if line.startswith("QUESTION --") or line.startswith('"QUESTION --'):
            output_lines.append(colored(f"# {line}", "yellow"))
            continue

        m = re.match(r"([ ]*)([^#].+)# (.+)", line)
        if m:
            output_lines.append(f"{m.group(1)}{colored(f'# {m.group(3)}', 'grey')}")
            output_lines.append(f"{m.group(1)}{colored(m.group(2), 'cyan')}")
        else:
            if line.startswith("#"):
                output_lines.append(colored(line, "grey"))
            else:
                output_lines.append(colored(line, "cyan"))

    return "\n".join(output_lines)
