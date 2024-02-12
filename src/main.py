from kybra import (
    Async,
    CallResult,
    ic,
    match,
    query, 
    update, 
    void
)

from kybra.canisters.management import (
    HttpResponse,
    HttpTransformArgs,
    management_canister,
)

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

@update
def run_diffdock_demo() -> Async[HttpResponse]:
    global sim_ran
    http_result: CallResult[HttpResponse] = yield management_canister.http_request(
        {
            "url": "https://diffdock-flask-pip.azurewebsites.net/icp/demo",
            "max_response_bytes": 2_000,
            "method": {"get": None},
            "headers": [],
            "body": None,
            "transform": {"function": (ic.id(), "xkcd_transform"), "context": bytes()},
        }
    ).with_cycles(50_000_000)

    sim_ran = True

    return match(http_result, {"Ok": lambda ok: ok, "Err": lambda err: ic.trap(err)})

@query
def xkcd_transform(args: HttpTransformArgs) -> HttpResponse:
    http_response = args["response"]

    http_response["headers"] = []

    return http_response