from androguard.misc import AnalyzeAPK
from androguard.core.analysis.analysis import ExternalMethod
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
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
        if ins_seq =='' or ins_seq[0] == ['invoke-direct','return-void']:#去除init函数
            CFG.remove_node(orig_method)


def get_instruction_seq_for_func(m_a, nodes):
    basic_blocks = m_a.basic_blocks.get()

    opcode_seq,api_seq = [],[]
    for i in basic_blocks:
        instructions = list(i.get_instructions())
        for ins in instructions:
            opcode_seq.append(ins.get_name())
            operands = ins.get_operands()
            if len(operands)>2:
                api = str(operands[-1][-1])
                if api not in nodes:api_seq.append(api)
    text = ' '.join([xx for x in [opcode_seq,api_seq] for xx in x]).replace(';','').lower()
    return text


def get_graph_and_nodes_ins_for_apk(apk_file, bc,draw_graph=False):
    a, d, dx = AnalyzeAPK(apk_file)
    CFG = dx.get_call_graph()

    delete_external_and_xref0_nodes(CFG)
    delete_init_method(CFG,dx)
    delete_external_and_xref0_nodes(CFG)

    ins_seqs,nodes = {},CFG.nodes
    for orig_method in nodes:
        m_a = dx.get_method(orig_method)
        ins_seq = get_instruction_seq_for_func(m_a, [str(n) for n in nodes])
        ins_seqs[orig_method] = bc.encode([ins_seq])

    if draw_graph:
        pos = nx.spring_layout(CFG)
        nx.draw_networkx_nodes(CFG, pos=pos, node_color='b', nodelist=nodes)
        nx.draw_networkx_edges(CFG, pos, arrow=True)
        nx.draw_networkx_labels(CFG, pos=pos, labels={x: "{}".format(ins_seqs[x]) for x in nodes})
        plt.draw()
        plt.show()
    methods = list(ins_seqs.keys())
    adj_dict,L = CFG.adj,len(methods)
    adj = [(i,1,j) for i in range(L) for j in range(L) if methods[j] in adj_dict[methods[i]].keys()]
    node_feature = {}
    for i in range(L):
        if methods[i] in ins_seqs:
            node_feature[i] = ins_seqs[methods[i]]
    return adj,node_feature


if __name__=='main':
    from bert_serving.client import BertClient
    bc = BertClient()
    CFG,ins_seqs = get_graph_and_nodes_ins_for_apk('../1.apk',bc)
    a=2
