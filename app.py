import streamlit as st
from collections import deque

if "tree" not in st.session_state:
    st.session_state.tree = {}

st.set_page_config(page_title="Travel Destination Planner", page_icon="🗺️", layout="centered")
st.title("🗺️ Travel Destination Planner")

with st.form("add_form", clear_on_submit=True):
    parent = st.text_input("Parent (Country/State/City)")
    child = st.text_input("Child (State/City/Attraction)")
    submitted = st.form_submit_button("Add relation")
    if submitted:
        p = parent.strip()
        c = child.strip()
        if not p or not c:
            st.warning("Enter both parent and child")
        else:
            if p not in st.session_state.tree:
                st.session_state.tree[p] = []
            if c not in st.session_state.tree[p]:
                st.session_state.tree[p].append(c)
            if c not in st.session_state.tree:
                st.session_state.tree[c] = []
            st.success("Added")

st.divider()
st.subheader("Delete relation / node")
with st.form("del_form", clear_on_submit=True):
    name = st.text_input("Name to delete (removes subtree)")
    submitted2 = st.form_submit_button("Delete")
    if submitted2:
        key = name.strip()
        if not key:
            st.warning("Enter a name")
        else:
            if key not in st.session_state.tree:
                st.info("Not found")
            else:
                # remove subtree: delete key and remove from parents
                def collect_subtree(n, out):
                    out.add(n)
                    for ch in st.session_state.tree.get(n, []):
                        collect_subtree(ch, out)
                to_delete = set()
                collect_subtree(key, to_delete)
                for d in to_delete:
                    st.session_state.tree.pop(d, None)
                for k, v in list(st.session_state.tree.items()):
                    st.session_state.tree[k] = [x for x in v if x not in to_delete]
                st.success("Deleted subtree")

st.divider()
st.subheader("Search")
q = st.text_input("Search for place name")
if st.button("Search"):
    name = q.strip()
    if not name:
        st.info("Enter a name")
    else:
        if name in st.session_state.tree:
            st.success(f"Found {name}")
            st.write("Children:", st.session_state.tree.get(name, []))
        else:
            st.info("Not found")

st.divider()
st.subheader("Traversals")
order = st.selectbox("Choose traversal", ["Preorder","Postorder","Level-order"], index=0)
if st.button("Show traversal"):
    nodes = set(st.session_state.tree.keys())
    child_set = set([c for cl in st.session_state.tree.values() for c in cl])
    roots = [n for n in nodes if n not in child_set]
    out = []
    def preorder(n):
        if not n: return
        out.append(n)
        for c in st.session_state.tree.get(n, []):
            preorder(c)
    def postorder(n):
        if not n: return
            
    def postorder_fixed(n):
        if not n: return
        for c in st.session_state.tree.get(n, []):
            postorder_fixed(c)
        out.append(n)
    def levelorder(roots):
        q = deque(roots)
        while q:
            n = q.popleft()
            out.append(n)
            for c in st.session_state.tree.get(n, []):
                q.append(c)
    if not roots:
        st.info("No relations yet")
    else:
        if order == "Preorder":
            for r in roots:
                preorder(r)
        elif order == "Postorder":
            for r in roots:
                postorder_fixed(r)
        else:
            levelorder(roots)
        st.write(out)

st.divider()
st.subheader("Tree (Indented view)")
nodes = set(st.session_state.tree.keys())
child_set = set([c for cl in st.session_state.tree.values() for c in cl])
roots = [n for n in nodes if n not in child_set]
if not roots:
    st.caption("No relations yet")
else:
    def render(n, depth=0):
        lines = [("  " * depth) + "- " + n]
        for c in st.session_state.tree.get(n, []):
            lines += render(c, depth+1)
        return lines
    for r in roots:
        for line in render(r):
            st.text(line)

st.divider()
st.caption("Simple planner: add Country -> State -> City -> Attraction relations and explore traversals")
st.write("Raw data:")
st.json(st.session_state.tree)
