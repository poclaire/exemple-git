import sys, argparse, importlib, traceback
import pyhocon

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def parseargs(args, config):
    msg = "Runing Annual Statement of Payemnt model"
    usage = "main.py <task_name> [<args>] [-h | --help]"
    parser = argparse.ArgumentParser(description=msg, usage=usage)

    for key, value in dict(config).items():
        parser.add_argument("--"+key, default=value, type=type(value))

    msg = "Earse previously written files (Run from zero)"
    parser.add_argument("--initialize", action='store_true', help=msg)
    msg = "Frequentlty serach for new PDF submissions and late issuers"
    parser.add_argument("--search_sub", action='store_true', help=msg)
    msg = "Process MS Word. Input: path to docx | Output"
    parser.add_argument("--process_word", action='store_true', help=msg)
    msg = "PostProcessing"
    parser.add_argument("--postprocess", action='store_true', help=msg)

    return parser.parse_args(args)


tasks = {"asop": "data_entry_assistant",
         "miner_note": "data_entry_assistant",
         "loan_acpt": "data_entry_assistant",
         "actif_net": "data_entry_assistant",

         "miner_promo": "rule_filtring",
         "miner_sm": "rule_filtring",
         "fgm_change": "rule_filtring",
         "arrangement": "rule_filtring",
         "nr_change": "rule_filtring"}


def helpinfo():
    print("usage:")
    print("\tmain.py <command> [<args>]")
    print("using 'main.py <{}> --help' to see valid options".format('|'.join(tasks.keys())))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        helpinfo()
    else:
        command = sys.argv[1]

        if command not in tasks.keys() :    
            helpinfo()
            raise ValueError("Not recognize task. List of valid task: {}".format('|'.join(tasks.keys())))
 
        pkg = tasks[command]
        main_module = importlib.import_module(pkg+"."+command, package=None)
        print("Command list:")
        print(" ".join(sys.argv))
        config = pyhocon.ConfigFactory.parse_file(pkg+"/experiments.conf")[command]
        parsed_args = parseargs(sys.argv[2:], config)
        dico = dict([(att, getattr(parsed_args, att)) for att in dir(parsed_args) if not att.startswith("_")])
        config.update(dico)

        for item in    ["initialize", "search_sub", "process_word", "postprocess"]:
            if getattr(parsed_args, item):
                try:
                    getattr(main_module, item)(config)
                except Exception as e:
                    traceback.print_exc()
                    print(e)
                    input("Bug occurs!!!! Please take a screen shot of the console and send it to Fintech Lab.\nPress Enter to close the program")
les modifications marches
deuxiemes modifications 


