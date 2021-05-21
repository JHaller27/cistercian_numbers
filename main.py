import typer
from typing import Optional
from random import randint, choices


app = typer.Typer()


basic_nums = []
with open('nums.txt', 'r') as fin:
    for idx, line in enumerate(fin):
        value = idx // 3
        if len(basic_nums) <= value:
            basic_nums.append([])
        basic_nums[value].append(line.replace('\n', ''))


def auto_color(num_lines: list[str], color = typer.colors.BLUE):
    for line in num_lines:
        for ch in line:
            if ch.isspace():
                typer.echo(ch, nl=False)
            else:
                typer.secho(ch, nl=False, bg=color, fg=color)
        typer.echo()


def ones(num_lines: list[str]) -> list[str]:
    return num_lines


def tens(num_lines: list[str]) -> list[str]:
    return [rline for rline in reversed(num_lines)]


def hundreds(num_lines: list[str]) -> list[str]:
    return ["".join(reversed(line)) for line in num_lines]


def thousands(num_lines: list[str]) -> list[str]:
    return hundreds(tens(num_lines))


def i2m(num: int) -> list[str]:
    assert 0 <= num <= 9999

    digits = []
    for _ in range(4):
        num, dig = divmod(num, 10)
        digits.append(basic_nums[dig])

    ones_place = ones(digits[0])
    tens_place = tens(digits[1])
    hundreds_place = hundreds(digits[2])
    thousands_place = thousands(digits[3])

    out_lines = []
    for line_1, line_100 in zip(ones_place, hundreds_place):
        out_lines.append(f"{line_1}    {line_100}")
    out_lines.append("....................")
    for line_10, line_1000 in zip(tens_place, thousands_place):
        out_lines.append(f"{line_10}    {line_1000}")

    return out_lines


@app.command("game")
def guessing_game(
    count: int = typer.Argument(0, help="(Use 0 for infinite)"),
    color: str = typer.Option("blue", "--color", "-c"),
    level: int = typer.Option(4, "--level", "-l", min=1, max=4),
):
    def _round():
        rand_choices = [
            # weight, min, max
            (30, 0, 9),
            (40, 10, 99),
            (20, 100, 999),
            (10, 1000, 9999)
        ]
        cut_choices = rand_choices[:level]
        choice_vals, choice_wgts = [(c[1], c[2]) for c in cut_choices], [c[0] for c in cut_choices]

        min_target, max_target = choices(choice_vals, k=1, weights=choice_wgts)[0]
        target = randint(min_target, max_target)
        m_str = i2m(target)

        while True:
            typer.clear()
            auto_color(m_str, color=color.lower())

            guess = typer.prompt("What number is this? [#/q/h/t #]")

            if guess[0].lower() == "q":
                typer.echo(f"Answer: {target}")
                raise typer.Exit()

            elif guess[0].lower() == "h":
                typer.echo(f"Hint: {min_target} - {max_target}")

                continue

            elif guess[0].lower() == "t":
                parts = guess.split()
                num = [int(i) for i in parts[1:]][0]

                typer.clear()
                t_str = i2m(num)
                typer.echo(num)
                auto_color(t_str, color=color.lower())

                typer.confirm("Continue?", default=True)

                continue

            if int(guess) == target:
                typer.secho("Correct!", fg=typer.colors.GREEN)
            else:
                typer.secho("Incorrect.", fg=typer.colors.RED)
                typer.echo(f"Answer: {target}")
            typer.echo()

            return typer.confirm("Continue?", default=True)

    if count == 0:
        lcv = True
        while lcv:
            lcv = _round()

    else:
        for _ in range(count):
            if not _round():
                raise typer.Exit()


@app.command()
def convert(numbers: Optional[list[int]] = typer.Argument(None), color: str = typer.Option("blue", "--color", "-c")):
    if numbers is None:
        numbers = [typer.prompt("Number", type=int)]
    for num in numbers:
        m_str = i2m(num)
        typer.echo(num)
        auto_color(m_str, color=color.lower())


if __name__ == "__main__":
    app()
