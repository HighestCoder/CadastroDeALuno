Neste projeto, a persistência em arquivo foi implementada apenas para o cadastro de alunos, através do arquivo alunos.json.

Entretanto, as operações de edição e exclusão de alunos não atualizam o arquivo JSON, mantendo apenas o banco SQLite como fonte principal de dados.

Da mesma forma, a funcionalidade de Disciplina não possui persistência em arquivo, sendo salva somente no banco.

Essas melhorias (sincronização completa do JSON e persistência para disciplinas) poderão ser adicionadas em versões futuras, para alinhar totalmente o sistema à especificação.
