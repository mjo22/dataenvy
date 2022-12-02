"""
Collection of routines to read different classes of datasets, read
by the script Write.py.

To add a routine, use the skeleton

def read_mydata(filename, example=5, **kwargs):
     # Load data
     data = load(filename)  # You'll need to fill in how you load your data
     # Return data
     return data

After setting up your dataset, refer to one of these functions in your
analysis config file MyConfig.toml for Write.py with the line

[read_mydata]
example = 20  # Set keyword from config file

"""
