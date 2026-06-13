INSERT INTO paciente (pac_id, prontuario, nome) 
VALUES (:pac_id, :prontuario, :nome)
RETURNING pac_id, prontuario, nome;