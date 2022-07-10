from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))


def create_node(tx, name, entity_type):
    print(f"{name}: {entity_type}")
    tx.run(
        "MERGE (a:" + entity_type + " {name: $name, label: $label})",
        name=name.lower().strip(),
        label=entity_type.lower().strip(),
    )


def create_relation(tx, subject, object, relation_type):
    tx.run(
        "MATCH (a:" + subject[1] + ") WHERE a.name = $subject_name "
        "CREATE (a)-[:"
        + relation_type.upper().strip()
        + "]->(:"
        + object[1]
        + " {name: $object_name})",
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
