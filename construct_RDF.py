import csv

to_encode = [
    ':', '/', '?', '#', '[', ']', '@', '!', '$', '&', "'",
    '(', ')', '*', '+', ',', ';', '=', '<', '>', '"', ' ',
    '{', '}', '|', '\\', '^', '`'
]

def encode_string(string:str):
    new_string = ''
    for char in string:
        if char in to_encode:
            new_string += '%' + hex(ord(char))[2:]
            continue
        new_string += char
    return new_string

def write_to_csv(filename:str, items:list):
    writer = csv.writer(open(filename, "w"))
    writer.writerows(items)

def csv_to_eav(scheduleFile:str, filename:str):
    reader = csv.reader(open(scheduleFile))
    header = next(reader)
    eav = []
    for row in reader:
        # print(reader.line_num, row)
        
        for col, val in zip(header, row):
            if col == 'Ώρα':
                new_vals = val.split('-')
                # print(new_vals)
                eav.append([reader.line_num - 1, 'Ώρα Έναρξης', new_vals[0]])
                eav.append([reader.line_num - 1, 'Ώρα Λήξης', new_vals[1]])
            else:
                eav.append([reader.line_num - 1, col, val])
    # [print(e) for e in eav]
    write_to_csv(filename, eav)
    return eav 

def eav_to_graph(eav:list, filename:str):
    graph = list(eav)
    graph = [["b:" + str(sub), pre, "u:" + obj] if pre in ["Μάθημα", "Αίθουσα", "Διδάσκων"] else ["b:" + str(sub), pre, "l:" + obj] for sub, pre, obj in graph]
    # [print(g) for g in graph]
    write_to_csv(filename, graph)
    return graph

def graph_to_iri(graph:list, filename:str, home_uri:str):
    iri = list(graph)
    iri = [[sub, home_uri + "/myvocab#" + encode_string(pre), home_uri + "/resource/" + encode_string(obj.replace("u:", ""))] if "u:" in obj else [sub, home_uri + "/myvocab#" + encode_string(pre), obj] for sub, pre, obj in iri]
    # [print(i) for i in iri]
    write_to_csv(filename, iri)
    return iri

def iri_to_rdf(iri:list, filename:str):
    fp = open(filename, "w")
    rdf = []
    for sub, pre, obj in iri:
        sub = "_:" + sub[2:]
        if "l:" in obj:
            obj = obj.replace("l:", "")
            if "Ώρα" in pre:
                obj += ":00"
            obj = "\"" + obj + "\""
        else:
            obj = "<" + obj + ">"
        rdf.append([sub, pre, obj])
        fp.write(" ".join(rdf[-1]) + " .\n")
    return rdf
    

if __name__ == "__main__":
    eav = csv_to_eav("Schedule.csv", "EAV_Schedule.csv")
    graph = eav_to_graph(eav, "Graph_Schedule.csv")
    home_uri = "http://host/sw/p15papa1"
    iri = graph_to_iri(graph, "IRI_schedule.csv", home_uri)
    rdf = iri_to_rdf(iri, "RDF_Schedule.nt")



