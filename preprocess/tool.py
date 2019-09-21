from androguard.misc import AnalyzeAPK
from androguard.core.analysis.analysis import ExternalMethod
import matplotlib.pyplot as plt
import networkx as nx
import os


def delete_external_and_xref0_nodes(CFG):
    nodes = list(CFG.nodes)[:]
    for orig_method in nodes:
        if isinstance(orig_method, ExternalMethod):
            CFG.remove_node(orig_method)
        else:
            if not CFG.degree()[orig_method]:
                CFG.remove_node(orig_method)


def delete_init_method(CFG,dx):
    nodes = list(CFG.nodes)[:]
    for orig_method in nodes:
        m_a = dx.get_method(orig_method)
        ins_seq = get_instruction_seq_for_func(m_a, [str(n) for n in CFG.nodes])
        if ins_seq[0] == ['invoke-direct','return-void']:#去除init函数
            CFG.remove_node(orig_method)


def get_instruction_seq_for_func(m_a, nodes):
    basic_blocks = m_a.basic_blocks

    opcode_seq,api_seq = [],[]
    for i in basic_blocks:
        instructions = list(i.get_instructions())
        for ins in instructions:
            opcode_seq.append(ins.get_name())
            operands = ins.get_operands()
            if len(operands)>2:
                api = str(operands[-1][-1])
                if api not in nodes:api_seq.append(api)
    return ' '.join([xx for x in [opcode_seq,api_seq] for xx in x]).replace(';','').lower()


def get_graph_and_nodes_ins_for_apk(apk_file, draw_graph=False):
    a, d, dx = AnalyzeAPK(apk_file)
    CFG = dx.get_call_graph()

    delete_external_and_xref0_nodes(CFG)
    delete_init_method(CFG,dx)
    delete_external_and_xref0_nodes(CFG)

    ins_seqs,nodes = {},CFG.nodes
    for orig_method in nodes:
        m_a = dx.get_method(orig_method)
        ins_seq = get_instruction_seq_for_func(m_a, [str(n) for n in nodes])
        ins_seqs[orig_method] = ins_seq

    if draw_graph:
        pos = nx.spring_layout(CFG)
        nx.draw_networkx_nodes(CFG, pos=pos, node_color='b', nodelist=nodes)
        nx.draw_networkx_edges(CFG, pos, arrow=True)
        nx.draw_networkx_labels(CFG, pos=pos, labels={x: "{}".format(ins_seqs[x]) for x in nodes})
        plt.draw()
        plt.show()
    return CFG, [ins_seqs[x] for x in CFG.nodes if x in ins_seqs]


def get_data_for_word2vec(apk_dir, saved_file_path):
    apk_files = os.listdir(apk_dir)
    with open(saved_file_path,'a') as f:
        for apk_file in apk_files:
            print(apk_dir+apk_file)
            portion = os.path.splitext(apk_file)
            if portion[1] != ".apk":continue
            CFG,node_txt = get_graph_and_nodes_ins_for_apk(apk_dir+apk_file)
            [f.write(x+'\n') for x in node_txt]


CFG,text = get_graph_and_nodes_ins_for_apk('../1.apk',True)
a=2