from input.input_csv import open_file, CalculateWeight
from input.data_structure import arm_tree, get_all_Teams, wide_walk_str
from anytree import RenderTree
from input.minmax import minmax



#print(open_file(r"C:\Users\Morpheus\Code\Min-Max_Score_Table\temp.records.csv"))
#CalculateWeight()
print(minmax(arm_tree("Burnley", "Tottenham"),[-99999999999, 999999999999]))


