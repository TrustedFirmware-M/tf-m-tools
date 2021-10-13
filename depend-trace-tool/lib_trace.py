# -----------------------------------------------------------------------------
# Copyright (c) 2021, Arm Limited. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#
# -----------------------------------------------------------------------------

import os
import glob
import sys
import getopt
import json
from graphviz import Digraph

# Const variables
Public, Interface, Private = 0, 1, 2
Static_lib, Interface_lib, Unknown_lib = 'lightgreen', 'lightblue2', 'pink'
input_flag, output_flag = 0, 1
library_flag, include_flag, source_flag, compile_definition_flag = 0, 1, 2, 3
help_msg = 'This is a tool to draw a library\'s link relationship.\
The usage is:\n\
python3 lib_trace.py -l <library_name>\n\
                     -p <repo_path_1,repo_path_2,...>\n\
                     -d <max depth>\n\
                     -i # draw src libraries\n\
                     -o # draw dst libraries\n\
                     -h # help message'
edge_color = {
    'PUBLIC': 'green',
    'PRIVATE': 'red',
    'INTERFACE': 'blue',
    '': 'black'
}
gz_library = Digraph(
    name="CMake Library Relationship",
    comment='comment',
    filename=None,
    directory=None,
    format='png',
    engine=None,
    encoding="UTF-8",
    graph_attr={'rankdir': 'LR'},
    node_attr={
        'color': 'lightblue2',
            'fontcolor': 'black',
            'fontname': 'TimesNewRoman',
            'fontsize': '24',
            'shape': 'Mrecord',
            'style': 'filled',
    },
    edge_attr={
        'color': '#999999',
        'fontcolor': 'black',
        'fontsize': '16',
        'fontname': 'TimesNewRoman'
    },
    body=None,
    strict=True
)

def find_file_in_path(path, name_list):
    """
    Search file in a list of 'path' which name is in 'name_list' and the content
    in the file includes certain cmake function key words.
    """
    file_list, content = [], ''
    path_list = path.split(',')
    for sub_path in path_list:
        for name in name_list:
            for root, dirs, files in os.walk(sub_path):
                pattern = os.path.join(root, name)
                for sub_file in glob.glob(pattern):
                    content = open(sub_file,
                                   encoding="utf8",
                                   errors='ignore').read()
                    if 'add_library' in content \
                            or 'target_link_libraries' in content \
                            or 'target_include_directories' in content \
                            or 'target_sources' in content\
                            or 'target_compile_definitions' in content:
                        file_list.append(sub_file)
    return file_list

def get_library_name_and_property(file_list):
    """
    Get library name and property, including static, interface and unknown.
    """
    ret = {}
    for sub_file in file_list:
        file_content = open(sub_file).read()
        position_start = 0
        while position_start >= 0:
            position_start = file_content.find(
                'add_library', position_start + len('add_library'))
            if position_start > 0:
                position_end = file_content.find(')', position_start) + 1
                add_library = file_content[position_start:position_end]
                lib_name = add_library[add_library.find(
                    '(')+1: add_library.find(' ')]
                if add_library.find('STATIC') > 0:
                    ret[lib_name] = Static_lib
                elif add_library.find('INTERFACE') > 0:
                    ret[lib_name] = Interface_lib
                else:
                    ret[lib_name] = Unknown_lib
    return ret

def check_input_library():
    """
    Check the input library whether exists.
    """
    flag = False
    for s in all_libs.keys():
        if s == library:
            flag = True
    if not flag:
        print("Error: library %s doesn't exist!"% library)
        exit(2)

