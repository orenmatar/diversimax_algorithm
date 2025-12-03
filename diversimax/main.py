import mip

from diversimax.algorithm import DiversityOptimizer
from diversimax.utils import read_categories_file, read_pool_members_file, verify_data

def main():
    panel_size = 60
    participating_col = 'participating'
    cats = read_categories_file('../example_data/categories_exact_ranges.csv')
    pool_members = read_pool_members_file('../example_data/participants_pool.csv')
    verify_data(pool_members, cats, participating_col, panel_size)
    optimizer = DiversityOptimizer(pool_members, participating_col=participating_col)
    model, selected = optimizer.optimize(dimensions=cats, panel_size=panel_size)

    assert model.status == mip.OptimizationStatus.OPTIMAL
    assert selected.sum() == panel_size
    # selected or participating is same as selected. i.e. everyone who was participating is still considered as such
    assert ((pool_members[participating_col] == 'yes') | selected == selected).all()
    print("Optimization successful. Selected panel size:", selected.sum())
    print("Selected participants IDs:", selected[selected == 1].index.tolist())

if __name__ == "__main__":
    main()