from fifo import app, db, User, Material, Allocation

def listar_usuarios():
    users = User.query.all()
    print("Usuários cadastrados:")
    for u in users:
        print(f"ID: {u.id} - Username: {u.username}")

def listar_materiais():
    materials = Material.query.all()
    print("\nMateriais disponíveis:")
    for m in materials:
        print(f"ID: {m.id} - Nome: {m.name} - Quantidade: {m.quantity}")

def listar_alocacoes():
    allocations = Allocation.query.all()
    print("\nAlocações realizadas:")
    for a in allocations:
        print(f"ID: {a.id} - Material ID: {a.material_id} - Quantidade: {a.quantity}")

if __name__ == "__main__":
    with app.app_context():
        listar_usuarios()
        listar_materiais()
        listar_alocacoes()
