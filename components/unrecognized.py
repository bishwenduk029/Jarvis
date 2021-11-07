from os.path import isfile, sep

from yaml import dump


def unrecognized_dumper(converted: str) -> None:
    """If none of the conditions are met, converted text is written to a yaml file.

    Args:
        converted: Takes the voice recognized statement as argument.
    """
    train_file = {'Uncategorized': converted}
    if isfile(f'..{sep}training_data.yaml'):
        with open(f'..{sep}training_data.yaml') as train_read:
            content = train_read.read()
        for key, value in train_file.items():
            if str(value) not in content:  # avoids duplication in yaml file
                dict_file = [{key: [value]}]
                with open(f'..{sep}training_data.yaml', 'a') as writer:
                    dump(dict_file, writer)
    else:
        for key, value in train_file.items():
            train_file = [{key: [value]}]
        with open(f'..{sep}training_data.yaml', 'w') as writer:
            dump(train_file, writer)
