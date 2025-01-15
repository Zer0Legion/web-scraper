from openai import OpenAI
from dotenv import dotenv_values
import requests

CONFIG = {
    **dotenv_values(".env")
}
URL = "https://api.openai.com/v1/chat/completions"

def main(content):
    client = OpenAI(organization="Personal", project="Default project", api_key=CONFIG["OPENAI_API_KEY"])
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + CONFIG["OPENAI_API_KEY"]
    }
    data = {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": content}],
        "temperature": 1,
        "max_tokens": 4095,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "response_format": {
            "type": "text"
        }
    }

    response = requests.post(URL, headers=headers, json=data)
    print(response.json())

if __name__ == "__main__":
    main("""

Why are these blocks needed to accommodate for the "unassigned" functionality? 
             // CHANGED HERE

        } else if (is_declaration(command)) {
            C = pair(declaration_value_expression(command),
                  pair(make_init_instruction(
                         declaration_symbol(command)),
                       C));                     
                     
        } else if (is_name(command)) {
            S = pair(lookup_symbol_value(
                         symbol_of_name(command),
                         E),
                     S);
        } else if (is_assignment(command)) {
            C = pair(assignment_value_expression(command),
                  pair(make_assign_instruction(
                         assignment_symbol(command)),
                       C));
         
                 } else if (is_init_instruction(command)) {
            init_symbol_value(
               init_instruction_symbol(command), 
               head(S),
               E);        

function is_init_instruction(component) {
    return is_tagged_list(component, "init");
}
function init_instruction_symbol(component) {
    return head(tail(component));
}
function make_init_instruction(symbol) {
    return list("init", symbol);
}

         
""")