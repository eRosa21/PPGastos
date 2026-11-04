##DROP DATABASE gastos;
CREATE DATABASE IF NOT EXISTS gastos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE gastos;


SELECT id, nome, email, ativo, admin
FROM gastos.usuarios;

##UPDATE usuarios SET admin = TRUE WHERE email = 'email-do-usuario'; 
##atualizando o usuario para admin ou não