def get_relationship(key_word, relationship_flag):
    """
    Get relationship in cmake files between target and source.

    The target is usaually a library name and it will be added into the key_word
    to search suitable dependencies, including source_libraries, include paths,
    source files and compiler definitions. These different classes are
    determined by relationship_flag.

    It will return a list of [source, target, cmake_key_word, condition]
    """
    def rename_file(initial_file, current_path, relationship_flag):
        """
        Format the source name into ablsolute path if it is a include path or
        source file.
        TODO: Add more checks about CMAKE variables
        """
        ret = ""
        if relationship_flag == library_flag or \
                relationship_flag == compile_definition_flag:
            ret = initial_file
        elif relationship_flag == include_flag:
            if 'CMAKE_CURRENT_SOURCE_DIR' in initial_file:
                ret = current_path[:-len('CMakeLists.txt')] + \
                    initial_file[len('$\{CMAKE_CURRENT_SOURCE_DIR\}') - 1:]
            elif '$' in initial_file:
                ret = initial_file
            else:
                if len(initial_file) == 1 and initial_file[0] == '.':
                    ret = current_path[:-
                                       len('CMakeLists.txt')] + initial_file[1:]
                else:
                    ret = current_path[:- len('CMakeLists.txt')] + initial_file
        elif relationship_flag == source_flag:
            if 'CMAKE_CURRENT_SOURCE_DIR' in initial_file:
                ret = current_path[:-len('CMakeLists.txt')] + \
                    initial_file[len('$\{CMAKE_CURRENT_SOURCE_DIR\}') - 1:]
            elif '$' in initial_file:
                ret = initial_file
            else:
                ret = current_path[:- len('CMakeLists.txt')] + initial_file
        return ret

    def delete_comment(input):
        """
        Sometimes there are comments in cmake key content which will affect the
        source deal.
        """
        left_idx = 0
        right_idx = 0
        while left_idx >= 0:
            left_idx = input.find('#', left_idx + 1)
            right_idx = input.find('\n', left_idx)
            input = input.replace(input[left_idx:right_idx], "")
        return input

    ret, cmake_key_word = [], ""
    for sub_file in file_list:
        left_idx = 0
        file_content = open(sub_file,
                            encoding="utf8",
                            errors='ignore').read()
        while left_idx >= 0:
            left_idx = file_content.find(key_word, left_idx + len(key_word))
            if left_idx > 0:
                right_idx = file_content.find(')', left_idx) + 1

                # Get the key content without any cmake comment
                key_content = delete_comment(file_content[left_idx:right_idx])

                # Get source list
                src_list = key_content.split()

                # Get the target library name
                target = src_list[0][key_content.find('(') + 1:]

                for src in src_list[1:-1]:
                    if src in ['PUBLIC', 'INTERFACE', 'PRIVATE']:
                        cmake_key_word = src
                        continue
                    else:
                        condition = ""
                        if src.find(':') > 0:

                            # Get link condition
                            condition = src[2:-(len(src.split(':')[-1]) + 1)]
                            src = src.split(':')[-1][:-1]

                        ret.append([rename_file(src,
                                                sub_file,
                                                relationship_flag),
                                    target,
                                    cmake_key_word,
                                    condition])
    return ret

def append_lib():
    """
    Append more libraries into all_libs from link_library
    """
    tmp = []
    for s in all_libs:
        tmp.append(s)

    for s in link_library:
        if s[0] not in tmp:
            tmp.append(s[0])
            all_libs[s[0]] = Unknown_lib
        if s[1] not in tmp:
            tmp.append(s[1])
            all_libs[s[1]] = Unknown_lib

def restruct_relationship(flag, target_library, input_relationship):
    """
    The input_relationship is a list of [source, target, cmake_key_word,
    condition], and it shows like:
                   condition
    source   -----cmake_key_word--->     target

    This function will traverse the input_relationship and restruct the
    relationship into a dictionary.
    """
    ret = {'PUBLIC': [], 'PRIVATE': [], 'INTERFACE': []}
    lib_public, lib_interface, lib_private = [], [], []
    if flag == input_flag:
        target_idx, source_idx = 1, 0
    elif flag == output_flag:
        """
        An exception situation is when searching the target's destination
        library which links the target. So the index will be reversed.
        """
        target_idx, source_idx = 0, 1

    for lib in input_relationship:

        # Avoid repeat
        for s in ret['PUBLIC']:
            lib_public.append(s['name'])
        for s in ret['PRIVATE']:
            lib_interface.append(s['name'])
        for s in ret['INTERFACE']:
            lib_private.append(s['name'])

        if target_library == lib[target_idx]:
            if lib[2] in ['PUBLIC', 'public', 'Public'] and \
                    lib[source_idx] not in lib_public:
                ret['PUBLIC'].append({'name': lib[source_idx],
                                      'condition': lib[3]})
            if lib[2] in ['INTERFACE', 'interface', 'Interface'] and \
                    lib[source_idx] not in lib_interface:
                ret['INTERFACE'].append({'name': lib[source_idx],
                                         'condition': lib[3]})
            if lib[2] in ['PRIVATE', 'private', 'Private'] and \
                    lib[source_idx] not in lib_private:
                ret['PRIVATE'].append({'name': lib[source_idx],
                                       'condition': lib[3]})
    for s in ret.keys():

        # Sort the ret with key 'name'
        ret[s] = sorted(ret[s], key=lambda i: i['name'])
    return ret

