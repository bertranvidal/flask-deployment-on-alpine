import argparse
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, required=True)
    parser.add_argument("--top", type=int, required=True)
    parser.add_argument("--output_file", type=str, required=True)
    
    return parser.parse_args()

def main():
    args = parse_args()
    data = pd.read_csv(args.input_file, delimiter='\t', header=None)
    data.columns = ['user_id', 'check-in time', 'location_id']

    user_interactions = data['user_id'].value_counts()
    top_users = user_interactions.head(args.top)

    with open(args.output_file, 'w') as f:
        for user_id, _ in top_users.items():
            f.write(f"{user_id}\n")
    
        print(f"Top {args.top} users saved to {args.output_file}")

if __name__ == "__main__":
    main()
