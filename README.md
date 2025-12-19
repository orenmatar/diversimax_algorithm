# DiversiMax: Maximizing Intersectional Diversity in Sortition

**📚 [Read more about the algorithm and see comparisons →](https://orenmatar.github.io/diversimax_algorithm/)**

**NOTE**: the algorithm has been merged into
https://github.com/sortitionfoundation/sortition-algorithms
which offers more sortition algorithms, and more support in pre-processing, validating the data etc. It is reccomended to use that repo.

## Overview

DiversiMax is a sortition algorithm that selects citizen assembly panels by maximizing intersectional diversity while maintaining demographic quotas. The algorithm optimizes for diversity across all combinations of demographic categories (e.g., age × gender × education), not just within individual categories.

### How It Works

The algorithm uses Mixed Integer Programming (MIP) to optimize diversity by balancing representation across all intersectional demographic tables. It generates intersection tables for all demographic dimensions and their combinations, then minimizes total deviation from optimal balanced values across all intersections. This approach ensures all demographic quota constraints are satisfied while reducing empty cells and promoting representation of marginalized identities.

## Key Features

- ✅ **Intersectional diversity optimization** - Goes beyond single-category quotas
- ✅ **Quota compliance** - Maintains required demographic representation ranges
- ✅ **Resampling support** - Handle participant withdrawals efficiently

## Installation

```bash
git clone https://github.com/orenmatar/diversimax_algorithm.git
cd diversimax_algorithm
pip install -r requirements.txt
```

## Quick Start

The easiest way to run DiversiMax is through `main.py`:

1. Open `main.py`
2. Configure your parameters:
   ```python
   pool_members_file = "path/to/your/pool.csv"
   panel_size = 30
   participating_column = "participating"
   ```
3. Run the algorithm:
   ```bash
   python main.py
   ```

This will load your data and generate an optimally diverse panel.

## Input File Requirements

DiversiMax requires two CSV files:

### 1. Participants Pool File

Contains demographic information for all potential participants. Must include a `participating` column (or your custom column name) with values: `"yes"`, `"no"`, or `"?"`. This can be used if resampling is needed after pool members are contacted for confirmation, and some drop out: simply indicate the status of each pool member, and the algorithm will create a new sample which will respect the members' responses.

**Example:**
```csv
area,age,gender,education,religiousness,participating
south,40-49,female,16+,secular,?
center-north,70+,female,16+,secular,?
center-south,40-49,female,15-13,secular,?
```

### 2. Quota Ranges File

Defines minimum and maximum representation for each demographic category.

**Example:**
```csv
category,name,min,max
area,center-north,18,18
area,center-south,15,15
area,east,11,11
area,south-west,5,5
```

Example files are available in the `example_data/` folder.

## Output

The algorithm outputs the IDs (line numbers) of selected participants from the pool file.

## Learn More

For detailed methodology, comparisons with other algorithms, and empirical results:  
**[https://orenmatar.github.io/diversimax_algorithm/](https://orenmatar.github.io/diversimax_algorithm/)**

## Citation

If you use DiversiMax in your research or democratic processes, please cite:

```
Matar, O. (2025). Diversimax: Maximizing Intersectional Diversity in Sortition.
Democracy 3.0. https://orenmatar.github.io/diversimax_algorithm/
```

## Contact

**Oren Matar**  
[Democracy 3.0](https://www.democracy3.org.il/eng)

For questions, issues, or contributions, please open an issue on GitHub.

---

*Developed by Democracy 3.0 for use in participatory democratic processes.*
