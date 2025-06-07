import pickle
    
def import_pickle(pickle_location):
    print("Importing ",  pickle_location)
    with open(pickle_location, 'rb') as dataset_file:
        dataset = pickle.load(dataset_file)
        return dataset
    
def export_pickle(data, pickle_name, is_not_df: bool = False):
    print("Saving to", pickle_name)
    if is_not_df:
        pickle.dump(data, open(pickle_name, 'wb'))
    else:
        data.to_pickle(pickle_name)

