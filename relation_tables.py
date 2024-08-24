import pandas as pd


class RelationTable:
    def __init__(self, table_1=pd.DataFrame(), table_2=pd.DataFrame()):
        self.table_1 = table_1
        self.table_2 = table_2

    def relation_table_inner(self, left_table_column=str(), right_table_column=str()):
        table_merged = pd.merge(left=self.table_1,
                                right=self.table_2,
                                left_on=left_table_column,
                                right_on=right_table_column,
                                how='inner'
                                )
        return table_merged

    def relation_table_left(self, left_table_column=str(), right_table_column=str()):
        table_merged = pd.merge(left=self.table_1,
                                right=self.table_2,
                                left_on=left_table_column,
                                right_on=right_table_column,
                                how='left'
                                )
        return table_merged

    def relation_table_right(self, left_table_column=str(), right_table_column=str()):
        table_merged = pd.merge(left=self.table_1,
                                right=self.table_2,
                                left_on=left_table_column,
                                right_on=right_table_column,
                                how='right'
                                )
        return table_merged
