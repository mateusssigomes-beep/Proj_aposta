from models.Persist.conect_bd import conector

if __name__ == "__main__":
    conector.conectar()
    conector.criar_tabelas() 
    # conector.destruir_tabelas()
