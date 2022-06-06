from di import containers
import argparse

def import_dataset(name, path):
    print(name, path)
    importer = containers.inject_dataset_importer()

    importer.import_dataset(name, path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset-name", "-n", help="dataset name to import", type=str, required=True)
    parser.add_argument(
        "--path", "-p", help="dataset file path", type=str, required=True)
    
    args = parser.parse_args()

    import_dataset(args.dataset_name, args.path)


main()