import re
import ast
import astor
import difflib
from difflib import SequenceMatcher
import re
import torch
from sentence_transformers import SentenceTransformer, util

"""normalize"""
def normalize(code):
    code = re.sub(r'#.*', '', code)
    code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)
    code = re.sub(r"'''.*?'''", '', code, flags=re.DOTALL)
    
    code = re.sub(r'\s+', '', code)
    
    return code

"""Checking for exact"""
def exact(code1,code2):
    if normalize(code1) == normalize(code2):
        return True
    else:
        return False

"""Checking for variable change"""
class RenameTransformer(ast.NodeTransformer):
    def __init__(self, var_name, func_name, class_name):
        self.var_name = var_name
        self.func_name = func_name
        self.class_name = class_name

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store) or isinstance(node.ctx, ast.Load):
            return ast.copy_location(ast.Name(id=self.var_name, ctx=node.ctx), node)
        return node

    def visit_arg(self, node):
        node.arg = self.var_name
        return node

    def visit_FunctionDef(self, node):
        node.name = self.func_name
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node):
        node.name = self.class_name
        self.generic_visit(node)
        return node

    def visit_Attribute(self, node):
        node.attr = self.var_name
        self.generic_visit(node)
        return node

def variable(code, var_name="var", func_name="fu", class_name="cl"):
    tree = ast.parse(code)
    transformer = RenameTransformer(var_name, func_name, class_name)
    transformed_tree = transformer.visit(tree)
    return normalize(astor.to_source(transformed_tree))

def variable_comp(code1,code2):
    return (SequenceMatcher(None, normalize(variable(code1)), normalize(variable(code2))).ratio())*100

"""checking for struct change"""
def structure(code1, code2):

    tree1 = ast.parse(code1)
    tree2 = ast.parse(code2)

    str1 = ast.unparse(tree1)
    str2 = ast.unparse(tree2)

    str1 = ''.join(str1.split())
    str2 = ''.join(str2.split())

    sm = difflib.SequenceMatcher(None, str1, str2)
    ratio = sm.ratio()

    return ratio

"""checking for obfuscated"""
def tokenize_code(code):
    tokens = re.findall(r'\w+|\S', code)
    return tokens

def obfuscated(original_code, submitted_code):

    original_tokens = tokenize_code(original_code)
    submitted_tokens = tokenize_code(submitted_code)

    similarity = difflib.SequenceMatcher(None, original_tokens, submitted_tokens).ratio()
    
    threshold = 0.5
    
    return similarity < threshold

# """checking for Semantic Similarity:"""
#
# tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
# model = BertModel.from_pretrained('bert-base-uncased')

# def encode_code(code_snippet):
#     
#     inputs = tokenizer(code_snippet, return_tensors='pt', truncation=True, padding=True)
#     outputs = model(**inputs)
#     
#     cls_embeddings = outputs.last_hidden_state[:, 0, :].detach().numpy()
#     return cls_embeddings

# def cosine_similarity(code1, code2):
#     vec1 = encode_code(code1)
#     vec2 = encode_code(code2)
#     
#     dot_product = np.dot(vec1, vec2.T)
#     norm_vec1 = np.linalg.norm(vec1)
#     norm_vec2 = np.linalg.norm(vec2)
#     return (dot_product / (norm_vec1 * norm_vec2))[0][0]

"""another method to check Semantic Similarity:"""

def sema_similarity(code1,code2):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embedding_1 = model.encode(code1, convert_to_tensor=True)
    embedding_2 = model.encode(code2, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(embedding_1, embedding_2)

    return similarity

def plag_check(code1,code2):
    exact_code = exact(code1,code2)
    var_code = variable_comp(code1,code2)
    struct_code = structure(code1,code2)
    obf_code = obfuscated(code1,code2)
    similar_code = float(sema_similarity(code1,code2))

    print(exact_code,var_code,struct_code,obf_code,similar_code)

    if exact_code:
        return False
    if var_code > 90:
        return False
    if struct_code > 0.5:
        return False
    if not(obf_code):
        return False
    if similar_code > 0.7:
        return False
    return True
