import dataclasses
import itertools
from collections.abc import Iterator

import click
import pandas as pd
import numpy as np
from rich.console import Console

console = Console()


@dataclasses.dataclass(frozen=True)
class GrecianComputer:
    discs: list[np.ndarray]
    n_cols: int
    n_rows: int


def load_discs(filepath: str) -> GrecianComputer:
    df = pd.read_csv(filepath)
    df["value"] = df["value"].replace("n", np.nan).astype(float)

    max_x = df["x"].max() + 1
    max_y = df["y"].max() + 1
    disc_indices = sorted(df["z"].unique())

    discs = []
    for z in disc_indices:
        disc_df = df[df["z"] == z]
        matrix = np.full((max_y, max_x), np.nan)
        for _, row in disc_df.iterrows():
            matrix[int(row["y"]), int(row["x"])] = row["value"]
        discs.append(matrix)

    return GrecianComputer(
        discs=discs,
        n_cols=max_x,
        n_rows=max_y,
    )


def rotate_disc(disc: np.ndarray, x_adjustment: int) -> np.ndarray:
    return np.roll(disc, x_adjustment, axis=1)


def overlay_discs(discs: list[np.ndarray]) -> np.ndarray:
    result = discs[0].copy()
    for disc in discs[1:]:
        mask = ~np.isnan(disc)
        result[mask] = disc[mask]
    return result


def check_solution(overlaid: np.ndarray, target: int = 42) -> bool:
    column_sums = np.nansum(overlaid, axis=0)
    return np.allclose(column_sums, target)


def rotate_and_overlay(discs: list[np.ndarray], adjustments: list[int]) -> np.ndarray:
    rotated = [rotate_disc(d, adj) for d, adj in zip(discs, adjustments)]
    return overlay_discs(rotated)


def solve(discs: list[np.ndarray], target: int = 42) -> Iterator[list[int]]:
    n_cols = discs[0].shape[1]
    for combo in itertools.product(range(n_cols), repeat=len(discs) - 1):
        adjustments = [0] + list(combo)
        adjusted = rotate_and_overlay(discs, adjustments)
        if check_solution(adjusted, target):
            yield adjustments


@click.command()
@click.argument("input_file", default="input_my.csv", type=click.Path(exists=True))
def main(input_file: str):
    gc_puzzle = load_discs(input_file)
    discs = gc_puzzle.discs

    console.print(f"Loaded [cyan]{len(discs)}[/cyan] discs:")
    for i, disc in enumerate(discs):
        console.print()
        console.print(f"[bold blue]Disc {i}:[/bold blue]")
        df = pd.DataFrame(disc)
        df = df.dropna(how="all")
        df = df.fillna("n")
        console.print(df.to_string(index=False, header=False))

    possible_combinations = gc_puzzle.n_cols ** (len(discs) - 1)
    console.print(f"Possible combinations: [cyan]{possible_combinations}[/cyan]")

    console.print()
    console.print("[yellow]Searching for solutions...[/yellow]")

    count = 0
    for solution in solve(discs):
        count += 1
        console.print()
        console.print(f"[bold green]Solution {count}:[/bold green]")
        for i, adj in enumerate(solution):
            console.print(f"  Disc {i}: x_adjustment = [magenta]{adj}[/magenta]")

        final_matrix = rotate_and_overlay(discs, solution)
        df = pd.DataFrame(final_matrix).fillna("")
        console.print()
        console.print("[bold]Final shape:[/bold]")
        console.print(df.to_string())

    if count == 0:
        console.print("[red]No solution found.[/red]")
    else:
        console.print()
        console.print(f"[bold green]Total: {count} solution(s) found.[/bold green]")


if __name__ == "__main__":
    main()
