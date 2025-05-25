from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Chave usada para proteger a sessão e outros dados criptografados

# Configuração do banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Define o banco de dados SQLite com arquivo local
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desativa o rastreamento de modificações para economizar recursos

db = SQLAlchemy(app)  # Inicializa o SQLAlchemy para gerenciar o banco de dados com Flask

# Estruturas Dinâmicas
class Stack:
    def __init__(self):
        self.items = []  # Lista para armazenar os itens da pilha

    def push(self, item):
        self.items.append(item)  # Adiciona item no topo da pilha

    def pop(self):
        if not self.is_empty():
            return self.items.pop()  # Remove e retorna o item do topo da pilha

    def is_empty(self):
        return len(self.items) == 0  # Verifica se a pilha está vazia

class Queue:
    def __init__(self):
        self.items = []  # Lista para armazenar os itens da fila

    def enqueue(self, item):
        self.items.insert(0, item)  # Adiciona item no início da lista (final da fila)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop()  # Remove e retorna o item do final da lista (início da fila)

    def is_empty(self):
        return len(self.items) == 0  # Verifica se a fila está vazia

class Node:
    def __init__(self, data):
        self.data = data  # Valor armazenado no nó
        self.next = None  # Referência para o próximo nó da lista

class LinkedList:
    def __init__(self):
        self.head = None  # Cabeça da lista ligada, inicialmente vazia

    def append(self, data):
        new_node = Node(data)  # Cria um novo nó com os dados passados
        if not self.head:
            self.head = new_node  # Se a lista está vazia, o novo nó vira a cabeça
        else:
            current = self.head
            while current.next:
                current = current.next  # Percorre até o último nó
            current.next = new_node  # Adiciona o novo nó no final da lista

    def to_list(self):
        items = []
        current = self.head
        while current:
            items.append(current.data)  # Adiciona os dados do nó na lista Python
            current = current.next  # Avança para o próximo nó
        return items  # Retorna a lista com todos os dados da lista ligada

# Modelos do Banco de Dados
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID único do usuário
    username = db.Column(db.String(80), nullable=False, unique=True)  # Nome de usuário único e obrigatório
    password = db.Column(db.String(120), nullable=False)  # Senha do usuário armazenada com hash

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID único do material
    name = db.Column(db.String(80), nullable=False)  # Nome do material, obrigatório
    quantity = db.Column(db.Integer, nullable=False)  # Quantidade disponível do material

class Allocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID único da alocação
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)  # Chave estrangeira para material
    quantity = db.Column(db.Integer, nullable=False)  # Quantidade alocada do material
    delivery_address = db.Column(db.String(255), nullable=False)  # Endereço para entrega do material
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Chave estrangeira para usuário que fez a alocação

# Algoritmos de Ordenação
def bubble_sort(items):
    n = len(items)
    for i in range(n):
        for j in range(0, n - i - 1):
            if items[j].name > items[j + 1].name:
                items[j], items[j + 1] = items[j + 1], items[j]  # Troca os itens se estiverem fora de ordem alfabetica pelo nome
    return items  # Retorna a lista ordenada

def quick_sort(items):
    if len(items) <= 1:
        return items  # Caso base da recursão, lista com 0 ou 1 elemento já está ordenada
    pivot = items[0]  # Escolhe o primeiro elemento como pivô
    less = [x for x in items[1:] if x.name <= pivot.name]  # Sublista dos itens menores ou iguais ao pivô
    greater = [x for x in items[1:] if x.name > pivot.name]  # Sublista dos itens maiores que o pivô
    return quick_sort(less) + [pivot] + quick_sort(greater)  # Combina as sublistas ordenadas recursivamente com o pivô

