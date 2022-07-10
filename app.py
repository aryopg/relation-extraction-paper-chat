import streamlit as st
from pubmed_utils import download_pubmed_by_pmid, get_publications_list
from relation_extraction_utils import (
    named_entity_recognition_predict,
    relation_extraction_predict,
)
from graph_utils import update_database

from spacy import displacy

HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""


entities = {
    "Var": ("#2193b0", "#6dd5ed"),
    "MPA": ("#ee9ca7", "#ffdde1"),
    "Interaction": ("#de6262", "#ffb88c"),
    "Pathway": ("#56ab2f", "#a8e063"),
    "CPA": ("#eacda3", "#d6ae7b"),
    "Reg": ("#ddd6f3", "#faaca8"),
    "PosReg": ("#43cea2", "#185a9d"),
    "NegReg": ("#ff512f", "#dd2476"),
    "Disease": ("#aa9cfc", "#fc9ce7"),
    "Gene": ("#ffafbd", "#ffc3a0"),
    "Protein": ("#ffd89b", "#19547b"),
    "Enzyme": ("#ed4264", "#ffedbc"),
}

colors = {
    entity: f"linear-gradient(90deg, {colors[0]}, {colors[1]})"
    for entity, colors in entities.items()
}
options = {"ents": entities, "colors": colors}


def main():
    st.title("Knowledge Base from Biomedical Literature")

    col1, col2 = st.columns(2)

    with col1:
        st.header("Insert PMID to include a publication to the DB")
        input_pmid = st.text_input("Enter PMID", placeholder="Type Here (Ex: 29630008)")
        my_bar = st.progress(0)
        if st.button("Analyze"):
            my_bar.progress(0)

            publication = download_pubmed_by_pmid(input_pmid)
            my_bar.progress(20)

            doc = named_entity_recognition_predict(
                str(publication.title) + "\n" + str(publication.abstract)
            )
            my_bar.progress(50)

            relations = relation_extraction_predict(doc)
            my_bar.progress(75)

            update_database(relations)
            success_message = f"Found {len(relations)} relations. \n"
            success_message += (
                "New nodes and edges are added to the DB!"
                if len(relations)
                else "No new nodes and edges added to the DB"
            )
            st.success(success_message)
            my_bar.progress(90)

            html = displacy.render(doc, style="ent", options=options)
            html = html.replace("\n\n", "\n")
            my_bar.progress(100)
            st.header(f"Title: {str(publication.title)}")
            st.write(HTML_WRAPPER.format(html), unsafe_allow_html=True)
    with col2:
        st.header("Last 10 processed publications")
        df = get_publications_list(num_publications=10)
        st.table(df)


if __name__ == "__main__":
    main()
