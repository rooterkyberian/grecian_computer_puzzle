import csv

import click

FIELDNAMES = ["x", "y", "z", "value"]


@click.command()
@click.option("-o", "--output", default="input.csv", help="Output file path")
def main(output: str) -> None:
    """Prepare a file with x, y, z, value columns."""
    n = 12
    num_discs = 4
    stacks = num_discs + 1

    rows = [
        {"x": x, "y": y, "z": z, "value": ""}
        for z in range(stacks)
        for y in range(num_discs)
        for x in range(n)
        if y >= max(z - 1, 0)
    ]

    with open(output, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    click.echo(f"Prepared {len(rows)} rows -> {output}")


if __name__ == "__main__":
    main()
