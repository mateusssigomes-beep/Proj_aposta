from validate_docbr import CPF
def validar_cpf(value: str):
    cpf = CPF()
    cpf.mask(value)
    if cpf.validate(value) == True:
        print(cpf.mask(value))
    else:
        print('Cpf Cancelado')



validar_cpf('03403646025')