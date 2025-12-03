from dataclasses import dataclass, field


@dataclass
class CategoryRanges:
    name: str
    min: int
    max: int

@dataclass
class Dimension:
    name: str
    items: dict[str, CategoryRanges] = field(default_factory=dict)

    def add_item(self, item: CategoryRanges):
        self.items[item.name] = item

    def get_ranges(self) -> list[CategoryRanges]:
        return list(self.items.values())

@dataclass
class Dimensions:
    dimensions: dict[str, Dimension] = field(default_factory=dict)

    def add_category_range(self, dimension_name: str, item: CategoryRanges):
        if dimension_name not in self.dimensions:
            self.dimensions[dimension_name] = Dimension(name=dimension_name)
        self.dimensions[dimension_name].add_item(item)

    def get_dimension(self, category_name: str) -> Dimension:
        return self.dimensions.get(category_name)

    @property
    def dimension_names(self) -> list[str]:
        return list(self.dimensions.keys())