# Função Recursiva para Busca Binária
def binary_search_recursive(arr, target, low, high):
    if low > high:
        return -1  # Elemento não encontrado, retorna -1
    mid = (low + high) // 2  # Ponto médio da lista
    if arr[mid].name == target:
        return mid  # Retorna o índice do elemento encontrado
    elif arr[mid].name > target:
        return binary_search_recursive(arr, target, low, mid - 1)  # Busca na metade esquerda
    else:
        return binary_search_recursive(arr, target, mid + 1, high)  # Busca na metade direita

# Rotas (mesma estrutura do primeiro código)

@app.route('/')
def home():
    return redirect(url_for('login'))  # Redireciona para a rota de login

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')  # Recebe o username do formulário
        password = request.form.get('password')  # Recebe a senha do formulário
        user = User.query.filter_by(username=username).first()  # Consulta usuário no banco
        if user and check_password_hash(user.password, password):
            # Se o usuário existe e a senha está correta
            session['user_id'] = user.id  # Salva o id do usuário na sessão para manter login
            return redirect(url_for('allocate'))  # Redireciona para a página de alocação
        else:
            # Se usuário não encontrado ou senha errada, renderiza login com erro
            return render_template('login.html', error="Usuário ou senha inválidos!")
    return render_template('login.html')  # Renderiza a página de login

@app.route('/logout')
def logout():
    session.clear()  # Limpa todos os dados da sessão (logout)
    return redirect(url_for('login'))  # Redireciona para login

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')  # Obtém o username do formulário
        password = request.form.get('password')  # Obtém a senha
        confirm = request.form.get('confirm_password')  # Confirmação da senha

        if password != confirm:
            flash("As senhas não coincidem", "error")  # Exibe mensagem de erro caso as senhas não coincidam
            return redirect(url_for('register'))  # Redireciona para a página de registro

        if User.query.filter_by(username=username).first():
            flash("Usuário já existe!", "error")  # Exibe erro se o username já está cadastrado
            return redirect(url_for('register'))  # Redireciona para a página de registro

        hashed_password = generate_password_hash(password)  # Gera hash da senha para armazenar com segurança
        new_user = User(username=username, password=hashed_password)  # Cria novo usuário
        db.session.add(new_user)  # Adiciona ao banco
        db.session.commit()  # Salva no banco
        return redirect(url_for('login'))  # Redireciona para login após registro bem-sucedido

    return render_template('register.html')  # Renderiza a página de registro

@app.route('/allocate', methods=['GET', 'POST'])
def allocate():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redireciona para login se não estiver autenticado

    materials = Material.query.all()  # Busca todos os materiais do banco
    materials_sorted = quick_sort(materials)  # Ordena os materiais pelo nome usando quick_sort

    if request.method == 'POST':
        material_id = request.form.get('material_id')  # ID do material escolhido para alocar
        quantity = int(request.form.get('quantity'))  # Quantidade solicitada
        delivery_address = request.form.get('delivery_address')  # Endereço para entrega
        user_id = session.get('user_id')  # ID do usuário logado

        material = db.session.get(Material, material_id)  # Busca o material no banco pelo ID
        if not material or material.quantity < quantity:
            # Se material não existe ou quantidade insuficiente
            return render_template('locacao.html', materials=materials_sorted, error="Quantidade insuficiente ou material inválido.")

        material.quantity -= quantity  # Atualiza a quantidade do material no banco (reduz a quantidade disponível)
        allocation = Allocation(
            material_id=material_id,
            quantity=quantity,
            delivery_address=delivery_address,
            user_id=user_id
        )  # Cria registro da alocação

        db.session.add(allocation)  # Adiciona a alocação no banco
        db.session.commit()  # Salva as alterações

        return render_template('locacao.html', materials=materials_sorted, success="Material alocado com sucesso!")

    return render_template('locacao.html', materials=materials_sorted)  # Renderiza página com materiais ordenados

