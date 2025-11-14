import pandas as pd
import itertools
import mip
from mip import MAXIMIZE, CBC, OptimizationStatus, MINIMIZE, BINARY, xsum, maximize, minimize
from sklearn.preprocessing import OneHotEncoder

"""
TODO:
Move optimizer code to a new file (after initial tests)
copy notebook for each assembly


FUTURE:
maximize geometric mean of each intersection table (+1 to avoid 0s)?
AT LEAST USE GMEAN AS A METRIC FOR HOW CLOSE WE ARE TO IDEAL.. TO COMPARE DIFFERENT METHODS

**may still need to weigh different intersection tables, based on the number of dims
- consider the number of panel members..?

**with >4 dimensions all intersection sizes will be 0/1 anyway... detect those cases and ignore those intersection tables
- much better than the MAX_DIMS_INTERSECTION_TO_OPTIMIZE_ON limitation we have now.
"""

class DiversityOptimizer(object):
    MAX_DIMS_INTERSECTION_N_TO_OPTIMIZE = 100

    def __init__(self, df, participating_col):
        self.df = df
        self.participating_col = participating_col
        self.data, self.all_dims_combs = self.prepare_all_data()
        self.all_ohe = self.create_all_one_hot_encodings()

    def _prepare_dims_data(self, dims):
        all_cat_combs = ['__'.join(x) for x in itertools.product(*[self.df[d].unique() for d in dims])]
        peoples_ids = self.df.loc[:, dims].apply(lambda row: '__'.join([row[d] for d in dims]), axis=1).values
        return {'all_cat_combs': all_cat_combs, 'peoples_ids': peoples_ids}

    def prepare_all_data(self):
        """
        Creates the data for optimization.
        Returns people data and all_dims_combs
        the data is a dict where key is a dim combination
        all_dims_combs - all the combinations of dimensions we can have e.g. (gender,), (gender, age)... (age, income, settlment type)
        """
        all_dims_combs = [itertools.combinations(self.df.columns, r=i) for i in range(1, self.df.shape[1] + 1)]
        all_dims_combs = [x for y in all_dims_combs for x in y]
        data = {}
        for dims in all_dims_combs:
            try:
                data[dims] = self._prepare_dims_data(dims)
            except Exception as e:
                print(e)
                raise Exception(f'Error with {dims}')
        return data, all_dims_combs

    def create_all_one_hot_encodings(self):
        """
        For every set of dimensions - one hot encode who is in which intersection.
        Rows are people. Columns are the different intersections.
        i.e. The columns are the number of combinations we have between the dimensions: product of their sizes.
        """
        all_ohe = []
        for dims in self.all_dims_combs:
            data = self.data[dims]
            possible_profiles = data['all_cat_combs']
            # only up to a certain amount of intersections. Each intersection adds a variable, makes the optimization more difficult.
            if len(possible_profiles) > DiversityOptimizer.MAX_DIMS_INTERSECTION_N_TO_OPTIMIZE:
                continue

            peoples_ids = data['peoples_ids']
            ohe = OneHotEncoder(categories=[possible_profiles], sparse_output=False)
            ohe = ohe.fit_transform(peoples_ids.reshape(-1, 1))
            all_ohe.append(ohe)
        return all_ohe

    def optimize(self, categories, panel_size):
        """
        Uses MIP to optimize based on the categories constraints

        For the optimization goal, for every dims intersection:
        Take the one hot encoded of who is in which intersection for these dims
        Take the binary vector of who is selected and multiply and sum to get the sizes of each intersection of categories
        Figure out the "best" value - if all intersections were of equal size
        Take the abs for each intersection from that value
        Minimize sum of abs
        """
        df = self.df
        m = mip.Model()  # for this to work you must have a gurubi license under env variable GRB_LICENSE_FILE. Otherwise specify mip solver_name
        # binary variable for each person - if they are selected or not
        model_variables = []
        m
        for person_id in df.index:
            var = m.add_var(var_type='B', name=str(person_id))
            model_variables.append(var)
            # add constraint - everyone who is already participating must remain selected
            if self.participating_col.loc[person_id] == 'yes':
                m.add_constr(var >= 1)
            elif self.participating_col.loc[person_id] == 'no':
                m.add_constr(var <= 0)
        model_variables = pd.Series(model_variables, index=df.index)

        # the sum of all people in each category must be between the min and max specified
        for dim, d in categories.items():
            for cat, const in d.items():
                relevant = model_variables[df[dim] == cat]
                rel_sum = xsum(relevant)
                m.add_constr(rel_sum >= const['min'])
                m.add_constr(rel_sum <= const['max'])
        m.add_constr(xsum(model_variables) == panel_size)  # cannot exceed panel size

        # define the optimization goal
        all_objectives = []
        for ohe in self.all_ohe:  # for every set of dims
            intersection_sizes = (model_variables.values.reshape(-1, 1) * ohe).sum(
                axis=0)  # how many selected to each intersection
            best_val = panel_size / ohe.shape[1]  # if all intersections were equal size

            # set support variables that are the diffs from each intersection size to the most equal value
            diffs_from_best_val = [m.add_var(var_type='C') for x in intersection_sizes]
            # constrain these support variables to be the abs diff from the intersection size
            for abs_diff, intersection_size in zip(diffs_from_best_val, intersection_sizes):
                m.add_constr(abs_diff >= (intersection_size - best_val))
                m.add_constr(abs_diff >= (best_val - intersection_size))

            support_vars_sum = xsum(diffs_from_best_val)  # we will minimize the abs diffs
            all_objectives.append(support_vars_sum)

        obj = xsum(all_objectives)
        m.objective = minimize(obj)
        m.optimize()
        selected = pd.Series([v.x for v in m.vars][:len(df)]) == 1
        # clear_output()

        return m, selected