import os
import pandas as pd 
from pathlib import Path 

def file_upload_location(instance, filename):
    return os.path.join('%s/%s/%s/%s/%s' % (instance.enterprise.name, instance.client.name, instance.engagement.name, instance.stockcount.name, filename))

    return os.path.join("%s" % str(instance.enterprise), "%s" % str(instance.client), "%s" % str(instance.engagement), "%s" % str(instance.stockcount), filename)

    ext = filename.split('.')[-1]
    # return f"{instance.enterprise}/{instance.client}/{instance.engagement}/{instance.stockcount}/{filename}"
    # return f"{filename}"
    FileType = '\\Inventory List'
    name = str(filename)
    path = os.path.join(str(instance.enterprise), str(instance.client), str(instance.engagement), str(instance.stockcount))
    # return f"{path}/{filename}"
    # return path 
    print(f"The path is {path}")
    # return f"{path}/"
    # return '{0}/{1}/{2}/{3}/{4}'.format(str(instance.enterprise), str(instance.client), str(instance.engagement), str(instance.stockcount), filename)
    return os.path.join("%s" % str(instance.enterprise), "%s" % str(instance.client), "%s" % str(instance.engagement), "%s" % str(instance.stockcount), filename)



    
def ReturnIndex(dfObj, value):
    listOfPos = list()
    # Get bool dataframe with True at positions where the given value exists
    result = dfObj.isin([value])
    # Get list of columns that contains the value
    seriesObj = result.any()
    columnNames = list(seriesObj[seriesObj == True].index)
    # Iterate over list of columns and fetch the rows indexes where value exists
    for col in columnNames:
        rows = list(result[col][result[col] == True].index)
        for row in rows:
            listOfPos.append((row, col))
    # Return a list of tuples indicating the positions of value in the dataframe
    return listOfPos