@app.route('/add_material', methods=['GET', 'POST'])
def add_material():
    if request.method == 'POST':
        name = request.form.get('name')  # Nome do novo material
        quantity = int(request.form.get('quantity'))  # Quantidade inicial
        new_material = Material(name=name, quantity=quantity)  # Cria novo material
        db.session.add(new_material)  # Adiciona ao banco
        db.session.commit()  # Salva no banco
        return redirect(url_for('allocate'))  # Após adicionar material, redireciona para a página de alocação
    return render_template('add_material.html')  # Renderiza o formulário para adicionar material

@app.route('/update_material/<int:id>', methods=['GET', 'POST'])
def update_material(id):
    material = db.session.get(Material, id)  # Busca o material pelo id na URL
    if request.method == 'POST':
        new_quantity = int(request.form.get('quantity'))  # Nova quantidade enviada pelo formulário
        material.quantity = new_quantity  # Atualiza a quantidade no objeto material
        db.session.commit()  # Salva a alteração no banco
        return redirect(url_for('allocate'))  # Redireciona para a página de alocação
    return render_template('update_material.html', material=material)  # Renderiza o formulário para editar material

@app.route('/allocations')
def allocations():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redireciona para login se não autenticado

    user_id = session.get('user_id')  # Pega id do usuário da sessão
    allocations_data = db.session.query(
        Allocation.id,
        Material.name.label('material'),
        Allocation.quantity,
        Allocation.delivery_address
    ).join(Material).filter(Allocation.user_id == user_id).all()  # Consulta todas alocações do usuário, com dados do material

    # Uso da LinkedList para transformar os dados em lista (exemplo didático, não obrigatório)
    ll = LinkedList()
    for alloc in allocations_data:
        ll.append({
            'id': alloc.id,
            'material': alloc.material,
            'quantity': alloc.quantity,
            'delivery_address': alloc.delivery_address
        })
    allocations_list = ll.to_list()  # Converte lista ligada para lista normal

    return render_template('allocations.html', allocations=allocations_list)  # Renderiza a página com as alocações do usuário

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        username = request.form.get('username')  # Usuário que quer resetar a senha
        new_password = request.form.get('new_password')  # Nova senha
        confirm_password = request.form.get('confirm_password')  # Confirmação da nova senha

        user = User.query.filter_by(username=username).first()  # Busca usuário pelo username

        if not user:
            flash("Usuário não encontrado!", "error")  # Mensagem de erro se usuário não existe
            return redirect(url_for('reset_password'))  # Redireciona para a mesma página

        if new_password != confirm_password:
            flash("As senhas não coincidem!", "error")  # Erro se senhas não batem
            return redirect(url_for('reset_password'))  # Redireciona para resetar novamente

        user.password = generate_password_hash(new_password)  # Atualiza senha com hash
        db.session.commit()  # Salva no banco

        flash("Senha atualizada com sucesso! Faça login com a nova senha.", "success")  # Mensagem sucesso
        return redirect(url_for('login'))  # Redireciona para login

    return render_template('reset_password.html')  # Renderiza formulário de reset de senha

# Banco de dados e dados iniciais
def setup_database():
    with app.app_context():
        db.create_all()  # Cria todas as tabelas no banco se não existirem
        if not Material.query.first():
            # Se não houver materiais cadastrados, adiciona alguns iniciais
            db.session.add_all([
                Material(name="Cadeiras", quantity=120),
                Material(name="Mesas", quantity=80),
                Material(name="Luminárias", quantity=45)
            ])
            db.session.commit()  # Salva materiais iniciais

        if not User.query.filter_by(username="admin").first():
            # Cria usuário admin padrão se não existir
            admin = User(username="admin", password=generate_password_hash("1234"))
            db.session.add(admin)
            db.session.commit()  # Salva usuário admin

# Rodar aplicação
if __name__ == '__main__':
    setup_database()  # Configura banco e dados iniciais antes de iniciar app
    app.run(debug=True)  # Executa o servidor Flask em modo debug para facilitar desenvolvimento

