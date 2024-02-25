from input.input_csv import open_file
from input.data_structure import arm_tree, get_all_Teams,  calculate_all, delete_all_min_max, delete_all_weight, calculate_new_weight,  delete_all, get_scores
from anytree import RenderTree
from input.minmax import minmax






#delete_all()
#open_file(r'C:\Users\Morpheus\Code\Min-Max_Score_Table\temp.records.csv')
delete_all_min_max()
delete_all_weight()
calculate_new_weight()
calculate_all(True)


