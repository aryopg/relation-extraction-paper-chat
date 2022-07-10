from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))


def create_node(tx, name, entity_type):
    tx.run(
        f"MERGE (a:{entity_type} {{name: $name}})",
        name=name.lower().strip(),
    )


def create_relation(tx, subject, object, relation_type):
    tx.run(
        f"MATCH (a:{subject[1]}) WHERE a.name = $subject_name "
        f"MATCH (b:{object[1]}) WHERE b.name = $object_name "
        f"MERGE (a)-[:{relation_type.upper().strip()}]->(b)",
        subject_name=subject[0].lower().strip(),
        object_name=object[0].lower().strip(),
    )


def update_database(relations: list):
    print("Updating DB")
    with driver.session() as session:
        for relation in relations:
            subject, object = None, None
            for entity, argname in zip(relation.entities, relation.argNames):
                if argname == "subj":
                    subject = (entity.text.strip(), entity.entityType.strip())
                elif argname == "obj":
                    object = (entity.text.strip(), entity.entityType.strip())
                session.write_transaction(
                    create_node, entity.text.strip(), entity.entityType.strip()
                )
            session.write_transaction(
                create_relation, subject, object, relation.relationType.strip()
            )
    print("Updating DB Done!")
