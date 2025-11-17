import tornado.ioloop
import tornado.web
import sqlite3

# Função de conexão com o banco
def conexao_db(query, valores=None):
    conexao = sqlite3.connect("db/db.sqlite3")
    cursor = conexao.cursor()

    if valores:
        cursor.execute(query, valores)
    else:
        cursor.execute(query)

    resultado = cursor.fetchall()
    conexao.commit()
    conexao.close()
    return resultado

# Handler da página inicial
class Home(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

# Listagem de usuários
class Usuarios(tornado.web.RequestHandler):
    def get(self):
        query = "SELECT * FROM usuarios"
        valores = None
        dados = conexao_db(query, valores)

        self.render("usuarios.html", usuarios=dados)


# Listagem de hidratação
class Hidratacao(tornado.web.RequestHandler):
    def get(self):
        query = """
            SELECT hidratacao.id, usuarios.nome, hidratacao.quantidade, hidratacao.data
            FROM hidratacao
            JOIN usuarios ON hidratacao.user_id = usuarios.id
        """
        valores = None
        dados = conexao_db(query, valores)

        self.render("hidratacao.html", registros=dados)

# Rotas
def make_app():
    return tornado.web.Application([
        (r"/", Home),
        (r"/usuarios", Usuarios),
        (r"/hidratacao", Hidratacao),
    ],
    template_path="templates"
    )

# Iniciar servidor

if __name__ == "__main__":
    print("Servidor rodando: http://localhost:8888")
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
