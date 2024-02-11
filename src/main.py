from kybra import query, update, void

# This is a global variable that is stored on the heap
protein: str = ''
ligand: str = ''
result: str = 'tmp'
sim_ran: bool = False

# Query calls complete quickly because they do not go through consensus
@query
def get_results() -> str:
    return protein+","+ligand+","+result
    # if sim_ran:
    #     return {
    #         "protein":protein, 
    #         "ligand":ligand, 
    #         "result":result,
    #         "error": "False",
    #         "message":""
    #         }
    # else:
    #     return {
    #         "error": "True",
    #         "message": "simulation has not been run"
    #     }

# Update calls take a few seconds to complete
# This is because they persist state changes and go through consensus
@update
def set_message(protein_smiles: str, ligand_smiles: str) -> void:
    global protein
    global ligand
    protein = protein_smiles 
    ligand = ligand_smiles

@update
def run_sim() -> void:
    global sim_ran
    run_diffdock()
    sim_ran = True

def run_diffdock() -> void:
    # TODO: run diffdock on set inputs
    pass