def draw_graph(flag, target_library, drawed_libs, drawed_edges, deep_size):
    """
    Draw the library graph.
    Parameters:
        flag:           To get whether source or destination libraries
        target_library: The target library
        drawed_libs:    A list of libraries which already be added as a node
        drawed_edges:   A list of drawed edges in the graph
        deep_size:      Current iteration count
    """
    if flag == input_flag:
        libs = restruct_relationship(flag, target_library, link_library)
    elif flag == output_flag:
        libs = restruct_relationship(flag, target_library, link_library)
    lib_count = 0

    # Get source's count which is the condition of iteration.
    for s in libs.keys():
        lib_count += len(libs[s])
    if lib_count != 0 and deep_size < max_dept:
        for s in libs.keys():
            for lib in libs[s]:

                # Draw source node
                if lib['name'] not in drawed_libs:
                    deep_size += 1

                    # Draw iteration
                    draw_graph(flag, lib['name'], drawed_libs, drawed_edges,
                               deep_size)
                    deep_size -= 1
                    gz_library.node(name=lib['name'],
                                    color=all_libs[lib['name']])
                    drawed_libs.append(lib['name'])

                # Draw taget node
                if target_library not in drawed_libs:
                    gz_library.node(name=target_library,
                                    color=all_libs[target_library])
                    drawed_libs.append(target_library)

                # Draw edage
                if [lib['name'], target_library] not in drawed_edges:
                    if flag == input_flag:
                        gz_library.edge(lib['name'],
                                        target_library,
                                        color=edge_color[s],
                                        label=lib['condition'])
                        drawed_edges.append([lib['name'], target_library])
                    elif flag == output_flag:
                        gz_library.edge(target_library,
                                        lib['name'],
                                        color=edge_color[s],
                                        label=lib['condition'])
                        drawed_edges.append([target_library, lib['name']])

def get_library_relationship():
    """
    Get a list of all library relationship.
    """
    key_word = 'target_link_libraries'
    ret = get_relationship(key_word, library_flag)
    return ret

def get_library_include(target_library):
    """
    Get a dictionary of library include pathes.
    """
    key_word = 'target_include_directories' + '(' + target_library
    ret = restruct_relationship(input_flag,
                                   target_library,
                                   get_relationship(key_word,
                                                    include_flag))
    return ret

def get_library_source(target_library):
    """
    Get a dictionary of library source files.
    """
    key_word = 'target_sources' + '(' + library
    ret = restruct_relationship(input_flag,
                                   target_library,
                                   get_relationship(key_word,
                                                    source_flag))
    return ret

def get_library_compile_definitions(target_library):
    """
    Get a dictionary of library compile definitions.
    """
    key_word = 'target_compile_definitions' + '(' + library
    ret = restruct_relationship(input_flag,
                                   target_library,
                                   get_relationship(key_word,
                                                    compile_definition_flag))
    return ret

def main(argv):
    opts = []
    global all_libs, library, link_library, PATH, max_dept, file_list
    src_flag, dst_flag = False, False
    drawed_edges, drawed_libs = [], []

    try:
        opts, args = getopt.getopt(
            argv, "hiol:p:d:", ["ilib=", "ppath=", "ddept="])
    except getopt.GetoptError:
        print(help_msg)
        sys.exit(2)
    if not opts:
        print(help_msg)
        sys.exit(2)

    # Get input options
    for opt, arg in opts:
        if opt == '-h':
            print(help_msg)
            sys.exit()
        elif opt in ("-l", "--ilib"):
            library = arg
        elif opt in ("-p", "--ppath"):
            PATH = arg
        elif opt in ("-d", "--ddept"):
            max_dept = int(arg)
        elif opt == '-o':
            dst_flag = True
        elif opt == '-i':
            src_flag = True

    # Get all library relationship and all libraries
    file_list = find_file_in_path(PATH, ['*.txt', '*.cmake'])
    all_libs = get_library_name_and_property(file_list)
    link_library = get_library_relationship()
    append_lib()

    check_input_library()

    src_lib = restruct_relationship(input_flag, library, link_library)
    dst_lib = restruct_relationship(output_flag, library, link_library)
    include = get_library_include(library)
    source = get_library_source(library)
    definitions = get_library_compile_definitions(library)

    # Draw graph
    if src_flag:
        drawed_libs = []
        draw_graph(input_flag, library, drawed_libs, drawed_edges, 0)
    if dst_flag:
        drawed_libs = []
        draw_graph(output_flag, library, drawed_libs, drawed_edges, 0)

    # Redraw the target library as a bigger node
    gz_library.node(name=library,
                    fontsize='36',
                    penwidth='10',
                    shape='oval')

    # Save picture
    gz_library.render(filename=library)

    # Write into a file with JSON format
    log = {'library name': library,
           'source libraries': src_lib,
           'destination libraries': dst_lib,
           'include directories': include,
           'source files': source,
           'compiler definitions': definitions
           }
    fo = open(library + ".log", "w")
    fo.write(json.dumps(log,
             sort_keys=False, indent=4, separators=(',', ': ')))
    fo.close()

    fo = open(library + '.txt', "w")
    for s in log.keys():
        if s == 'library name':
            fo.write('library name: ' + s + '\n')
            continue
        fo.write('\n' + s + ':\n')
        for t in log[s].keys():
            if log[s][t]:
                fo.write('\t' + t + '\n')
                for x in log[s][t]:
                    if x['condition']:
                        fo.write('\t\t' + x['name'] + '\t<----\t'\
                                  + x['condition'] + '\n')
                    else:
                        fo.write('\t\t' + x['name'] + '\n')
    fo.close()

if __name__ == "__main__":
    main(sys.argv[1:])
