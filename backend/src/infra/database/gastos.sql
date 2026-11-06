DROP DATABASE gastos;
CREATE DATABASE gastos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

SELECT id, nome, email, ativo, admin
FROM gastos.usuarios;


SELECT id, banco,saldo, fatura
FROM gastos.bancos;

SELECT id, valor, tipo, id_banco, meio_pagamento, dia
FROM gastos.gastos;

SHOW CREATE TABLE gastos.usuarios;
SHOW CREATE TABLE gastos.bancos;

##USE gastos;
##SHOW TABLES;
##SELECT * FROM alembic_version;

##UPDATE usuarios SET admin = TRUE WHERE email = 'email-do-usuario'; 
##atualizando o usuario para admin ou não

