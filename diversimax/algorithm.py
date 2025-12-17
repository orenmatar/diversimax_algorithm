import numpy as np
import pandas as pd
import itertools
import mip
from mip import xsum, minimize
from sklearn.preprocessing import OneHotEncoder
from dataclasses import dataclass

from diversimax.models import Dimensions

InteractionNamesTuple = tuple[str, ...]


@dataclass
class IntersectionData:
    intersections_names: list[str]
    intersection_member_values: np.array


@dataclass
class AllIntersectionsData:
    data: dict[InteractionNamesTuple, IntersectionData]
    all_dims_combs: list[InteractionNamesTuple]


class DiversityOptimizer(object):
    MAX_DIMS_INTERSECTION_N_TO_OPTIMIZE = 100

    def __init__(self, pool_members_df: pd.DataFrame, participating_col: str):
        self.participating_col = pool_members_df[participating_col]
        self.pool_members_df = pool_members_df.drop(columns=[participating_col])
        self.intersections_data: AllIntersectionsData = self.prepare_all_data()
        self.all_ohe = self.create_all_one_hot_encodings()

    @staticmethod
    def _intersection_name(category_names: tuple | list) -> str:
        return "__".join(category_names)

    def _prepare_dimensions_data(self, dimensions_names: tuple) -> IntersectionData:
        """
        Prepares the data for a given set of dimensions.
        Makes all the possible intersections between the dimensions' category names (e.g. male__18-24__highschool)
        Then for each person, figures out which intersection they belong to.
        """
        # Take all the combinations between the dimensions' category names
        all_combinations = itertools.product(*[self.pool_members_df[d].unique() for d in dimensions_names])
        intersections_names = [self._intersection_name(combination) for combination in all_combinations]
        # make the member value (join with __) for each person
        each_member_value = (
            self.pool_members_df.loc[:, dimensions_names]
            .apply(lambda row: self._intersection_name([row[d] for d in dimensions_names]), axis=1)
            .values
        )
        return IntersectionData(intersections_names=intersections_names, intersection_member_values=each_member_value)

    def prepare_all_data(self) -> AllIntersectionsData:
        """
        For each combination of dimensions, prepares the intersection data.
        The data is a dict where key is the combination of category names (e.g. (age, income, education level))
        and value is the IntersectionData for that combination.
        all_dims_combs is a list of all the intersections of all categories of all dimensions.
        (e.g. [(age,), (income,), (education level,), (income, education level), (age, income, education level)])
        """
        all_dims_combs_iterators = [
            itertools.combinations(self.pool_members_df.columns, r=i)
            for i in range(1, self.pool_members_df.shape[1] + 1)
        ]
        all_dims_combs: list[InteractionNamesTuple] = [x for y in all_dims_combs_iterators for x in y]
        data = {}
        for dimensions_intersections in all_dims_combs:
            try:
                data[dimensions_intersections] = self._prepare_dimensions_data(dimensions_intersections)
            except Exception as e:
                print(e)
                raise Exception(f"Error with {dimensions_intersections}")
        return AllIntersectionsData(data=data, all_dims_combs=all_dims_combs)

    def create_all_one_hot_encodings(self) -> list[np.array]:
        """
        For every intersection of dimensions - one hot encode who is in which intersection.
        Rows are the different people. Columns are the different possible intersections.
        The values are 0/1 if the person is in that intersection or not.
        i.e. The number of columns is the number of combinations we have between the dimensions: product of their sizes.
        """
        all_ohe = []
        for dims in self.intersections_data.all_dims_combs:
            intersection_data: IntersectionData = self.intersections_data.data[dims]
            possible_profiles = intersection_data.intersections_names
            # only up to a certain amount of intersections. Each intersection adds a variable, makes the optimization more difficult.
            if len(possible_profiles) > DiversityOptimizer.MAX_DIMS_INTERSECTION_N_TO_OPTIMIZE:
                continue

            ohe = OneHotEncoder(categories=[possible_profiles], sparse_output=False)
            ohe = ohe.fit_transform(intersection_data.intersection_member_values.reshape(-1, 1))
            all_ohe.append(ohe)
        return all_ohe

    def optimize(self, dimensions: Dimensions, panel_size: int) -> tuple[mip.Model, pd.Series]:
        """
        Uses MIP to optimize based on the categories constraints

        For the optimization goal, for every dims intersection:
        Take the one hot encoded of who is in which intersection for these dims
        Take the binary vector of who is selected and multiply and sum to get the sizes of each intersection of categories
        Figure out the "best" value - if all intersections were of equal size
        Take the abs for each intersection from that value
        Minimize sum of abs
        """
        df = self.pool_members_df
        m = mip.Model()
        # binary variable for each person - if they are selected or not
        model_variables = []
        for person_id in df.index:
            var = m.add_var(var_type="B", name=str(person_id))
            model_variables.append(var)
            # add constraint - everyone who already gave an answer must remain as they are
            if self.participating_col.loc[person_id] == "yes":
                m.add_constr(var >= 1)
            elif self.participating_col.loc[person_id] == "no":
                m.add_constr(var <= 0)
        model_variables = pd.Series(model_variables, index=df.index)

        # the sum of all people in each category must be between the min and max specified
        for dim_name in dimensions.dimension_names:
            dimension = dimensions.get_dimension(dim_name)
            for ranges in dimension.get_ranges():
                relevant_members = model_variables[df[dim_name] == ranges.name]
                rel_sum = xsum(relevant_members)
                m.add_constr(rel_sum >= ranges.min)
                m.add_constr(rel_sum <= ranges.max)
        m.add_constr(xsum(model_variables) == panel_size)  # cannot exceed panel size

        # define the optimization goal
        all_objectives = []
        for ohe in self.all_ohe:  # for every set of intersections of dimensions
            intersection_sizes = (model_variables.values.reshape(-1, 1) * ohe).sum(
                axis=0
            )  # how many selected to each intersection
            # the best value is if all intersections were equal size
            best_val = panel_size / ohe.shape[1]

            # set support variables that are the diffs from each intersection size to the best_val
            diffs_from_best_val = [m.add_var(var_type="C") for x in intersection_sizes]
            # constrain these support variables to be the abs diff from the intersection size
            for abs_diff, intersection_size in zip(diffs_from_best_val, intersection_sizes):
                m.add_constr(abs_diff >= (intersection_size - best_val))
                m.add_constr(abs_diff >= (best_val - intersection_size))

            support_vars_sum = xsum(diffs_from_best_val)  # we will minimize the abs diffs
            all_objectives.append(support_vars_sum)

        obj = xsum(all_objectives)
        m.objective = minimize(obj)
        m.optimize()
        selected = pd.Series([v.x for v in m.vars][: len(df)]).eq(1)

        return m, selected
